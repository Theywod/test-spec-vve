from PyQt5.QtWidgets import QWidget, QMainWindow, QSpinBox, QDoubleSpinBox,\
	QComboBox, QCheckBox, QRadioButton, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import QSettings, QObject
from typing import List, Tuple


__widgets_properties = {
	QComboBox.staticMetaObject.className():
		(str, '', QComboBox.setCurrentText, QComboBox.currentText),
	QSpinBox.staticMetaObject.className():
		(int, 0, QSpinBox.setValue, QSpinBox.value),
	QDoubleSpinBox.staticMetaObject.className():
		(float, 0, QDoubleSpinBox.setValue, QDoubleSpinBox.value),
	QCheckBox.staticMetaObject.className():
		(bool, False, QCheckBox.setChecked, QCheckBox.isChecked),
	QLineEdit.staticMetaObject.className():
		(str, '', QLineEdit.setText, QLineEdit.text),
	QRadioButton.staticMetaObject.className():
		(bool, False, QRadioButton.setChecked, QRadioButton.isChecked),
}


def __find_widgets(main_widget: QWidget, types: Tuple[QWidget, ...]):
	return filter(lambda w: not w.objectName().startswith('qt_') and w.objectName(), main_widget.findChildren(types))


def __get_function(w: QObject):
	type_, def_value, set_function, get_function = __widgets_properties[w.staticMetaObject.className()]
	return get_function


def __set_function(w: QObject):
	type_, def_value, set_function, get_function = __widgets_properties[w.staticMetaObject.className()]
	return set_function, type_, def_value


def save_widgets_values(settings: QSettings, parent_widget: QWidget, types: Tuple[QWidget, ...]):
	settings.beginGroup("Qt_Widgets")
	for widget in __find_widgets(parent_widget, types):
		get_ = __get_function(widget)
		settings.setValue(widget.objectName(), get_(widget))
	settings.endGroup()
	

def restore_widgets_values(settings: QSettings, parent_widget: QWidget, types: Tuple[QWidget, ...]):
	settings.beginGroup("Qt_Widgets")
	for widget in __find_widgets(parent_widget, types):
		set_, type_, default_ = __set_function(widget)
		set_(widget, settings.value(widget.objectName(), default_, type_))
	settings.endGroup()


def save_windows_values(settings: QSettings, *windows: QMainWindow):
	settings.beginGroup("Qt_Windows")
	for window in windows:
		settings.setValue(window.objectName() + "_size", window.size())
		settings.setValue(window.objectName() + "_pos", window.pos())
	settings.endGroup()


def restore_windows_values(settings: QSettings, *windows: QMainWindow):
	settings.beginGroup("Qt_Windows")
	for window in windows:
		window.resize(settings.value(window.objectName() + "_size", window.baseSize()))
		window.move(settings.value(window.objectName() + "_pos", window.pos()))
	settings.endGroup()


def __save_tree_item(settings: QSettings, item: QTreeWidgetItem, depth_current, prefix_root):
	if item.childCount() and depth_current > 0:
		settings.setValue(prefix_root, item.isExpanded())
		settings.beginGroup(prefix_root)
		for child in range(item.childCount()):
			__save_tree_item(settings, item.child(child), depth_current - 1, str(child))
		settings.endGroup()


def __restore_tree_item(settings: QSettings, item: QTreeWidgetItem, depth_current, prefix_root):
	if item.childCount() and depth_current > 0:
		item.setExpanded(settings.value(prefix_root, True, bool))
		settings.beginGroup(prefix_root)
		for child in range(item.childCount()):
			__restore_tree_item(settings, item.child(child), depth_current - 1, str(child))
		settings.endGroup()


def save_tree(settings: QSettings, widgets: List[QObject], depth=2):
	settings.beginGroup("Qt_Tree")
	for i, tree in enumerate(widgets):
		settings.beginGroup(str(i))
		for item_i in range(tree.topLevelItemCount()):
			__save_tree_item(settings, tree.topLevelItem(item_i), depth, str(item_i))
		settings.endGroup()
	settings.endGroup()


def restore_tree(settings: QSettings, widgets: List[QObject], depth=2):
	settings.beginGroup("Qt_Tree")
	for i, tree in enumerate(widgets):
		settings.beginGroup(str(i))
		for item_i in range(tree.topLevelItemCount()):
			__restore_tree_item(settings, tree.topLevelItem(item_i), depth, str(item_i))
		settings.endGroup()
	settings.endGroup()


saved_widgets = (QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox, QRadioButton, QLineEdit)
