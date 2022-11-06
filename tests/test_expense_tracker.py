# tests/test_expense.py

import json
from typer.testing import CliRunner
import pytest



from tracker import (
        DB_READ_ERROR,
        SUCCESS,
        __app_name__,
        __version__, 
        cli,
        tracker,
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert "%s v %s" % (__app_name__,__version__) in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{
        "Description": "some milk.",
        "amount": 2.0,
        "Done": False
        }]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

test_data1 = {
        "description": ["Clean", "the", "house"],
        "amount": 1.0,
        "todo": {
            "Description": "Clean the house.",
            "amount": 1.0,
            "Done": False,
            },
}

test_data2 = {
        "description" : ["Wash the car"],
        "amount": 2.0,
        "todo": {
            "Description": "Wash the car.",
            "amount": 2.0,
            "Done": False,
        },
}



@pytest.mark.parametrize(
        "description, amount, expected",
        [
            pytest.param(
                test_data1["description"],
                test_data1["amount"],
                (test_data1["expense"],SUCCESS),
                ),
            pytest.param(
                test_data2["description"],
                test_data2["amount"],
                (test_data2["todo"], SUCCESS),
                ),
        ],
)

def test_add(mock_json_file, description, amount, expected):
    expenser = tracker.Tracker(mock_json_file)
    assert expenser.add(description, amount) == expected
    read = expenser._db_handler.read_expense()
    assert len(read.todo_list) == 2


