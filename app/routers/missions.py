from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Mission, Target, SpyCat
from app.schemas import MissionCreate, MissionAssign, MissionResponse

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
def create_mission(mission_data: MissionCreate, db: Session = Depends(get_db)):
    if mission_data.cat_id is not None:
        cat = db.query(SpyCat).filter(SpyCat.id == mission_data.cat_id).first()
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spy cat with id {mission_data.cat_id} not found"
        )
        existing_mission = db.query(Mission).filter(Mission.cat_id == mission_data.cat_id).first()
        if existing_mission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Spy cat with id {mission_data.cat_id} already has an active mission"
        )

    mission = Mission(cat_id=mission_data.cat_id, complete=False)
    db.add(mission)
    db.flush()

    for target_data in mission_data.targets:
        target = Target(
            mission_id=mission.id,
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
            complete=False
        )
        db.add(target)

    db.commit()
    db.refresh(mission)
    return mission


@router.get("/", response_model=List[MissionResponse])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )

    if mission.cat_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a mission that is assigned to a cat"
        )

    db.delete(mission)
    db.commit()
    return None


@router.patch("/{mission_id}/assign", response_model=MissionResponse)
def assign_cat_to_mission(mission_id: int, assign_data: MissionAssign, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )

    if mission.complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign a cat to a completed mission"
        )

    cat = db.query(SpyCat).filter(SpyCat.id == assign_data.cat_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Spy cat with id {assign_data.cat_id} not found"
    )

    existing_mission = db.query(Mission).filter(
        Mission.cat_id == assign_data.cat_id,
        Mission.id != mission_id
    ).first()
    if existing_mission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Spy cat with id {assign_data.cat_id} already has an active mission"
        )

    mission.cat_id = assign_data.cat_id
    db.commit()
    db.refresh(mission)
    return mission

