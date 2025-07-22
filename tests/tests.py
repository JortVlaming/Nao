"""
WARNING: DO NOT RUN WITH AN ACTUAL NAO ROBOT (or do idk what happens lol)
this will connect every proxy and call every single method on the proxy
"""

import importlib
import inspect
import pkgutil
import traceback

from typing import Callable

import Nao
from Nao import Robot
import inspect
from typing import Callable, get_origin

robot = Robot("127.0.0.1", 9559)

def dummy_callback(*args, **kwargs):
    print("Dummy callback called with: " + str(args) + " and " + str(kwargs))


def dummy_arg_for(param):
    # Simple logic to generate dummy values based on param name or annotation
    name = param.name.lower()
    annotation = param.annotation
    origin = get_origin(annotation)

    if param.default is not inspect.Parameter.empty:
        return param.default
    if "name" in name or "path" in name or "behavior" in name:
        return "test"
    if "id" in name:
        return 0
    if "list" in name or annotation in [list, tuple]:
        return []
    if "bool" in name or annotation is bool:
        return False
    if annotation is int:
        return 0
    if annotation is float:
        return 0.0
    if origin is Callable:
        # Return a dummy callable that accepts any args and does nothing
        return dummy_callback
    return "test"  # fallback


SKIP_METHODS = ["disconnect_all"]
IGNORE_NONETYPE = True
PRINT_NONETYPE = False

def run_test(proxy):
    proxy.debug_mode = True
    proxyName = type(proxy).__name__
    print(f"[super] Executing {proxyName} tests")

    methods = {
        name: method
        for name, method in proxy.__class__.__dict__.items()
        if callable(method) and not name.startswith("_") and name not in SKIP_METHODS
    }

    ran = 0

    for method_name in methods:
        if method_name in SKIP_METHODS:
            continue
        method = getattr(proxy, method_name)

        try:
            sig = inspect.signature(method)
            params = sig.parameters.values()

            # Generate dummy args for parameters, skip 'self'
            args = [dummy_arg_for(p) for p in params if p.name != "self"]

            print(f"[{proxyName}] running Method {method_name} with args {args}")
            result = method(*args)
            ran += 1
            print(f"[{proxyName}] result for {method_name}: {result}")
        except Exception as e:
            if "'NoneType' object has no attribute" and IGNORE_NONETYPE:
                if PRINT_NONETYPE:
                    print(f"[{proxyName}] Threw a NoneType error but we're ignoring those")
                ran += 1
                continue
            print(f"[{proxyName}] error running {method_name}: {e}")
            traceback.print_exc()

    proxy.disconnect_all()

    print(f"[super] Executed {ran} {proxyName} tests")

def find_al_classes(package):
    al_classes = {}

    # Walk through all modules in the package
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f"[WARN] Skipping {module_name}: {e}")
            continue

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name.startswith("AL") and obj.__module__.startswith(package.__name__):
                al_classes[name] = obj

    return al_classes

al_classes = find_al_classes(Nao)

print("Detected AL classes:")
instances = {}
for name, cls in al_classes.items():
    try:
        print("-", name)
        instances[name] = cls(robot)
    except Exception as e:
        print(f"Failed to instantiate {name}: {e}")

for instance in instances.values():
    run_test(instance)