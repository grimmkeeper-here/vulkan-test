FROM python:3.12.5-alpine3.19
WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

CMD ["python", "src/main.py"]
