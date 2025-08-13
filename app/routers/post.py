from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import model, schema, oauth2
from ..database import engine, get_db
from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[schema.PostResponse])
def get_post(
    db: Session = Depends(get_db),
    get_current_user=Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = (
        db.query(model.PostModel, func.count(model.VotesModel.post_id).label("votes"))
        .join(
            model.VotesModel,
            model.PostModel.id == model.VotesModel.post_id,
            isouter=True,
        )
        .filter(model.PostModel.title.ilike(f"%{search}%"))
        .group_by(model.PostModel.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    # Convert tuples to dicts for Pydantic
    return [{"Post": post, "votes": votes} for post, votes in posts]


@router.post("/", response_model=schema.Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schema.CreatePost,
    db: Session = Depends(get_db),
    get_current_user=Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published)
    #                   VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = model.PostModel(user_id=get_current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schema.PostResponse)
def get_one_post(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    get_current_user=Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    # post = db.query(model.PostModel).filter(model.PostModel.id == id).first()
    
    post = (
        db.query(model.PostModel, func.count(model.VotesModel.post_id).label("votes"))
        .join(
            model.VotesModel,
            model.PostModel.id == model.VotesModel.post_id,
            isouter=True,
        )).filter(model.PostModel.id == id).group_by(model.PostModel.id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    # if post.user_id != get_current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action"
    #     )

    post, votes = post
    return {"Post": post, "votes": votes}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: model.UserModel = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(model.PostModel).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(
    id: int,
    post: schema.UpdatePost,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s
    #                   WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(model.PostModel).filter(model.PostModel.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    post_query.update(
        {getattr(model.PostModel, key): value for key, value in post.dict().items()},
        synchronize_session=False,
    )
    db.commit()
    return post_query.first()
