import uuid

from fastapi import Cookie


def get_session_id(session_id: str | None = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id
