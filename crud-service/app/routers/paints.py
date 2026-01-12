from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Paint
from app.schemas import PaintCreate, PaintOut
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/paints", tags=["Paints"])

@router.post("/", response_model=PaintOut)
def create_paint(paint: PaintCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_paint = Paint(**paint.dict())
    db.add(db_paint)
    db.commit()
    db.refresh(db_paint)
    return db_paint