"""Viz namespace contains all the classes to create a visualization, mainly
Map and Layer. It also includes our basemaps and the helper methods."""
from __future__ import absolute_import

from .basemaps import Basemaps as basemaps
from .map import Map
from .layer import Layer
from .source import Source
from .style import Style
from .popup import Popup
from .legend import Legend


__all__ = [
    'basemaps',
    'Map',
    'Layer',
    'Source',
    'Style',
    'Popup',
    'Legend'
]
