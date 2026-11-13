
import re
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.auth.dependencies import get_current_user
from src.database.models import User
from src.database.database import get_db
from src.database.models import Organisation, User
from src.auth.schemas import OrganisationRegister, UserLogin
from src.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register_organisation(
    request: OrganisationRegister,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered."
        )

    slug_base = re.sub(
        r"[^a-z0-9]+",
        "-",
        request.organisation_name.lower()
    ).strip("-")

    slug = f"{slug_base}-{uuid4().hex[:8]}"

    try:
        organisation = Organisation(
            name=request.organisation_name,
            slug=slug
        )

        db.add(organisation)
        db.flush()

        user = User(
            name=request.name,
            email=request.email,
            hashed_password=hash_password(request.password),
            role="admin",
            organisation_id=organisation.id
        )

        db.add(user)
        db.commit()

        db.refresh(user)

        token = create_access_token({
            "sub": str(user.id),
            "organisation_id": organisation.id,
            "role": user.role
        })

        return {
            "message": "Organisation registered successfully.",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "organisation_id": user.organisation_id,
                "role": user.role
            }
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Registration conflict. Please try again."
        )

    except Exception:
        db.rollback()
        raise


@router.post("/login")
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user or not verify_password(
        request.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive."
        )

    token = create_access_token({
        "sub": str(user.id),
        "organisation_id": user.organisation_id,
        "role": user.role
    })

    return {
        "message": "Login successful.",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "organisation_id": user.organisation_id,
            "role": user.role
        }
    }
@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "organisation_id": current_user.organisation_id,
        "role": current_user.role
    }