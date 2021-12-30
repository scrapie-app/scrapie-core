FROM python:3.9.9-buster

WORKDIR /app

COPY . .

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD [ "NODE_ENV=development", "poetry", "run", "python", "main.py" ]
