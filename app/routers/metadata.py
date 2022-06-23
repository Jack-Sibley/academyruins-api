from fastapi import APIRouter
from ..utils import db
from ..utils.responses import StatusResponse

router = APIRouter()


@router.get('/cr')
async def cr_metadata():
    meta = await db.fetch_cr_metadata()
    if not meta:
        meta = []

    for row in meta:
        row['creation_day'] = row['creation_day'].isoformat()
    return StatusResponse({'data': meta})


@router.get('/cr-diffs')
async def cr_diff_metadata():
    meta = await db.fetch_cr_diff_metadata()
    if not meta:
        meta = []
    for row in meta:
        row['creation_day'] = row['creation_day'].isoformat()
    return StatusResponse({'data': meta})


@router.get('/mtr')
async def mtr_metadata():
    meta = await db.fetch_mtr_metadata()
    if not meta:
        meta = []
    for row in meta:
        row['creation_day'] = row['creation_day'].isoformat()
    return StatusResponse({'data': meta})


@router.get('/ipg')
async def mtr_metadata():
    meta = await db.fetch_ipg_metadata()
    if not meta:
        meta = []
    for row in meta:
        row['creation_day'] = row['creation_day'].isoformat()
    return StatusResponse({'data': meta})
