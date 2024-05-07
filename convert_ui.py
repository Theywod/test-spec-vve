from pyqt_instruments.ui_converter import convert
import forms


def convert_package_ui():
    convert(forms)


if __name__ == '__main__':
    convert_package_ui()
