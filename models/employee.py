from typing import List, Optional

from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    id: Optional[int] = None
    name: str
    group: str
    department: str
    lottery_eligibility: str
    employee_id: str
    is_won: Optional[bool] = False
    is_donated: Optional[bool] = False


class EmployeeResponse(EmployeeCreate):
    id: int


class Winner(BaseModel):
    id: int
    name: str
    group: str
    department: str
    employee_id: str
    is_won: Optional[bool] = True
    is_donated: Optional[bool] = False


class WinnersList(BaseModel):
    winners: List[Winner]
