import json
import os
import codecs
from datetime import datetime
from getpass import getuser
from functools import partial
from collections import OrderedDict
from shakedown.util import mkdir

styles = ["h1", "h2", "h3", "h4", "text", "codeblock", "link", "image"]

outcomes = ["passed", "failed", "skipped", "errored", "unknown"]


class ReportSection:
    def __init__(self):
        self.description = None
        self.elements = []
        self.traceback = None
        self._outcome = None

    def __getattr__(self, name):
        # shortcut for appending elements by style
        if name in styles:
            return partial(self.append, name)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                self.__class__.__name__, name))

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        if not value in outcomes:
            raise ValueError("Invalid outcome '{}'".format(value))

        self._outcome = value

    def append(self, style, content, **kwargs):
        if style not in styles:
            raise ValueError("Unrecognized item style '{}'".format(style))

        self.elements.append({
            "style": style,
            "content": str(content),
            "keywords": kwargs
        })

    def to_dict(self):
        return {
            "description": self.description,
            "outcome": self.outcome,
            "elements": self.elements,
            "traceback": str(self.traceback) if self.traceback else None
        }


class Report:
    def __init__(self, name, title, description):

        self.heading = {
            "name": name,
            "title": title,
            "description": description,
            "created_at": str(datetime.utcnow()),
            "created_by": getuser()
        }

        self._sections = OrderedDict()

    def get_section(self, section_id):

        if section_id not in self._sections:
            self._sections[section_id] = ReportSection()

        return self._sections[section_id]

    def to_dict(self):

        result = OrderedDict(self.heading)
        result["sections"] = []

        for section_id, section in self._sections.items():
            section = section.to_dict()
            section["id"] = section_id
            result["sections"].append(section)

        return result


report_store = {}
