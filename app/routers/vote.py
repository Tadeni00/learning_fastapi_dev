from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from typing import List, Optional
from httpx import post
from sqlalchemy.orm import Session
from .. import model, schema, oauth2
from ..database import get_db


router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schema.Vote,
    db: Session = Depends(get_db),
    get_current_user=Depends(oauth2.get_current_user),
):

    post_query = (
        db.query(model.PostModel).filter(model.PostModel.id == vote.post_id).first()
    )
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {vote.post_id} does not exist",
        )
    vote_query = db.query(model.VotesModel).filter(
        model.VotesModel.post_id == vote.post_id,
        model.VotesModel.user_id == get_current_user.id,
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {get_current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = model.VotesModel(post_id=vote.post_id, user_id=get_current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote not found for user {get_current_user.id} on post {vote.post_id}",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}
