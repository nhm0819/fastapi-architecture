FROM python:3.11-slim

COPY requirements.txt /opt/fastapi-architecture/requirements.txt
#RUN pip install --upgrade pip

RUN pip install -r /opt/fastapi-architecture/requirements.txt --no-cache-dir

COPY ./ /opt/fastapi-architecture/
WORKDIR /opt/fastapi-architecture/

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app", "--log-config", "log_conf.yaml"]