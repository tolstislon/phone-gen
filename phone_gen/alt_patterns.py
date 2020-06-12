# -*- coding: utf-8 -*-
"""
Countries that are not in libphonenumber but are sometimes found
"""

ALT_PATTERNS = {
    "GS": {"code": "970", "pattern": "(082[014-68][\\d]{5})", "ref": "PS"},
    "WB": {"code": "970", "pattern": "(092[3569][\\d]{5})", "ref": "PS"},
    "NY": {"code": "90", "pattern": "(392[\\d]{7})", "ref": "TR"},
    "AQ": {"code": "672", "ref": "NF"},
    "GJ": {"code": "590", "ref": "GP"},
    "MI": {"code": "808", "pattern": "([1-9][\\d]{7})"},
    "AN": {"code": "599", "ref": "CW"},
}
