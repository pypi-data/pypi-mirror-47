# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import List

from qtpy import QtCore, QtWidgets

from prettyqt import widgets, core
from prettyqt.utils import bidict


BUTTONS = bidict(cancel=QtWidgets.QDialogButtonBox.Cancel,
                 ok=QtWidgets.QDialogButtonBox.Ok,
                 save=QtWidgets.QDialogButtonBox.Save,
                 open=QtWidgets.QDialogButtonBox.Open,
                 close=QtWidgets.QDialogButtonBox.Close,
                 discard=QtWidgets.QDialogButtonBox.Discard,
                 apply=QtWidgets.QDialogButtonBox.Apply,
                 reset=QtWidgets.QDialogButtonBox.Reset,
                 restore_defaults=QtWidgets.QDialogButtonBox.RestoreDefaults,
                 help=QtWidgets.QDialogButtonBox.Help,
                 save_all=QtWidgets.QDialogButtonBox.SaveAll,
                 yes=QtWidgets.QDialogButtonBox.Yes,
                 yes_to_all=QtWidgets.QDialogButtonBox.YesToAll,
                 no=QtWidgets.QDialogButtonBox.No,
                 no_to_all=QtWidgets.QDialogButtonBox.NoToAll,
                 abort=QtWidgets.QDialogButtonBox.Abort,
                 retry=QtWidgets.QDialogButtonBox.Retry,
                 ignore=QtWidgets.QDialogButtonBox.Ignore)

ROLES = bidict(invalid=QtWidgets.QDialogButtonBox.InvalidRole,
               accept=QtWidgets.QDialogButtonBox.AcceptRole,
               reject=QtWidgets.QDialogButtonBox.RejectRole,
               destructive=QtWidgets.QDialogButtonBox.DestructiveRole,
               action=QtWidgets.QDialogButtonBox.ActionRole,
               help=QtWidgets.QDialogButtonBox.HelpRole,
               yes=QtWidgets.QDialogButtonBox.YesRole,
               no=QtWidgets.QDialogButtonBox.NoRole,
               apply=QtWidgets.QDialogButtonBox.ApplyRole,
               reset=QtWidgets.QDialogButtonBox.ResetRole)

ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal,
                      vertical=QtCore.Qt.Vertical)


QtWidgets.QDialogButtonBox.__bases__ = (widgets.Widget,)


class DialogButtonBox(QtWidgets.QDialogButtonBox):

    button_clicked = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.on_click)

    def __len__(self):
        return len(self.buttons())

    def __getitem__(self, index):
        return self.button(BUTTONS[index])

    def __iter__(self):
        return iter(self.buttons())

    def __contains__(self, item):
        return self[item] is not None

    @classmethod
    def create(cls, **kwargs):
        box = cls()
        for k, v in kwargs.items():
            btn = box.add_button(k)
            btn.clicked.connect(v)
        return box

    def on_click(self, button):
        self.button_clicked.emit(button.objectName())

    def set_horizontal(self):
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        self.setOrientation(QtCore.Qt.Vertical)

    def set_orientation(self, orientation: str):
        """set the orientation of the splitter

        Allowed values are "horizontal", "vertical"

        Args:
            mode: orientation for the splitter

        Raises:
            ValueError: orientation does not exist
        """
        if orientation not in ORIENTATIONS:
            raise ValueError(f"{orientation} not a valid orientation.")
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self) -> str:
        """returns current orientation

        Possible values: "horizontal", "vertical"

        Returns:
            orientation
        """
        return ORIENTATIONS.inv[self.orientation()]

    def add_buttons(self, buttons: List[str]):
        return [self.add_button(btn) for btn in buttons]

    def add_button(self, button: str):
        """add a default button

        Valid arguments: "cancel", "ok", "save", "open", "close",
                         "discard", "apply", "reset", "restore_defaults",
                         "help", "save_all", "yes", "yes_to_all", "no",
                         "no_to_all", "abort", "retry", "ignore"

        Args:
            button: button to add

        Returns:
            created button

        Raises:
            ValueError: Button type not available
        """
        if button not in BUTTONS:
            raise ValueError("button type not available")
        btn = self.addButton(BUTTONS[button])
        btn.setObjectName(button)
        return btn

    def add_accept_button(self, button: QtWidgets.QPushButton):
        btn = self.addButton(button, self.AcceptRole)
        btn.setObjectName(button)
        return btn

    def add_reject_button(self, button: QtWidgets.QPushButton):
        btn = self.addButton(button, self.RejectRole)
        btn.setObjectName(button)
        return btn


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    widget = DialogButtonBox()
    buttons = list(BUTTONS.keys())
    widget.add_buttons(buttons)
    widget.button_clicked.connect(print)
    widget.show()
    app.exec_()
