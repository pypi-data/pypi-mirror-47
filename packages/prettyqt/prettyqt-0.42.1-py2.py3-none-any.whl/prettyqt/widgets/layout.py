# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

from prettyqt import widgets, core
from prettyqt.utils import bidict


MODES = bidict(maximum=QtWidgets.QLayout.SetMaximumSize,
               fixed=QtWidgets.QLayout.SetFixedSize)

ALIGNMENTS = bidict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    top=QtCore.Qt.AlignTop,
                    bottom=QtCore.Qt.AlignBottom)


class Layout(QtWidgets.QLayout):

    def __repr__(self):
        return f"{self.__class__.__name__}: {len(self)} children"

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def get_size_mode(self) -> str:
        return MODES.inv[self.sizeConstraint()]

    def set_alignment(self, alignment: str):
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment!r} not a valid alignment.")
        self.setAlignment(ALIGNMENTS[alignment])

    def get_alignment(self) -> str:
        return MODES.inv[self.alignment()]

    def add(self, item) -> int:
        if isinstance(item, QtWidgets.QWidget):
            return self.addWidget(item)
        elif isinstance(item, QtWidgets.QLayout):
            w = widgets.Widget()
            w.set_layout(item)
            return self.addWidget(w)
        else:
            raise TypeError("add_item only supports widgets and layouts")


Layout.__bases__[0].__bases__ = (core.Object, QtWidgets.QLayoutItem)
