from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Story, StoryNode
from schemas import CompleteStoryNodeResponse, CompleteStoryResponse


class DefaultStory:
    def build_complete_story_tree(
        self, db: Session, story: Story
    ) -> CompleteStoryResponse:
        nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()
        nodes_dict = {}
        for node in nodes:
            node_response = CompleteStoryNodeResponse(
                id=node.id,
                content=node.content,
                is_ending=node.is_ending,
                is_winning_ending=node.is_winning_ending,
                options=node.options,
            )
            nodes_dict[node.id] = node_response

        root_node = next((node for node in nodes if node.is_root), None)

        if not root_node:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Story root node not found",
            )

        return CompleteStoryResponse(
            id=story.id,
            title=story.title,
            session_id=story.session_id,
            created_at=story.created_at,
            root_node=nodes_dict[root_node.id],
            all_nodes=nodes_dict,
        )
