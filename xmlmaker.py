#!/usr/bin/env python3
'''
module borrowed from xxx
'''

from xml.dom.minidom import getDOMImplementation


def makeDoc(form_name=None):
    # Create the DOM
    impl = getDOMImplementation()
    dt = impl.createDocumentType("rms_express_form", None, 'rms_express_form.dtd')
    #dt = impl.createDocumentType(None, None, 'super_special.dtd')
    doc = impl.createDocument(None, form_name, dt)
    # return dt
    return doc


def makeQuery(doc, query_params, tag=None):
    """
        @doc is an xml.minidom.Document object
        @query_params is a dictionary structure that mirrors the structure of the xml.
        @tag used in recursion to keep track of the node to append things to next time through.

    """

    if tag is None:
        root = doc.documentElement
    else:
        root = tag

    for key, value in query_params.items():
        tag = doc.createElement(key)
        root.appendChild(tag)
        if isinstance(value, dict):
            makeQuery(doc, value, tag)
        else:
            root.appendChild(tag)
            tag_txt = doc.createTextNode(value)
            tag.appendChild(tag_txt)

    return doc.toxml()
