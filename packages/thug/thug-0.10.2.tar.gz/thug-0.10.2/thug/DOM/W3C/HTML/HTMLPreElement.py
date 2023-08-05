#!/usr/bin/env python

from .HTMLElement import HTMLElement
from .attr_property import attr_property
from .compatibility import thug_long


class HTMLPreElement(HTMLElement):
    width = attr_property("width", thug_long)

    def __init__(self, doc, tag):
        HTMLElement.__init__(self, doc, tag)
