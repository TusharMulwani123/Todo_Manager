from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.schemas.todo import TodoCreate, TodoOut, TodoUpdate
from app.crud import todo as crud
router = APIRouter()
async def get_db():
  async with SessionLocal() as session:
     yield session
@router.get("/", response_model=list[TodoOut])
async def list_todos(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_todos(db)
@router.post("/", response_model=TodoOut, status_code=201)
async def create(db: AsyncSession = Depends(get_db), todo: TodoCreate = Depends()):
   return await crud.create_todo(db, todo)
@router.get("/{todo_id}", response_model=TodoOut)
async def retrieve(todo_id: int, db: AsyncSession = Depends(get_db)):
  todo = await crud.get_todo(db, todo_id)
  if not todo:
   raise HTTPException(status_code=404, detail="Todo not found")
  return todo
@router.put("/{todo_id}", response_model=TodoOut)
async def update(todo_id: int, updates: TodoUpdate, db: AsyncSession = Depends(get_db)):
  updated = await crud.update_todo(db, todo_id, updates)
  if not updated:
    raise HTTPException(status_code=404, detail="Todo not found")
  return updated
@router.delete("/{todo_id}", status_code=204)
async def delete(todo_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_todo(db, todo_id)
    if not deleted:
       raise HTTPException(status_code=404, detail="Todo not found")