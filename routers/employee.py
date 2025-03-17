import pandas as pd
from fastapi import APIRouter, Body, HTTPException, UploadFile, status
from sqlalchemy import and_, insert

from database import database, employee_table
from models.employee import EmployeeResponse, WinnersList

router = APIRouter()

"""
# Batch create employees
# POST /api/v1/batch-create-employees
# Request Body: EXCEL file with columns name, department, lottery_eligibility, employee_id, is_won, is_donated
"""


@router.post(
    "/batch-create-employees", response_model=str, status_code=status.HTTP_201_CREATED
)
async def batch_create_employees(file: UploadFile):
    # Read the uploaded EXCEL file
    try:
        df = pd.read_excel(file.file)
        print("==df==", df.head(10))
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to process the uploaded file: {str(e)}"
        )

    # Check if the required columns are present
    required_columns = {
        "name",
        "department",
        "employee_id",
        "lottery_eligibility",
        "group",
    }

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns. Required: {required_columns}",
        )

    # Read the EXCEL file and create a list of employee data
    employees = []
    for _, row in df.iterrows():
        employee_data = {
            "name": row["name"],
            "department": row["department"],
            "lottery_eligibility": row["lottery_eligibility"],
            "employee_id": row["employee_id"],
            "group": row["group"],
            "is_won": False,
            "is_donated": False,
            "prize": None,
        }
        employees.append(employee_data)

    # Insert the employee data into the database
    query = insert(employee_table).values(employees)
    await database.execute(query)

    return "Batch employees data insert successfully"


"""
# Get employees by group one
# GET /api/v1/get-employees-by-group-one
# Response: List of employees in group one (group = 1)
"""


@router.get("/get-employees-by-group-one", response_model=list[EmployeeResponse])
async def get_employees_by_group_one():
    query = employee_table.select().where(
        and_(employee_table.c.group == "1", employee_table.c.is_won == "0")
    )
    results = await database.fetch_all(query)
    return results


"""
# Get employees by group two
# GET /api/v1/get-employees-by-group-two
# Response: List of employees in group two (group = 2)
"""


@router.get("/get-employees-by-group-two", response_model=list[EmployeeResponse])
async def get_employees_by_group_two():
    query = employee_table.select().where(
        and_(employee_table.c.group == "2", employee_table.c.is_won == "0")
    )
    results = await database.fetch_all(query)
    return results


"""
# Get employees by group three
# GET /api/v1/get-employees-by-group-three
# Response: List of employees in group two (group = 3)
"""


@router.get("/get-employees-by-group-three", response_model=list[EmployeeResponse])
async def get_employees_by_group_three():
    query = employee_table.select().where(
        and_(employee_table.c.group == "3", employee_table.c.is_won == "0")
    )
    results = await database.fetch_all(query)
    return results


"""
# Get employees by all group but zero
# GET /api/v1/get-employees-by-all-group
# Response: List of employees in group two (group != 0)
"""


@router.get("/get-employees-by-all-groups", response_model=list[EmployeeResponse])
async def get_employees_by_all_groups():
    query = employee_table.select().where(
        and_(employee_table.c.group != "0", employee_table.c.is_won == "0")
    )
    results = await database.fetch_all(query)
    return results


"""
# Add winners to the database
# POST /api/v1/add-winners
# Request Body: List of winners
"""


@router.post("/add-winners", response_model=dict)
async def add_winners(winners_data: WinnersList = Body(...)):
    if not winners_data.winners:
        raise HTTPException(status_code=400, detail="Winners list cannot be empty")

    winner_updates = []
    for winner in winners_data.winners:
        winner_updates.append(
            {
                "id": winner.id,
                "is_won": True,
                "prize": winner.prize,
                "is_donated": winner.is_donated
                if winner.is_donated is not None
                else False,
            }
        )

    if not winner_updates:
        raise HTTPException(status_code=400, detail="No valid winner data provided")

    for winner in winner_updates:
        query = (
            employee_table.update()
            .where(employee_table.c.id == winner["id"])
            .values(
                is_won=winner["is_won"],
                is_donated=winner["is_donated"],
                prize=winner["prize"],
            )
        )
        await database.execute(query)

    return {"message": f"成功更新 {len(winner_updates)} 位員工為中獎（包含棄權資訊）"}
