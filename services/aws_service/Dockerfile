FROM python:3.8 AS python_build

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

EXPOSE 8040

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", ":8040", "main:app"]