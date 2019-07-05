#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A test  case file for the Database class (Model in MVC).
Used to illustrate Test Driven Development (TDD) and DevOps CI/CD.
"""

import pytest
import database


@pytest.fixture
def db_mock():
    """
    Test fixture setup to create sample database from "model" data.
    """
    return database.Database("data/db.json")


def test_balance(db_mock):
    """
    Test the "balance()" method.
    """
    assert db_mock.balance("ACCT100") == 40
    assert db_mock.balance("ACCT200") == -10
    assert db_mock.balance("ACCT300") == 0


def test_owes_money(db_mock):
    """
    Test the "owes_money()" method.
    """
    assert db_mock.owes_money("ACCT100")
    assert not db_mock.owes_money("ACCT200")
    assert not db_mock.owes_money("ACCT300")
