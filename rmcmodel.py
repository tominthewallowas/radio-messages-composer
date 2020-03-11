from PyQt5.QtWidgets import (QLineEdit,)
from xmlmaker import makeDoc, makeQuery

CR = '\r'
LF = '\n'
CRLF = '\r\n'


class RMCModel:
    def __init__(self, view):
        self._view = view
        self._configuration = view._configuration

    def _getFieldData(self):
        field_data = {}
        fields = self._view._centralwidget.findChildren(QLineEdit)
        for field in fields:
            field_data[field.objectName()] = field.text()
        return field_data

    def _createTextMessage(self, field_data):
        text_message = ''
        for template_item in self._view._current_print_template:
            if '$$' in template_item:
                if template_item[2:] == 'CR':
                    text_message += CR
                else:
                    text_message += field_data[template_item[2:]]
            else:
                text_message += template_item
        return text_message

    def _createXMLMessage(self, field_data):
        paired_data = {}
        doc = makeDoc(self._view._current_xml_template['formname'])
        for key, value in field_data.items():
            paired_data[self._view._current_xml_template[key]] = value
        qxml = makeQuery(doc, paired_data)
        return qxml
