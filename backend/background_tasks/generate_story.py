from datetime import datetime

from core.story_generator import StoryGenerator
from db.database import SessionLocal
from models import StoryJob


def generate_story_task(job_id: str, theme: str, session_id: str):
    db = SessionLocal()
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        if not job:
            return
        try:
            job.status = "processing"
            db.commit()

            # story = {}  # TODO: generate story
            story = StoryGenerator.generate_story(db, session_id, theme)
            job.story_id = story.id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            db.commit()
    finally:
        db.close()
