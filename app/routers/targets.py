from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Target, Mission
from app.schemas import TargetUpdate, TargetResponse

router = APIRouter(prefix="/targets", tags=["Targets"])


def check_all_targets_complete(db: Session, mission: Mission) -> bool:
    return all(target.complete for target in mission.targets)


@router.patch("/{target_id}", response_model=TargetResponse)
def update_target(target_id: int, target_data: TargetUpdate, db: Session = Depends(get_db)):
    target = db.query(Target).filter(Target.id == target_id).first()
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target with id {target_id} not found"
        )

    mission = db.query(Mission).filter(Mission.id == target.mission_id).first()

    if target_data.notes is not None:
        if target.complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update notes on a completed target"
            )
        if mission.complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update notes on a target belonging to a completed mission"
            )
        target.notes = target_data.notes

    if target_data.complete is not None:
        if target_data.complete and target.complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Target is already complete"
            )
        if not target_data.complete and target.complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot mark a completed target as incomplete"
            )
        target.complete = target_data.complete

    db.commit()
    db.refresh(target)

    db.refresh(mission)
    if check_all_targets_complete(db, mission):
        mission.complete = True
        db.commit()

    return target

