
from datetime import date
from backend.app.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.task import Task, TaskStatus
from backend.app.schemas.task import TaskCreate, TaskUpdate, TaskResponse


router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task















@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()

    return {
        "total": len(tasks),
        "todo": sum(t.status == TaskStatus.TODO for t in tasks),
        "in_progress": sum(t.status == TaskStatus.IN_PROGRESS for t in tasks),
        "completed": sum(t.status == TaskStatus.COMPLETED for t in tasks),
        "overdue": sum(
            t.due_date < date.today() and t.status != TaskStatus.COMPLETED
            for t in tasks
        )
    }


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")

    return task

#mise a joure de tasck
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"Le champ {field} ne peut pas être nul"
            )
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task









@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")

    db.delete(task)
    db.commit()
    return {"message": "Tâche supprimée avec succès"}

