from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Job, User
from app.schemas.jobs import JobCreate, JobPublic, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _get_job_or_404(db: Session, job_id: int, user_id: int) -> Job:
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/", response_model=list[JobPublic])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Job)
        .filter(Job.user_id == current_user.id)
        .order_by(Job.created_at.desc())
        .all()
    )


@router.post("/", response_model=JobPublic, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = Job(user_id=current_user.id, **payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobPublic)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_job_or_404(db, job_id, current_user.id)


@router.patch("/{job_id}", response_model=JobPublic)
def update_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = _get_job_or_404(db, job_id, current_user.id)

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(job, k, v)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = _get_job_or_404(db, job_id, current_user.id)
    db.delete(job)
    db.commit()
    return None