import uuid
from datetime import datetime

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from background_tasks import generate_story_task
from data import DefaultStory
from db.database import SessionLocal, get_db
from dependencies import get_session_id
from models import Story, StoryJob, StoryNode
from schemas import (
    CompleteStoryNodeResponse,
    CompleteStoryResponse,
    CreateStoryRequest,
    StoryJobResponse,
)

default_story = DefaultStory()

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db),
) -> StoryJobResponse:
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending",
    )
    db.add(job)
    db.commit()

    background_tasks.add_task(generate_story_task, job_id, request.theme, session_id)

    return job


@router.get("/{story_id}/complete")
def get_complete_story(
    story_id: int,
    db: Session = Depends(get_db),
) -> CompleteStoryResponse:
    story = db.query(Story).filter(Story.id == story_id).first()

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Story not found"
        )
    complete_story = default_story.build_complete_story_tree(db, story)
    return complete_story
