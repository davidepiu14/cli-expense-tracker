"""This module provides the ET expense model-controller."""

import datetime

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from tracker import DB_READ_ERROR, ID_ERROR
from tracker.database import DatabaseHandler


class CurrentExpense(NamedTuple):
    expense: Dict[str, Any]
    error: int

class Expense:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], amount: float=0.0) -> CurrentExpense:
        """Add new expense to the database."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        expense = {
                "Description": description_text,
                "Amount": amount,
                "Date": str(datetime.date.today()),
                "Done": False
        }
        read = self._db_handler.read_expense()
        if read.error == DB_READ_ERROR: 
            return CurrentExpense(expense, read.error)
        read.expense_list.append(expense)
        write = self._db_handler.write_expense(read.expense_list)
        return CurrentExpense(expense, write.error)

    def get_expense_list(self) -> List[Dict[str, Any]]:
        """Return the current expense list."""
        read = self._db_handler.read_expense()
        return read.expense_list
    
    def set_done(self, expense_id: int) -> CurrentExpense:
        """Set an expense as done."""
        read = self._db_handler.read_expense()
        if read.error:
            return CurrentExpense({}, read.error)
        try:
            expense = read.expense_list[expense_id - 1]
        except IndexError:
            return CurrentExpense({}, ID_ERROR)
        expense["Done"] = True
        write = self._db_handler.write_expense(read.expense_list)
        return CurrentExpense(expense, write.error)
    
    def remove(self, expense_id: int) -> CurrentExpense:
        """Remove an expense from the database using its id or index."""
        read = self._db_handler.read_expense()
        if read.error:
            return CurrentExpense({}, read.error)
        try:
            expense = read.expense_list.pop(expense_id - 1)
        except IndexError:
            return CurrentExpense({}, ID_ERROR)
        write = self._db_handler.write_expense(read.expense_list)
        return CurrentExpense(expense, write.error)
        
    def remove_all(self) -> CurrentExpense:
        """Remove all expenses from the database."""
        write = self._db_handler.write_expense([])
        return CurrentExpense({}, write.error)
        