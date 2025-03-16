from typing import Optional

from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    name: str
    department: str
    lottery_eligibility: str
    employee_id: str
    is_won: Optional[bool] = False
    is_donated: Optional[bool] = False


class EmployeeResponse(EmployeeCreate):
    id: int
