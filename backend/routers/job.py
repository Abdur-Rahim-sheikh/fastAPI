import uuid
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models import StoryJob
from schemas import StoryJobResponse

router = APIRouter(prefix="/job", tags=["jobs"])


@router.get("/{job_id}")
def get_job_status(job_id: str, db: Annotated[Session, Depends(get_db)]):
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )

    return job
