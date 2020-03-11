#!/usr/bin/env python3

# Filename: winlink-messages.py

"""
   Radio Messages Composer allows filling out a form and then creating a formatted message
   for copy and paste into an email window.  In addition, it will create and xml file with
   the same information.  This is a workaround for the pat winlink email client to mimic
   what WinLink Express does with message forms.
"""

import sys
import yaml
from rmcmodel import RMCModel
from rmccontroller import RMCController

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QVBoxLayout, QFormLayout,
                             QWidget, QComboBox,)

__version__ = '0.1'
__author__ = 'Tom Bingham'

# Global constant to handle errors
ERROR_MSG = 'ERROR'


class RMCUi(QMainWindow):
    """Radio Messages Composer View (GUI)."""

    def __init__(self):
        """View initializer"""
        super().__init__()
        self.setWindowTitle('Radio Messages Controller')
        self.setFixedSize(235, 200)
        self.generalLayout = QVBoxLayout()
        self._centralwidget = QWidget(self)
        self.setCentralWidget(self._centralwidget)
        self._centralwidget.setLayout(self.generalLayout)
        self._configuration = self._loadConfiguration('rmcconfig.yaml')
        self._createSelectionCombo(self._configuration['forms'])
        self._createForm()
        self._createButtonBar(self._configuration['buttons'])
        self._current_print_template = []
        self._current_xml_template = {}

    def _loadConfiguration(self, yaml_file=None):
        if not yaml_file:
            return None
        config_data = None
        with open(yaml_file) as f:
            #config_data = yaml.load(f)
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        return config_data

    def _createSelectionCombo(self, forms=None):
        cmb = QComboBox(self._centralwidget)
        cmb.setObjectName('cmbForm')
        items = []
        for key, value in forms.items():
            items.append(value['selection'])
        cmb.addItems(items)
        self.generalLayout.addWidget(cmb)

    def _createForm(self):
        self._frmLayout = QFormLayout()
        self._frmLayout.setObjectName('frmLayout')
        self.generalLayout.addLayout(self._frmLayout)

    def _createButtonBar(self, buttons):
        buttonLayout = QHBoxLayout()
        for label, button_name in buttons.items():
            button = QPushButton(label, self._centralwidget)
            button.setObjectName(button_name)
            buttonLayout.addWidget(button)
        self.generalLayout.addLayout(buttonLayout)


def main():
    """Main function."""
    rmc = QApplication(sys.argv)
    view = RMCUi()
    view.show()
    model = RMCModel(view)
    RMCController(model=model, view=view)
    sys.exit(rmc.exec())


if __name__ == '__main__':
    main()
