from PyQt5.QtWidgets import (QPushButton, QLineEdit, QComboBox,
                             QDialog, QDialogButtonBox, QVBoxLayout,
                             QTextEdit, QWidget, QFileDialog,)
from PyQt5.QtCore import Qt
from functools import partial


class MessageDialog(QDialog):
    def __init__(self, parent=None):
        super(MessageDialog, self).__init__(parent)
        centralWidget = QWidget()
        self.messageText = QTextEdit()
        self.messageText.setText('Tom \nMessage \nBox')
        self.messageText.setReadOnly(True)
        self.copyButton = QPushButton("&Copy Message")
        self.copyButton.setDefault(True)
        self.copyButton.clicked.connect(self.copyText)
        cancelButton = QPushButton("C&ancel")
        cancelButton.clicked.connect(self.close)
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton(self.copyButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(cancelButton, QDialogButtonBox.ActionRole)
        messageLayout = QVBoxLayout()
        messageLayout.setContentsMargins(10, 10, 10, 10)
        messageLayout.addWidget(self.messageText)
        messageLayout.addWidget(buttonBox)
        centralWidget.setLayout(messageLayout)
        self.setLayout(messageLayout)
        self.setWindowTitle("WinLink Message")
        centralWidget.show()

    def copyText(self):
        self.messageText.selectAll()
        self.messageText.copy()
        self.close()


class RMCController:
    """Radio Messages Composer Controller class."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._model = model
        self._view = view
        self._connectSignals()
        # Force form combo index change event
        combo = self.__deriveFormCombo()

        combo.setCurrentIndex(1)
        combo.setCurrentIndex(0)

    def _connectSignals(self):
        buttons = self._view._centralwidget.findChildren(QPushButton)
        for button in buttons:
            button.clicked.connect(partial(self._handleButton, button.objectName()))
        combo = self.__deriveFormCombo()
        combo.currentIndexChanged[str].connect(self._handleComboBox)

    def _handleComboBox(self, text):
        forms = self._view._configuration['forms']
        for key, value in forms.items():
            if value['selection'] == text:
                self._createFormFields(value['form-fields'])
                self._view._current_print_template = value['print-template']
                self._view._current_xml_template = value['xml-template']
                self.populateTestFields(text)
                break

    def populateTestFields(self, text):
        if text == 'Name and Age':
            self._view._centralwidget.findChild(QLineEdit, 'leName').setText('Tom')
            self._view._centralwidget.findChild(QLineEdit, 'leAge').setText('69')
            self._view._centralwidget.findChild(QLineEdit, 'leJob').setText('Retired')
            self._view._centralwidget.findChild(QLineEdit, 'leHobbies').setText('Ham Radio')
        elif text == 'Cats':
            self._view._centralwidget.findChild(QLineEdit, 'leName').setText('Lilly')
            self._view._centralwidget.findChild(QLineEdit, 'leAge').setText('1')
            self._view._centralwidget.findChild(QLineEdit, 'leColor').setText('Black, Copper, White')

    def _createFormFields(self, field_names={}):
        # First delete all the rows
        self.__removeFormFields()
        for label, field_name in field_names.items():
            form_field = QLineEdit(self._view._centralwidget)
            form_field.setObjectName(field_name)
            self._view._frmLayout.addRow(label, form_field)

    def _handleButton(self, object_name):
        if object_name == 'btnClear':
            self._clearFields()
        elif object_name == 'btnQuit':
            self._view.close()
        elif object_name == "btnSubmit":
            self._submit()

    def _submit(self):
        field_data = self._model._getFieldData()
        text_message = self._model._createTextMessage(field_data)
        print(text_message)
        messageDialog = MessageDialog()
        messageDialog.messageText.setText(text_message)
        messageDialog.setModal(True)
        messageDialog.exec()
        messageDialog.show()
        xml_message = self._model._createXMLMessage(field_data)
        print(xml_message)
        # Save Dialog code goes here
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        suggested_file_name = self._view._current_xml_template['formname'] + '.xml'
        filename, _ = QFileDialog.getSaveFileName(None,
                                                  "Save XML File",
                                                  suggested_file_name,
                                                  "XML Files (*.xml);;All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if filename:
            self.__saveXMLFile(filename=filename, file_data=xml_message)

    def __saveXMLFile(self, filename=None, file_data=None):
        print(filename, file_data)
        f = open(filename, 'w')
        f.write(file_data)
        f.close()

    def _clearFields(self):
        fields = self._view._centralwidget.findChildren(QLineEdit)
        for field in fields:
            field.setText('')

    def __removeFormFields(self):
        row_count = self._view._frmLayout.rowCount()
        for index in reversed(range(row_count)):
            self._view._frmLayout.removeRow(index)

    def __deriveFormCombo(self):
        combos = self._view._centralwidget.findChildren(QComboBox)
        for combo in combos:
            if combo.objectName() == 'cmbForm':
                return combo

