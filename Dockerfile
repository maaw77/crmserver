FROM python:3.10-slim

RUN mkdir /crmserver

RUN pip install --upgrade pip

COPY requirements.txt /crmserver

RUN pip install -r /crmserver/requirements.txt --no-cache-dir

COPY crm/ /crmserver/crm
COPY .env  /crmserver
WORKDIR /crmserver

CMD ["python", "crm/main.py"]