# FastAPI Tutorial and Guide

## What is FastAPI?

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It's designed to be easy to use and learn, fast to code, and ready for production.

### Key Features:
- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Increase development speed by 200-300%
- **Fewer bugs**: Reduce developer-induced errors by 40%
- **Intuitive**: Great editor support with autocompletion
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication
- **Robust**: Get production-ready code with automatic interactive documentation

## Installation

```bash
        pip install fastapi
        pip install uvicorn[standard]  # ASGI server
```

## Basic FastAPI Application

### 1. Simple Hello World

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### 2. Running the Application

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload during development.

## Core Concepts

### 1. Path Parameters

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### 2. Query Parameters

```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/items/")
    def read_items(skip: int = 0, limit: int = 10):
        return {"skip": skip, "limit": limit}
```

### 3. Request Body with Pydantic Models

```python
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()

    class Item(BaseModel):
        name: str
        description: str = None
        price: float
        tax: float = None

    @app.post("/items/")
    def create_item(item: Item):
        return item
```

### 4. Response Models

```python
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()

    class Item(BaseModel):
        name: str
        description: str = None
        price: float
        tax: float = None

    class ItemResponse(BaseModel):
        name: str
        price: float

    @app.post("/items/", response_model=ItemResponse)
    def create_item(item: Item):
        return item
```

## Advanced Features

### 1. Dependency Injection

```python
    from fastapi import FastAPI, Depends

    app = FastAPI()

    def get_db():
        # Database connection logic
        return "database_connection"

    @app.get("/items/")
    def read_items(db = Depends(get_db)):
        return {"db": db}
```

### 2. HTTP Status Codes

```python
    from fastapi import FastAPI, status
    from fastapi.responses import JSONResponse

    app = FastAPI()

    @app.post("/items/", status_code=status.HTTP_201_CREATED)
    def create_item(item: Item):
        return item

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        if item_id == 0:
            return JSONResponse(
                status_code=404,
                content={"message": "Item not found"}
            )
        return {"item_id": item_id}
```

### 3. Form Data

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

### 4. File Uploads

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

### 5. Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

## Error Handling

### 1. HTTPException

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

### 2. Custom Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )

@app.get("/unicorns/{name}")
def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

## Middleware

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## CORS (Cross-Origin Resource Sharing)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security

### 1. OAuth2 with Password (and hashing)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Testing

### 1. TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item():
    response = client.get("/items/5?q=somequery")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": "somequery"}
```

## Production Deployment

### 1. Using Gunicorn with Uvicorn Workers

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 2. Docker Deployment

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Best Practices

1. **Use Type Hints**: Always use Python type hints for better IDE support and validation
2. **Pydantic Models**: Use Pydantic models for request/response validation
3. **Dependency Injection**: Use FastAPI's dependency system for reusable components
4. **Error Handling**: Implement proper error handling with HTTPException
5. **Documentation**: FastAPI automatically generates OpenAPI documentation
6. **Testing**: Write tests using TestClient
7. **Security**: Implement proper authentication and authorization
8. **Performance**: Use async/await for I/O operations

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`

## Common Use Cases

1. **REST APIs**: Building RESTful web services
2. **Microservices**: Creating lightweight microservices
3. **Data APIs**: Exposing data from databases
4. **Webhooks**: Creating webhook endpoints
5. **Real-time APIs**: WebSocket support for real-time communication

## Performance Tips

1. Use async/await for I/O operations
2. Use Pydantic for data validation (faster than manual validation)
3. Use dependency injection to avoid code duplication
4. Use background tasks for non-critical operations
5. Implement proper caching strategies
6. Use connection pooling for databases

FastAPI is an excellent choice for building modern, fast, and reliable APIs with Python. Its automatic documentation generation, type safety, and high performance make it a popular choice for both small projects and large-scale applications.
