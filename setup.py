import platform
import shutil

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys, os, subprocess
from pathlib import Path
import requests

def is_writable(path):
    return os.access(path, os.W_OK)

def move_with_elevation(src, dst, plat):
    if is_writable(os.path.dirname(dst)):
        # Normal move
        import shutil
        shutil.move(src, dst)
        return

    if plat in ("linux", "mac"):
        # Linux/macOS: sudo
        print("sudo perms to move the files please :D")
        subprocess.run(["sudo", sys.executable, "-c",
                        f"import shutil; shutil.move(r'{src}', r'{dst}')"],
                       check=True)
    elif plat == "windows":
        # Windows: runas
        # This opens a new command prompt as administrator
        subprocess.run(["powershell", "-Command",
                        f"Start-Process python -ArgumentList '-c \"import shutil; shutil.move(r'''{src}''', r'''{dst}''')\"' -Verb RunAs"],
                       check=True)
    else:
        raise RuntimeError(f"Unsupported platform: {plat}")

def download_naoqi(platform: str):
    expected_path = get_expected_qi_sdk_path(platform)

    if os.path.exists(expected_path):
        print(f"Found expected path {expected_path}")
        print("nuke it or i wont work >:(")

        raise RuntimeError(f"Naoqi already exists in {expected_path}.")

    url = f"https://api.crystalcoding.org/files/projects/naoqi/platforms"

    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError("Failed to get naoqi platforms.")
    platforms_available = res.json()
    print(f"platforms available: {platforms_available}")
    if platform not in platforms_available:
        raise RuntimeError(f"Platform {platform} not available")

    url = f"{url}/{platform}"

    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Platform {platform} not available")

    cd = res.headers.get("Content-Disposition")
    if cd:
        # Usually looks like: 'attachment; filename="windows.zip"'
        import re
        fname_match = re.findall(r'filename="?([^"]+)"?', cd)
        filename = fname_match[0] if fname_match else platform
    else:
        filename = platform

    # Save file
    with open(filename, "wb") as f:
        f.write(res.content)
    print(f"Downloaded as {filename}")

    extract_to = "temporary_for_naoqi_installation"

    if os.path.exists(extract_to):
        print(f"Removing {extract_to} (how did it even exist lmao)")
        shutil.rmtree(extract_to)

    os.makedirs(extract_to)

    if filename.endswith(".zip"):
        import zipfile
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Extracted {filename} to {extract_to}")

    elif filename.endswith((".tar.gz", ".tgz", ".tar.bz2", ".tar")):
        import tarfile
        with tarfile.open(filename, "r:*") as tar_ref:
            tar_ref.extractall(extract_to)
        print(f"Extracted {filename} to {extract_to}")
    else:
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(extract_to):
            shutil.rmtree(extract_to)
        raise RuntimeError(f"File type not supported for auto-extract: {filename}, files have been cleaned")

    os.remove(filename)

    dir_with_the_shit = os.listdir(extract_to)[0]

    dir_with_the_shit = os.path.join(extract_to, dir_with_the_shit)

    move_with_elevation(dir_with_the_shit, expected_path, platform)

    print("Installed naoqi sdk. it is located at " + expected_path)
    print("cleaning up")

    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)

    return expected_path


def get_plat():
    if sys.platform.startswith("linux"):
        plat = "linux"
    elif sys.platform == "darwin":
        plat = "mac"
    elif sys.platform.startswith("win"):
        plat = "windows"
    else:
        plat = sys.platform
    return plat

def get_expected_qi_sdk_path(plat):
    if plat.startswith("linux"):
        sdk_path = "/opt/naoqi-sdk"
    elif plat == "darwin":
        sdk_path = "/usr/local/naoqi-sdk"
    elif plat.startswith("win"):
        sdk_path = "C:\\Program Files\\naoqi-sdk"
    else:
        sdk_path = None
    return sdk_path


def get_qi_sdk_path():
    sdk_path = os.getenv("QI_SDK_PATH")
    if sdk_path and os.path.exists(sdk_path):
        return sdk_path

    plat = get_plat()
    sdk_path = get_expected_qi_sdk_path(plat)

    if sdk_path and os.path.exists(sdk_path):
        return sdk_path

    is_installed = input("NAOqi SDK not found. Have you installed NAOqi? (y/N): ").lower() == "y"

    if is_installed:
        sdk_path = input("Please enter its path: ")
        if not os.path.exists(sdk_path):
            print("Path does not exist. Exiting.")
            sys.exit(1)

        return sdk_path

    install_it = input("Install NAOqi? (y/N): ").lower() == "y"

    if not install_it:
        print("NAOqi SDK not found. Exiting.")
        sys.exit(1)

    return download_naoqi(plat)

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        build_temp = Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = Path(self.get_ext_fullpath(ext.name)).parent.resolve()
        cfg = 'Release'

        qi_sdk_path = get_qi_sdk_path()

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}/nao",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
            f"-DQI_SDK_PATH={qi_sdk_path}",
        ]

        build_args = ["--config", cfg]

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_temp)

if __name__ == "__main__":
    setup(
        name="nao",
        version="0.1.0",
        author="Jort Vlaming",
        description="Python bindings for NAO robot C++ library",
        ext_modules=[CMakeExtension("_nao_bindings")],
        cmdclass={"build_ext": CMakeBuild},
        packages=["nao"],
        zip_safe=False,
        include_package_data=True,
    )
