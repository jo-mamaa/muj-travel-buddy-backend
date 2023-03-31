import uuid

from sqlalchemy.orm import Session

from . import models, schemas, utils


# Users CRUD
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(
        UID=user.UID,
        fname=user.fname,
        lname=user.lname,
        email=user.email,
        designation=user.designation,
        user_type=user.user_type,
        phone=user.phone,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.UID == user_id).first()


def create_ride(db: Session, ride: schemas.RideCreate, user_id: int):
    db_ride = models.Ride(**dict(ride), publisher_id=user_id)
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)

    return db_ride


# Rides CRUD
def get_all_rides(db: Session):
    db_rides = db.query(models.Ride).all()

    return db_rides


def get_ride_by_id(db: Session, ride_id: str):
    db_ride = db.query(models.Ride).filter(models.Ride.id == uuid.UUID(ride_id)).first()

    return db_ride


def get_rides_by_publisher_id(db: Session, publisher_id: int):
    return db.query(models.Ride).filter(models.Ride.publisher_id == publisher_id).all()


# Ride Requests CRUD
def create_ride_request(
    db: Session, ride_request: schemas.RideRequestCreate, requestee_id: int
):
    db_request = models.RideRequest(**dict(ride_request), requestee_id=requestee_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return db_request
