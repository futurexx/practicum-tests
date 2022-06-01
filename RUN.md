## Запуск тестов:

### Локально
```bash
pip install poetry==1.1 && poetry run pytest
```
### Через Docker
```bash
docker build -t tests . && docker run tests
```