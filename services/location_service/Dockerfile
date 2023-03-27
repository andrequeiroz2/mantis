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

EXPOSE 8030

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", ":8030", "main:app"]

