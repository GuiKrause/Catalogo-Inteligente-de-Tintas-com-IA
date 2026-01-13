from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.paints import Paint as PaintModel
from app.schemas.paints import PaintResponse, PaintCreate
from app.utils.deps import UserModel, get_current_active_user, get_current_admin_user, get_db
from app.utils.embeddings import text_generate_for_embedding
from app.core.clients import client
from app.core.config import settings

router = APIRouter(prefix="/paints", tags=["Paints"])

@router.post("/", response_model=PaintResponse, status_code=status.HTTP_201_CREATED)
def create_tinta(
    tinta: PaintCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    admin_user: UserModel = Depends(get_current_admin_user)
):
    # 1. Gera texto rico
    texto_embedding = text_generate_for_embedding(tinta)

    # 2. Chama OpenAI
    try:
        response = client.embeddings.create(
            model=settings.EMBEDDINGS_MODEL,
            input=texto_embedding
        )
        embedding = response.data[0].embedding
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar embedding: {str(e)}"
        )

    # 3. Cria objeto SQLAlchemy
    db_tinta = PaintModel(
        **tinta.dict(),
        embedding=embedding
    )

    # 4. Salva no banco
    db.add(db_tinta)
    db.commit()
    db.refresh(db_tinta)

    return db_tinta



@router.get("/", response_model=List[PaintResponse])
def get_paints(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Get all paints"""
    return db.query(PaintModel).all()


@router.get("/{paint_id}", response_model=PaintResponse)
def get_paint(
    paint_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """Get paint by ID"""
    paint = db.query(PaintModel).filter(PaintModel.id == paint_id).first()

    if not paint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paint not found"
        )

    return paint


@router.delete("/{paint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paint(
    paint_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    admin_user: UserModel = Depends(get_current_admin_user)
):
    """Delete a paint"""
    paint = db.query(PaintModel).filter(PaintModel.id == paint_id).first()

    if not paint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paint not found"
        )

    db.delete(paint)
    db.commit()
