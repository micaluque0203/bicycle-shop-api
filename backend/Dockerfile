FROM python:3.9

RUN pip install poetry

WORKDIR /backend


COPY ../pyproject.toml ../poetry.lock ./

COPY . .
RUN poetry lock
RUN poetry install --no-root


ENV PYTHONPATH="${PWD}/backend/src"

EXPOSE 8001

CMD ["/api/entrypoint.sh"]
