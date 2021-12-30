FROM python:3.9.9-buster

WORKDIR /app

COPY . .

COPY scripts/init.sql /docker-entrypoint-initdb.d/

ENV NODE_ENV=production

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD [ "alembic", "upgrade", "head" ]

ENTRYPOINT [ "poetry", "run", "python", "main.py" ]