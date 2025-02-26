from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.expense import Expense

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=Expense)
def create_expense(expense: Expense, session: Session = Depends(get_session)):
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


@router.get("/", response_model=list[Expense])
def get_expenses(session: Session = Depends(get_session)):
    expenses = session.exec(select(Expense)).all()
    return expenses


@router.get("/{expense_id}", response_model=Expense)
def get_expense(expense_id: int, session: Session = Depends(get_session)):
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, updated_expense: Expense, session: Session = Depends(get_session)):
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.work_assignment_id = updated_expense.work_assignment_id
    expense.expense_type = updated_expense.expense_type
    expense.estimated_cost = updated_expense.estimated_cost
    expense.actual_cost = updated_expense.actual_cost
    expense.date = updated_expense.date

    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, session: Session = Depends(get_session)):
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    session.delete(expense)
    session.commit()
    return {"message": "Expense deleted successfully"}
