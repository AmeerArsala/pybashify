import sys
import tomli
from pybashify.constants import PROJECT_ROOT


if __name__ == "__main__":
    # Read the new version
    with open(f"{PROJECT_ROOT}/pyproject.toml", 'rb') as pyproject_dot_toml_file:
        pyproject_dot_toml: dict = tomli.load(pyproject_dot_toml_file)

    version: str = pyproject_dot_toml["project"]["version"]
    
    sys.stdout.write(version)
    sys.exit(0)
