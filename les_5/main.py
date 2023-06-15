# Задание
#
# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. Для
# каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку
# Pedantic.

from pydantic import BaseModel
from fastapi import FastAPI
from typing import Dict
from collections import defaultdict

app = FastAPI()


class Task_list(BaseModel):
    id: int
    title: str
    description: str
    status: bool = False


task_dict: Dict[int, Task_list] = defaultdict()


@app.get("/tasks")
async def read_tasks(skip: int = 0, limit: int = 100):
    return list(task_dict.values())[skip: skip + limit]


@app.get("/tasks/{task_id}", response_model=Task_list)
async def read_task(task_id: int):
    return task_dict[task_id]


@app.post("/tasks", response_model=Task_list)
async def create_task(task: Task_list):
    task_id = len(task_dict) + 1
    date_task = Task_list(id=task_id, **task.dict())
    task_dict[task_id] = date_task
    return date_task


@app.put("/tasks/{task_id}", response_model=Task_list)
async def update_task(task_id: int, task: Task_list):
    date_task = task_dict[task_id]
    for field, value in task.dict(exclude_unset=True).items():
        setattr(date_task, field, value)
    return date_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    del task_dict[task_id]
    return {"RESULT": "OK"}
