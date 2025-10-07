FROM python:3.10-slim 

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

# Port number that needs to be exposed
EXPOSE 8000
# docker run -p 8000:8000 fastapi-app

CMD ["python", "main.py"]   