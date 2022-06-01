import sys
import importlib
from io import StringIO
import pytest
from types import ModuleType


@pytest.fixture(scope='module', autouse=True)
def output(module_name: str) -> str:
    stdout = sys.stdout
    with StringIO() as s:
        sys.stdout = s
        _ = importlib.import_module(module_name)
        sys.stdout = stdout
        return s.getvalue()


@pytest.fixture(scope='module')
def user_code(module_name: str) -> str:
    module = importlib.import_module(module_name)

    with open(module.__file__) as f:
        return f.read()


@pytest.fixture(scope='module')
def user_module(module_name: str) -> ModuleType:
    return importlib.import_module(module_name)
