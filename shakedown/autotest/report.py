
import json
import os
import codecs
from datetime import datetime
from getpass import getuser

from collections import OrderedDict
from shakedown.util import mkdir

item_kinds = [
    "h1",
    "h2",
    "h3",
    "h4",
    "text",
    "codeblock",
    "link",
    "image"
]

outcomes = [
    "passed",
    "failed",
    "skipped",
    "errored",
    "unknown"
]

class ReportSection:
    def __init__(self):
        self.description = None
        self.items = []

        self._outcome = None

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        if not value in outcomes:
            raise ValueError("Invalid outcome '{}'".format(value))

        self._outcome = value

    def append(self, kind, content):
        if kind not in item_kinds:
            raise ValueError("Unrecognized item kind '{}'".format(kind))

        self.items.append({"format": kind, "content": content})

    def to_dict(self):
        return {
            "description": self.description,
            "outcome": self.outcome,
            "items": self.items,
        }

class Report:

    def __init__(self, title, description):

        self.heading = {
            "title": title,
            "description": description,
            "created_at": str(datetime.utcnow()),
            "created_by": getuser()
        }

        self._sections = OrderedDict()

    def save(self, path):
        path = os.path.expanduser(path)
        mkdir(os.path.dirname(path))
        with codecs.open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_json(), fh, indent=2, separators=(',', ': '))

    def get_section(self, section_id):

        if section_id not in self._sections:
            self._sections[section_id] = ReportSection()

        return self._sections[section_id]

    def to_json(self):

        result = OrderedDict(heading=self.heading)
        result["sections"] = []

        for sid, section in self._sections.items():
            section = section.to_dict()
            section["id"] = sid
            result["sections"].append(section)

        return result

report_store = {}
