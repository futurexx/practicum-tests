FROM python:3.9.10-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /code

COPY poetry.lock pyproject.toml ./
COPY task_2 ./task_2
COPY task_3 ./task_3
COPY task_4 ./task_4

RUN pip install poetry==1.1 && \
    poetry install

RUN rm -rf $HOME/.cache/pypoetry/artifacts/*

COPY tests ./tests

CMD ["poetry", "run", "pytest"]