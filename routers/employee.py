import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, status
from sqlalchemy import insert

from database import database, employee_table
from models.employee import EmployeeResponse

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
        "lottery_eligibility",
        "employee_id",
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
        }
        employees.append(employee_data)

    # Insert the employee data into the database
    query = insert(employee_table).values(employees)
    await database.execute(query)

    return "Batch employees data insert successfully"


@router.get("/getEmployeesByGroupOne", response_model=list[EmployeeResponse])
async def getEmployeesByGroupOne():
    query = employee_table.select().where(employee_table.c.group == "1")
    results = await database.fetch_all(query)
    return results
