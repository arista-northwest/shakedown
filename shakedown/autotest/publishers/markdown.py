# -*- coding: utf-8 -*-
# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import jinja2
import os

TEMPLATE = """{{ heading.title }}
{{ "===" }}

{{ heading.description }}

{% for section in sections %}

{{ section.description|default("[No Description]") }}
{{ "---" }}

__Outcome__: {{ section.outcome }}

    {% for elem in section.elements %}
        {% if elem.style == "codeblock" %}
```
{{ elem.content }}
```
        {% elif elem.style == "link" %}
[{{ elem.keywords["text"]|default(elem.content) }}]({{ elem.content }} "{{ elem.keywords["title"]|default("") }}")
        {% elif elem.style == "image" %}
![{{ elem.keywords["text"]|default(elem.content) }}]({{ elem.content }} "{{ elem.keywords["title"]|default("") }}")
        {% elif elem.style == "h1" %}
# {{ elem.content }}
        {% elif elem.style == "h2" %}
## {{ elem.content }}
        {% elif elem.style == "h3" %}
### {{ elem.content }}
        {% elif elem.style == "h4" %}
#### {{ elem.content }}
        {% else %}
{{ elem.content }}
        {% endif %}

    {% endfor %}

    {% if section.traceback != None %}
__Traceback__
```
{{ section.traceback }}
```
    {% endif %}
{% endfor %}
"""

def render(data):
    j2_env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    template = j2_env.from_string(TEMPLATE)
    return template.render(data)

def save(data, path):
    path = os.path.join(path, "report.md")
    with open(path, "w") as fh:
        fh.write(render(data))
