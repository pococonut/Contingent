from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data_to_table, get_table_data
from models.structure.direction import DirectionData
from models.structure.department import DepartmentData
from models.structure.group import GroupData
from models.structure.profile import ProfileData
from models.structure.subgroup import SubgroupData
from schemas.structure.direction import DirectionSh
from schemas.structure.department import DepartmentSh
from schemas.structure.group import GroupSh
from schemas.structure.profile import ProfileSh
from schemas.structure.subgroup import SubgroupSh

router = APIRouter()


@router.post("/direction")
async def post(direction: DirectionSh,
               db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, direction, DirectionData)
    return {"Successfully added": direction}


@router.post("/department")
async def post(department: DepartmentSh,
               db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, department, DepartmentData)
    return {"Successfully added": department}


@router.post("/profile")
async def post(profile: ProfileSh,
               db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, profile, ProfileData)
    return {"Successfully added": profile}


@router.post("/group")
async def post(group: GroupSh,
               db: AsyncSession = Depends(get_db)):
    data = jsonable_encoder(group)
    list_of_groups = data.get('group')

    for gr in list_of_groups:
        data['group'] = gr
        await add_data_to_table(db, data, GroupData)

    return {"Successfully added": group}


@router.post("/subgroup")
async def post(subgroup: SubgroupSh,
               db: AsyncSession = Depends(get_db)):
    data = jsonable_encoder(subgroup)
    list_of_subgroups = data.get('subgroup')

    for sgr in list_of_subgroups:
        data['subgroup'] = sgr
        await add_data_to_table(db, data, SubgroupData)

    return {"Successfully added": subgroup}
