from sqlalchemy.orm import Session

from models import Story
from schemas import CompleteStoryResponse


class DefaultStory:
    def build_complete_story_tree(
        self, db: Session, story: Story
    ) -> CompleteStoryResponse:
        pass
