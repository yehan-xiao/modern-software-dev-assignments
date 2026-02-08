from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import db
from ..services.extract import extract_action_items


# --- Pydantic Schema ---

class ExtractRequest(BaseModel):
    text: str                    # 必填，要提取行动项的文本
    save_note: bool = False      # 可选，是否同时保存为笔记

class ActionItemOut(BaseModel):
    id: int
    text: str

class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: list[ActionItemOut]

class ActionItemDetail(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str

class MarkDoneRequest(BaseModel):
    done: bool = True            # 可选，默认标记为完成

class MarkDoneResponse(BaseModel):
    id: int
    done: bool


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    try:
        note_id: Optional[int] = None
        if payload.save_note:
            note_id = db.insert_note(payload.text)

        items = extract_action_items(payload.text)
        ids = db.insert_action_items(items, note_id=note_id)
    except Exception:
        raise HTTPException(status_code=500, detail="failed to extract action items")
    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemOut(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.get("", response_model=list[ActionItemDetail])
def list_all(note_id: Optional[int] = None) -> list[ActionItemDetail]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemDetail(
            id=r["id"], note_id=r["note_id"], text=r["text"],
            done=bool(r["done"]), created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    try:
        db.mark_action_item_done(action_item_id, payload.done)
    except Exception:
        raise HTTPException(status_code=500, detail="failed to update action item")
    return MarkDoneResponse(id=action_item_id, done=payload.done)


