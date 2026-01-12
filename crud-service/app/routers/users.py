from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import UserCreate, UserResponse
from app.deps import get_current_active_user, get_db
from app.models import User as UserModel
from app.auth import get_password_hash
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
def get_users(current_user: UserModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get all users"""
    return db.query(UserModel).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, current_user: UserModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get one user by ID"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    
    db_user = UserModel(
        email=user.email,
        role=user.role,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, updated_user: UserCreate, current_user: UserModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Update a user"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db_user.email=updated_user.email,
    db_user.role=updated_user.role,
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: UserModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Delete a user"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}