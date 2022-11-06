# cli-expense-tracker

Simple CLI written in Python to track expenses

### Install 
Create python virtual enviroment:

1)    python3 -m venv venv
2)  . venv/bin/activate

### Usage 
```python -m [COMMAND] [OPTION]```

Options: 
```  
  -v, --version         Show the application's version and exit.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  add       Add a new expense with a DESCRIPTION.
  clear     Remove all expenses
  complete  Complete a expense by setting it as done useing its ID.
  init      Initialize the expense database.
  list      List all expenses.
  remove    Remove a expense using its EXPENSE_ID
```

