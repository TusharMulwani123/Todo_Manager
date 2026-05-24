from fastapi import FastAPI 
from app.api.v1.routes import todo
app = FastAPI(title="Todo Manager API", version="1.0.0") 
app.include_router(todo.router, prefix="/api/v1/todos", tags=["Todos"])