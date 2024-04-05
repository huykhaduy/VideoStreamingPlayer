from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig

class StyleSheet(StyleSheetBase, Enum):
    """ StyleSheet enumeration """
    MAIN_INTERFACE = "main_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/styles/qss/{theme.value.lower()}/{self.value}.qss"
