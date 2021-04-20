import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import settings
from auth import check_admin_authentication_header
import controller
from database import get_session
import schemas
import cache
import models
import database


app = FastAPI(
    title="Controller",
    description="",
)


@app.on_event('startup')
async def startup_event():
    await cache.init_cache()


@app.on_event('shutdown')
async def shutdown_event():
    await cache.connection.close()
    await cache.connection.wait_closed()


@app.post('/marks')
async def receive_mark(mark: schemas.MarkCreate):

    last_command_datetime = await cache.connection.get(controller.last_command_datetime_key)
    if last_command_datetime is None:

        with database.context_session() as db:
            last_command_datetime = db.query(
                models.Command.datetime
            ).order_by(
                models.Command.datetime.desc()
            ).limit(1).scalar()

        if last_command_datetime is None:
            last_command_datetime = datetime.datetime.min

    else:
        last_command_datetime = datetime.datetime.fromisoformat(last_command_datetime)

    if mark.datetime < last_command_datetime:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail='Outdated mark.')

    await cache.connection.publish_json('marks', jsonable_encoder(mark))

    return mark


@app.get('/commands', dependencies=[Depends(check_admin_authentication_header)],
         response_model=List[schemas.Command])
def retrieve_command(take_last: int = Query(ge=1, default=1), db: Session = Depends(get_session)):
    commands = db.query(models.Command).order_by(models.Command.id.desc()).limit(take_last).all()
    return commands
