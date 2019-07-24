class Mediator:
    """
    Design Pattern: Mediator.
    """
    def __init__(self):
        self.checks = {}
        self.buttons = {}

    def update(self, sender, state):
        """
        :param sender: text of sender button
        :param state: 0 means "uncheck", 2 means "check"
        :return: nothing, just change states of checkboxes, buttons and text fields
        """
        if sender == "Run Python" and self.checks["Run Cython"].isChecked() and state == 2:
            self.checks["Run Both"].setChecked(True)
        if sender == "Run Python" and self.checks["Run Cython"].isChecked() and state == 0:
            self.checks["Run Both"].setChecked(False)
            self.checks["Run Cython"].setChecked(True)

        if sender == "Run Cython" and self.checks["Run Python"].isChecked() and state == 2:
            self.checks["Run Both"].setChecked(True)
        if sender == "Run Cython" and self.checks["Run Python"].isChecked() and state == 0:
            self.checks["Run Both"].setChecked(False)
            self.checks["Run Python"].setChecked(True)

        if sender == "Run Both" and state == 2:
            self.checks["Run Cython"].setChecked(True)
            self.checks["Run Python"].setChecked(True)
        if sender == "Run Both" and state == 0:
            self.checks["Run Cython"].setChecked(False)
            self.checks["Run Python"].setChecked(False)

        if self.checks["Run Python"].isChecked():
            self.buttons["Browse (.py)"][0].setEnabled(True)
            self.buttons["Browse (.py)"][1].setEnabled(True)
        else:
            self.buttons["Browse (.py)"][0].setEnabled(False)
            self.buttons["Browse (.py)"][1].setEnabled(False)

        if self.checks["Run Cython"].isChecked():
            self.buttons["Browse (.pyd)"][0].setEnabled(True)
            self.buttons["Browse (.pyd)"][1].setEnabled(True)
        else:
            self.buttons["Browse (.pyd)"][0].setEnabled(False)
            self.buttons["Browse (.pyd)"][1].setEnabled(False)
