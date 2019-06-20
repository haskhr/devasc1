#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way.
"""

from flask import Flask, render_template, request
from logging import DEBUG
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


# Create Flask object and set logging level to assist with debugging/learning
app = Flask(__name__)
app.logger.setLevel(DEBUG)

# Toggle between db.json, db.yml, and db.xml
path = "data/db.xml"
db = Database(path)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    This is a view function which responds to requests for the top-level
    URL. It serves as the "controller" in MVC as it accesses both the
    model and the view.
    """

    # The button click within the view kicks off a POST request ...
    if request.method == "POST":

        # This collects the user input from the view. The controller's job
        # is to process this information, which includes using methods from
        # the "model" to get the information we need (in this case,
        # the account balance).
        acct_id = request.form["acctid"]
        acct_balance = db.balance(acct_id)
        app.logger.debug(f"balance for {acct_id}: {acct_balance}")
    else:
        # During a normal GET request, no need to perform any calculations
        acct_balance = None

    # This is the "view", which is the jinja2 templated HTML data that is
    # presented to the user. The user interacts with this webpage and
    # provides information that the controller then processes.
    # The controller passes the account balance into the view so it can
    # be displayed back to the user.
    return render_template("index.html", acct_balance=acct_balance)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
