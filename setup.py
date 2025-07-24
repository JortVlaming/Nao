from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys, os, subprocess
from pathlib import Path

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

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
        ]

        build_args = ["--config", cfg]

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_temp)

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
