from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SpyCat
from app.schemas import SpyCatCreate, SpyCatUpdate, SpyCatResponse
from app.services.cat_api import validate_breed

router = APIRouter(prefix="/cats", tags=["Spy Cats"])


@router.post("/", response_model=SpyCatResponse, status_code=status.HTTP_201_CREATED)
def create_cat(cat_data: SpyCatCreate, db: Session = Depends(get_db)):
    if not validate_breed(cat_data.breed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid breed: '{cat_data.breed}'. Please use a valid cat breed."
        )

    cat = SpyCat(**cat_data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.get("/", response_model=List[SpyCatResponse])
def list_cats(db: Session = Depends(get_db)):
    return db.query(SpyCat).all()


@router.get("/{cat_id}", response_model=SpyCatResponse)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spy cat with id {cat_id} not found"
        )
    return cat


@router.patch("/{cat_id}", response_model=SpyCatResponse)
def update_cat(cat_id: int, cat_data: SpyCatUpdate, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spy cat with id {cat_id} not found"
        )

    cat.salary = cat_data.salary
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spy cat with id {cat_id} not found"
        )

    db.delete(cat)
    db.commit()
    return None

