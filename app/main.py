"""A tiny Notes API to demonstrate CI/CD.

One feature : notes with a title and content, stored in Postgres (Neon).
One monitor : GET /health
"""
import os
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import NoteRow, get_session

# Render sets RENDER_GIT_COMMIT to the commit it deployed, so /health can say which
# version is live. Outside Render (your laptop) there is no commit, so we say "dev".
GIT_SHA = os.getenv("RENDER_GIT_COMMIT") or os.getenv("GIT_SHA", "dev")

app = FastAPI(title="Notes API", description="A tiny app to learn CI/CD", version="1.0.0")

SessionDep = Annotated[Session, Depends(get_session)]


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100, examples=["My first note"])
    content: str = Field(min_length=1, examples=["Hello from CI/CD!"])


class Note(NoteIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


@app.get("/health", tags=["monitor"])
def health() -> dict[str, str]:
    """Is the app alive? Monitors and the smoke test call this."""
    return {"status": "ok", "version": GIT_SHA}


@app.post("/notes", response_model=Note, status_code=201, tags=["notes"])
def create_note(note: NoteIn, session: SessionDep) -> NoteRow:
    """Add a note with a title and content."""
    row = NoteRow(title=note.title, content=note.content)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


@app.get("/notes", response_model=list[Note], tags=["notes"])
def list_notes(session: SessionDep) -> list[NoteRow]:
    """See all notes."""
    return list(session.scalars(select(NoteRow).order_by(NoteRow.id)))
