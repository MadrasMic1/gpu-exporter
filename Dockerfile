FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y pciutils && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9835

CMD ["python","app.py"]