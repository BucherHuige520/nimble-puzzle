from flask import jsonify, request

from nimble.app import app
from nimble.db import db, Task


def task_to_dict(task):
    # Prefer mapper to do this, e.g. marshmallow-sqlalchemy.
    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
    }


@app.get("/task/<int:idx>")
def get_task(idx):
    task = Task.query.filter(Task.id == idx).first_or_404()
    return jsonify(task_to_dict(task))


@app.get("/task/list")
def find_task():
    filters = request.args
    conditions = []

    # Dynamic condition combination to support customizable queries.
    for key in filters:
        match key:
            case "id":
                conditions.append(Task.id == int(filters[key]))
            case "title":
                conditions.append(Task.title.contains(filters[key]))
            case "completed":
                conditions.append(Task.completed == bool(filters[key]))
            case _:
                raise KeyError(f"Invalid condition attribute: {key}")
    tasks = Task.query.filter(*conditions).all()
    return jsonify(list(map(task_to_dict, tasks)))


@app.post("/task")
def add_task():
    new_task = request.get_json()
    task = Task(
        title=new_task["title"],
        completed=False,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task_to_dict(task))


@app.put("/task")
def update_task():
    updated_task = request.get_json()
    task = Task.query.filter(Task.id == updated_task["id"]).first_or_404()
    if "title" in updated_task:
        task.title = updated_task["title"]
    if "completed" in updated_task:
        task.completed = updated_task["completed"]
    db.session.commit()
    return jsonify(task_to_dict(task))


@app.delete("/task/<int:idx>")
def delete_task(idx):
    task = Task.query.filter(Task.id == idx).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify(task_to_dict(task))


def init():
    # When imported, all apis are registered.
    pass
