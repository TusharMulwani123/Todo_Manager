from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

async def get_all_todos(db: AsyncSession):
    result = await db.execute(select(Todo))
    return result.scalars().all()

async def get_todo(db: AsyncSession, todo_id: int):
   result = await db.execute(select(Todo).where(Todo.id == todo_id))
   return result.scalar_one_or_none()

async def create_todo(db: AsyncSession, todo: TodoCreate):
   new_todo = Todo(**todo.model_dump())
   db.add(new_todo)
   await db.commit()
   await db.refresh(new_todo)
   return new_todo

async def update_todo(db: AsyncSession, todo_id: int, updates: TodoUpdate):
   db_todo = await get_todo(db, todo_id)
   if not db_todo:
      return None
   for field, value in updates.dict(exclude_unset=True).items():
      setattr(db_todo, field, value)
   await db.commit()
   await db.refresh(db_todo)
   return db_todo
async def delete_todo(db: AsyncSession, todo_id: int):
   db_todo = await get_todo(db, todo_id)
   if db_todo:
      await db.delete(db_todo)
      await db.commit()
   return db_todo