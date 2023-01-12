FROM python:3.8 AS python_build

# Atualiza pip
RUN pip install --upgrade pip setuptools wheel
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
# Variaveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.

FROM python_build

WORKDIR /app

# Copia e Instala Requirements
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copia aplicacao
COPY app ./

EXPOSE 8020

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", ":8020", "main:app"]
#FROM python:3.10.9-alpine3.17 as python_build
#
#RUN apk update && apk upgrade && apk add py3-pip && apk add postgresql-dev gcc python3-dev musl-dev && pip install psycopg2-binary
#
#
## Variaveis de ambiente
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#ENV PYTHONPATH=.
#
#FROM python_build
#
#WORKDIR /app
#
#COPY ./requirements.txt ./
#RUN pip install -r requirements.txt
#
## Copia aplicacao
#COPY app ./
#
#EXPOSE 8010
#
#CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", ":8010", "main:app"]
