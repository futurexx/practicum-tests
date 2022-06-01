import inspect
from types import ModuleType

import pytest


@pytest.fixture(scope='module')
def module_name() -> str:
    return 'task_4.author'


def test_user_module__objects(user_module: ModuleType) -> None:
    assert hasattr(user_module, 'make_divider_of'), 'В модуле отсутствует функция make_divider_of'
    assert inspect.isfunction(getattr(user_module, 'make_divider_of')), f'make_divider_of не является функцией'


def test_user_module__functions_signature(user_module: ModuleType) -> None:
    func_params = inspect.signature(getattr(user_module, 'make_divider_of')).parameters.keys()
    assert 'divider' in func_params, 'Не хватает аргумента divider в функции make_divider_of'
    assert len(func_params) == 1, 'Слишком много аргументов у функции make_divider_of'


def test_user_module__make_divider_of(user_module: ModuleType) -> None:
    divider_of_5 = user_module.make_divider_of(5)

    assert inspect.isfunction(divider_of_5), 'Функция make_divider_of должна возвращать функцию'

    res = divider_of_5(5)
    assert res == 1.0, f'make_divider_of(5)(5) != {res}'

    res = divider_of_5(1)
    assert res == 0.2, f'make_divider_of(5)(1) != {res}'

    res = divider_of_5(-5)
    assert res == -1.0, f'make_divider_of(5)(-5) != {res}'

    with pytest.raises(ZeroDivisionError):
        divider_of_0 = user_module.make_divider_of(0)
        divider_of_0(5)


def test_user_output__make_divider_of(output: str, user_module: ModuleType) -> None:
    assert output == '5.0\n4.0\n2.0\n', 'Неверный формат вывода'