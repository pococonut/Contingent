from fastapi import Depends, APIRouter, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data_to_table
from db.structure_commands import get_structures_data, change_structure
from helpers.dicts import structure_models_dict
from models.structure.direction import DirectionData
from models.structure.department import DepartmentData
from models.structure.fgos import FgosData
from models.structure.group import GroupData
from models.structure.profile import ProfileData
from models.structure.subgroup import SubgroupData
from schemas.structure.direction import DirectionSh
from schemas.structure.department import DepartmentSh
from schemas.structure.group import GroupSh
from schemas.structure.profile import ProfileSh
from schemas.structure.subgroup import SubgroupSh
from schemas.structure.fgos import FgosSh

router = APIRouter()


@router.post("/direction", tags=['structure'])
async def post_direction(direction: DirectionSh,
                         db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, direction, DirectionData)
    return {"Successfully added": direction}


@router.post("/department", tags=['structure'])
async def post_department(department: DepartmentSh,
                          db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, department, DepartmentData)
    return {"Successfully added": department}


@router.post("/profile", tags=['structure'])
async def post_profile(profile: ProfileSh,
                       db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, profile, ProfileData)
    return {"Successfully added": profile}


@router.post("/fgos", tags=['structure'])
async def post_profile(fgos: FgosSh,
                       db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, fgos, FgosData)
    return {"Successfully added": fgos}


@router.post("/group", tags=['structure'])
async def post_group(group: GroupSh,
                     db: AsyncSession = Depends(get_db)):
    data = jsonable_encoder(group)
    list_of_groups = data.get('name')

    for gr in list_of_groups:
        data['name'] = gr
        await add_data_to_table(db, data, GroupData)

    return {"Successfully added": group}


@router.post("/subgroup", tags=['structure'])
async def post_subgroup(subgroup: SubgroupSh,
                        db: AsyncSession = Depends(get_db)):
    data = jsonable_encoder(subgroup)
    list_of_subgroups = data.get('name')

    for sgr in list_of_subgroups:
        data['name'] = sgr
        await add_data_to_table(db, data, SubgroupData)

    return {"Successfully added": subgroup}


@router.get("/structures", tags=['structure'])
async def get_structures(db: AsyncSession = Depends(get_db)):
    data = await get_structures_data(db)
    return data


@router.patch("/change_structure", tags=['structure'])
async def change_student_card(structure_id: int = None,
                              table_name: str = Query(enum=list(structure_models_dict.keys())),
                              parameters: dict = None,
                              db: AsyncSession = Depends(get_db)):

    data = {"structure_id": structure_id,
            "table_name": table_name,
            "parameters": parameters}

    updated_data = await change_structure(db, data)
    return updated_data

