FROM python:3.10-slim
RUN apt-get update && apt-get install -y git
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py /app/main.py
WORKDIR /app
CMD ["python", "main.py"]
