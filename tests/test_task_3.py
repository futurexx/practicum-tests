import inspect
import io
from types import ModuleType

import pytest
import sys


@pytest.fixture(scope='module')
def module_name() -> str:
    return 'task_3.author'


@pytest.mark.parametrize(
    'func_name',
    [
        'time_check',
        'cache_args',
        'long_heavy',
    ]
)
def test_user_module__objects(user_module: ModuleType, func_name: str) -> None:
    assert hasattr(user_module, func_name), f'В модуле отсутствует функция {func_name}'
    assert inspect.isfunction(getattr(user_module, func_name)), f'{func_name} не является функцией'


@pytest.mark.parametrize(
    'func_name,params',
    [
        ('time_check', {'func'}, ),
        ('cache_args', {'func'}, ),
        ('long_heavy', {'args'}, ),
    ],
)
def test_user_module__functions_signature(
        user_module: ModuleType,
        func_name: str,
        params: set[str],
) -> None:
    func_params = inspect.signature(getattr(user_module, func_name)).parameters.keys()

    for param in params:
        assert param in func_params, f'Не хватает аргумента {param} в функции {func_name}'

    assert len(func_params) == 1, f'Слишком много аргументов у функции {func_name}'


def test_user_module__cache_args(user_module: ModuleType):
    f = lambda x: print(f'execute for {x}')
    cached_f = user_module.cache_args(f)

    assert inspect.isfunction(cached_f), 'Функция cache_args должна возвращать функцию'

    stdout = sys.stdout
    with io.StringIO() as s:
        sys.stdout = s
        res = cached_f('test_1')
        assert res is None, 'Функция cache_args не должна изменять результат декорируемой функции'
        s.seek(0)
        assert s.read() == 'execute for test_1\n', (
            'Функция cache_args не должна модифицировать вывод декорируемой функции'
        )

        offset = s.truncate()
        cached_f('test_1')
        s.seek(offset)
        assert s.read() == '', (
            'Функция cache_args не кэширует результат исполнения функции при одном и том же аргументе'
        )

        sys.stdout = stdout


def test_user_output__cache_args(output: str, user_module: ModuleType) -> None:
    target_output = (
        'Время выполнения функции: 1.0 с.\n'
        '2\n'
        'Время выполнения функции: 0.0 с.\n'
        '2\n'
        'Время выполнения функции: 1.0 с.\n'
        '4\n'
        'Время выполнения функции: 0.0 с.\n'
        '4\n'
        'Время выполнения функции: 0.0 с.\n'
        '4\n'
    )

    assert output == target_output, 'Неверный формат вывода'
