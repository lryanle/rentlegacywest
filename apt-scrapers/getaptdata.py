import os
import importlib
import glob
import json

files = glob.glob(os.path.dirname(__file__) + "/*.py")
files = [file for file in files if not (os.path.basename(file).startswith("_") or os.path.basename(file).startswith("getaptdata"))]

apts = [file.split("/")[-1].split(".")[0] for file in files]

for file in files:
    if file != os.path.basename(__file__):
        module_name = os.path.basename(file)[:-3]
        print(f"Importing {module_name}")
        module = importlib.import_module(module_name)
        functions = dir(module)
        for function in functions:
            if not function.startswith("__"):
                globals()[function] = getattr(module, function)

data = {}
print(dir())
for function in dir():
    if function in apts:
        data[function] = globals()[function]()

# write to separate files based on the function name
for function in data:
    with open(f"{os.path.dirname(__file__)}/data/{function}.json", "w") as f:
        f.write(json.dumps(data[function], indent=2))

