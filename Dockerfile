FROM python:3.9-slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py /app/main.py
WORKDIR /app
CMD ["python", "main.py"]
