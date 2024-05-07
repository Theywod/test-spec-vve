import os
from PyQt5 import uic


def convert_ui_folder(ui_folder):
	for file in os.listdir(ui_folder):
		if file.endswith('.ui'):
			with open(ui_folder + file.replace('.ui', '.py'), 'w', encoding='utf-8') as py_file:
				uic.compileUi(ui_folder + file, py_file)


def convert(*modules):
	for module in modules:
		ui_folder = module.__path__[0] + '/'
		convert_ui_folder(ui_folder)
