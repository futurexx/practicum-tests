import inspect
import io
from types import ModuleType

import pytest
import sys


@pytest.fixture(scope='module')
def module_name() -> str:
    return 'task_2.author'


def test_user_module__has_contact_class(user_module: ModuleType) -> None:
    assert hasattr(user_module, 'Contact'), 'В модуле отсутствует класс Contact'
    assert inspect.isclass(user_module.Contact), 'Contact не является классом'


@pytest.mark.parametrize(
    'instance_name',
    [
        'mike',
        'vlad',
    ],
)
def test_user_module__has_instances(user_module: ModuleType, instance_name: str) -> None:
    assert hasattr(user_module, instance_name), f'В модуле отсутствует объект {instance_name}'
    assert isinstance(
        getattr(user_module, instance_name),
        user_module.Contact,
    ), f'{instance_name} не является инстансом класса Contact'


@pytest.mark.parametrize(
    'method, params',
    [
        ('__init__', {'self', 'name', 'phone', 'birthday', 'address'}),
        ('show_contact', {'self'}),
    ]
)
def test_user_module__contact_class_signature(
        user_module: ModuleType,
        method: str,
        params: set[str],
) -> None:
    contact_class = user_module.Contact

    assert hasattr(contact_class, method), f'В классе Contact отсутствует метод {method}'

    contact_class_method_params = inspect.signature(getattr(contact_class, method)).parameters.keys()
    for param in params:
        assert param in contact_class_method_params, f'Не хватает аргумента {param} в методе {method} класса Contact'

    unnecessary_params = contact_class_method_params - params
    assert not unnecessary_params, f"Лишние аргументы в методе {method}: {', '.join(unnecessary_params)}"


@pytest.mark.parametrize(
    'contact_name,data',
    [
        (
            'mike',
            {
                'name': 'Михаил Булгаков',
                'phone': '2-03-27',
                'birthday': '15.05.1891',
                'address': 'Россия, Москва, Большая Пироговская, дом 35б, кв. 6',
            },
        ),
        (
            'vlad',
            {
                'name': 'Владимир Маяковский',
                'phone': '73-88',
                'birthday': '19.07.1893',
                'address': 'Россия, Москва, Лубянский проезд, д. 3, кв. 12',
            },
        ),
    ]
)
def test_user_module__contact_class_instances(
        user_module: ModuleType,
        contact_name: str,
        data: dict[str, str],
) -> None:
    contact = getattr(user_module, contact_name)

    for attr_name in data.keys():
        attr = getattr(contact, attr_name)
        assert attr is not None, f'У {contact_name} отсутствует аттрибут {attr_name}'
        assert attr == data[attr_name], (
            f'Неверное значение атрибута {attr_name} для {contact_name}:\n'
            f'Должно быть: {data[attr_name]}\n'
            f'Имеется: {attr}'
        )


def test_user_module__show_contact(user_module: ModuleType) -> None:
    stdout = sys.stdout

    with io.StringIO() as s:
        sys.stdout = s
        contact = user_module.Contact(
            name='1',
            phone='2',
            birthday='3',
            address='4',
        )

        offset = s.truncate()

        res = contact.show_contact()
        assert res is None, 'Метод show_contact не должен возвращать значение'

        s.seek(offset)
        assert s.read() == (
            f'{contact.name} — адрес: {contact.address},'
            f' телефон: {contact.phone}, день рождения: {contact.birthday}\n'
        ), 'Неверный формат вывода у метода show_contact'

        sys.stdout = stdout


def test_user_output__show_contact(output: str, user_module: ModuleType) -> None:
    target_output = (
        f'Создаём новый контакт {user_module.mike.name}\n'
        f'Создаём новый контакт {user_module.vlad.name}\n'
        f'{user_module.mike.name} — адрес: {user_module.mike.address},'
        f' телефон: {user_module.mike.phone}, день рождения: {user_module.mike.birthday}\n'
        f'{user_module.vlad.name} — адрес: {user_module.vlad.address},'
        f' телефон: {user_module.vlad.phone}, день рождения: {user_module.vlad.birthday}\n'
    )

    assert output == target_output, 'Неверный формат вывода'
