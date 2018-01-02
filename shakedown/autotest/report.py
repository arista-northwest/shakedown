
import json
import os
import codecs
from datetime import datetime
from getpass import getuser

from collections import OrderedDict
from shakedown.util import mkdir

styles = [
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

    def append(self, style, content):
        if style not in styles:
            raise ValueError("Unrecognized item style '{}'".format(style))

        self.items.append({"style": style, "content": content})

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
            fh.write(self.to_json())

    def get_section(self, section_id):

        if section_id not in self._sections:
            self._sections[section_id] = ReportSection()

        return self._sections[section_id]

    def to_json(self, indent=2, separators=(',', ': ')):

        result = OrderedDict(heading=self.heading)
        result["sections"] = []

        for section_id, section in self._sections.items():
            section = section.to_dict()
            section["id"] = section_id
            result["sections"].append(section)

        return json.dumps(result, indent=indent, separators=separators)

report_store = {}
