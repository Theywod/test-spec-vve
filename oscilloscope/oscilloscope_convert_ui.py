from pyqt_instruments.ui_converter import convert
import oscilloscope.forms

def convert_package_ui():
    convert(oscilloscope.forms)

if __name__ == '__oscilloscope__':
    convert_package_ui()
