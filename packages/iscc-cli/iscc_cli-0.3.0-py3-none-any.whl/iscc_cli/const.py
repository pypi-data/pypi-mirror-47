# -*- coding: utf-8 -*-
from iscc import const


class GMT:
    """Generic Media Type"""

    IMAGE = "image"
    TEXT = "text"


SUPPORTED_MIME_TYPES = {
    "application/rtf": {"gmt": GMT.TEXT, "ext": "rtf"},
    "application/msword": {"gmt": GMT.TEXT, "ext": "doc"},
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "gmt": GMT.TEXT,
        "ext": "docx",
    },
    "image/jpeg": {"gmt": GMT.IMAGE, "ext": "jpg"},
    "image/png": {"gmt": GMT.IMAGE, "ext": "png"},
    "application/pdf": {"gmt": GMT.TEXT, "ext": "pdf"},
    "application/epub+zip": {"gmt": GMT.TEXT, "ext": "epub"},
}


SUPPORTED_EXTENSIONS = [value["ext"] for _, value in SUPPORTED_MIME_TYPES.items()]


ISCC_COMPONENT_TYPES = {
    const.HEAD_MID: {"name": "Meta-ID", "code": "CC"},
    const.HEAD_CID_T: {"name": "Content-ID Text", "code": "CT"},
    const.HEAD_CID_T_PCF: {"name": "Content-ID Text", "code": "Ct"},
    const.HEAD_CID_I: {"name": "Content-ID Image", "code": "CY"},
    const.HEAD_CID_I_PCF: {"name": "Content-ID Image", "code": "Ci"},
    const.HEAD_CID_A: {"name": "Content-ID Audio", "code": "CA"},
    const.HEAD_CID_A_PCF: {"name": "Content-ID Audio", "code": "Ca"},
    const.HEAD_CID_V: {"name": "Content-ID Video", "code": "CV"},
    const.HEAD_CID_V_PCF: {"name": "Content-ID Video", "code": "Cv"},
    const.HEAD_CID_M: {"name": "Content-ID Mixed", "code": "CM"},
    const.HEAD_CID_M_PCF: {"name": "Content-ID Mixed", "code": "Cm"},
    const.HEAD_DID: {"name": "Data-ID", "code": "CD"},
    const.HEAD_IID: {"name": "Instance-ID", "code": "CR"},
}

ISCC_COMPONENT_CODES = {
    value["code"]: {"name": value["name"], "marker": key}
    for key, value in ISCC_COMPONENT_TYPES.items()
}
