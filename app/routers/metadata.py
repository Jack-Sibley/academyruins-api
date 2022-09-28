from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import operations as ops
from ..database.db import get_db
from ..database.models import Mtr, Ipg

router = APIRouter(include_in_schema=False)


@router.get("/cr")
async def cr_metadata(db: Session = Depends(get_db)):
    meta = ops.get_cr_metadata(db)

    if meta:
        ret = [{"creation_day": d, "set_code": c, "set_name": n} for d, c, n in meta]
    else:
        ret = []

    return {"data": ret}


@router.get("/cr-diffs")
async def cr_diff_metadata(db: Session = Depends(get_db)):
    meta = ops.get_cr_diff_metadata(db)

    if meta:
        ret = [
            {"creation_day": d, "source_code": sc, "dest_code": dc, "dest_name": n, "bulletin_url": b}
            for d, sc, dc, n, b in meta
        ]
    else:
        ret = []

    return {"data": ret}


def format_creation_days(meta: list | None):
    if meta:
        return [{"creation_day": day} for day in meta]
    else:
        return []


@router.get("/mtr")
async def mtr_metadata(db: Session = Depends(get_db)):
    meta = ops.get_creation_dates(db, Mtr)
    return {"data": meta}


@router.get("/ipg")
async def mtr_metadata(db: Session = Depends(get_db)):
    meta = ops.get_creation_dates(db, Ipg)
    return {"data": meta}
