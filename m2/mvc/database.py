#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way.
"""

import json

# import yaml
# import xmltodict


class Database:
    """
    Represent the interface to the data (model). Can be statically defined
    data, read from a simple file such as JSON, YAML, or XML, or a more
    complex remote database including postgres and SQL-based options.
    """

    def __init__(self, path):
        """
        Constructor to initialize the data attribute as
        a dictionary where the account number is the key and
        the value is another dictionary with keys "paid" and "owes".
        """

        # Open the specified database file for reading and perform loading
        with open(path, "r") as handle:
            self.data = json.load(handle)

            # ALTERNATIVE IMPLEMENTATIONS: Using YAML or XML to load data
            # self.data = yaml.safe_load(handle)
            # self.data = xmltodict.parse(handle.read())["root"]

    def balance(self, acct_id):
        """
        Determines the customer balance by finding the difference between
        what has been paid and what is still owed on the account, The "model"
        can provide methods to help interface with the data; it is not
        limited to only storing data.
        """
        acct = self.data.get(acct_id)
        if acct:
            return int(acct["paid"]) - int(acct["owes"])
        return None

    def owes_money(self, acct_id):
        """
        Returns true if the account holder owes us money. Returns
        false if they are up to date on payments or have credit.
        """
        return self.balance(acct_id) < 0


def run_unit_tests():
    """
    Simple, un-frameworked unit testing to demonstrate test-driven development.
    Don't do it this way in real life! Focus on the logical flow, not the code.
    """
    # Build test database
    test_db = Database("data/db.json")

    # After-the-fact tests (not TDD, but still useful)
    assert test_db.balance("ACCT100") == 40
    assert test_db.balance("ACCT200") == -10

    # Real TDD tests for a method not yet implemented ...
    assert not test_db.owes_money("ACCT100")
    assert test_db.owes_money("ACCT200")

    print("All database tests passed!")


if __name__ == "__main__":
    run_unit_tests()
