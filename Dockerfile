FROM python:3.11-slim
WORKDIR /app
COPY app app
COPY requirements.txt requirements.txt
COPY index.html index.html
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

