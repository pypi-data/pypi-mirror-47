# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/randovania/randovania/randovania/gui/tracker_window.ui',
# licensing of '/home/travis/build/randovania/randovania/randovania/gui/tracker_window.ui' applies.
#
# Created: Tue May 28 20:55:47 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TrackerWindow(object):
    def setupUi(self, TrackerWindow):
        TrackerWindow.setObjectName("TrackerWindow")
        TrackerWindow.resize(932, 488)
        self.centralWidget = QtWidgets.QWidget(TrackerWindow)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.undo_last_action_button = QtWidgets.QPushButton(self.centralWidget)
        self.undo_last_action_button.setObjectName("undo_last_action_button")
        self.gridLayout.addWidget(self.undo_last_action_button, 0, 4, 1, 1)
        self.actions_box = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actions_box.sizePolicy().hasHeightForWidth())
        self.actions_box.setSizePolicy(sizePolicy)
        self.actions_box.setTitle("")
        self.actions_box.setObjectName("actions_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.actions_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.actions_title_label = QtWidgets.QLabel(self.actions_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actions_title_label.sizePolicy().hasHeightForWidth())
        self.actions_title_label.setSizePolicy(sizePolicy)
        self.actions_title_label.setWordWrap(True)
        self.actions_title_label.setObjectName("actions_title_label")
        self.verticalLayout.addWidget(self.actions_title_label)
        self.actions_list = QtWidgets.QListWidget(self.actions_box)
        self.actions_list.setObjectName("actions_list")
        self.verticalLayout.addWidget(self.actions_list)
        self.gridLayout.addWidget(self.actions_box, 1, 4, 1, 1)
        self.configuration_label = QtWidgets.QLabel(self.centralWidget)
        self.configuration_label.setWordWrap(True)
        self.configuration_label.setObjectName("configuration_label")
        self.gridLayout.addWidget(self.configuration_label, 0, 0, 1, 4)
        self.pickups_scroll_area = QtWidgets.QScrollArea(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pickups_scroll_area.sizePolicy().hasHeightForWidth())
        self.pickups_scroll_area.setSizePolicy(sizePolicy)
        self.pickups_scroll_area.setMinimumSize(QtCore.QSize(285, 0))
        self.pickups_scroll_area.setWidgetResizable(True)
        self.pickups_scroll_area.setObjectName("pickups_scroll_area")
        self.pickups_scroll_contents = QtWidgets.QWidget()
        self.pickups_scroll_contents.setGeometry(QtCore.QRect(0, 0, 283, 419))
        self.pickups_scroll_contents.setObjectName("pickups_scroll_contents")
        self.pickup_box_layout = QtWidgets.QVBoxLayout(self.pickups_scroll_contents)
        self.pickup_box_layout.setObjectName("pickup_box_layout")
        self.upgrades_box = QtWidgets.QGroupBox(self.pickups_scroll_contents)
        self.upgrades_box.setObjectName("upgrades_box")
        self.upgrades_layout = QtWidgets.QGridLayout(self.upgrades_box)
        self.upgrades_layout.setObjectName("upgrades_layout")
        self.pickup_box_layout.addWidget(self.upgrades_box)
        self.translators_box = QtWidgets.QGroupBox(self.pickups_scroll_contents)
        self.translators_box.setObjectName("translators_box")
        self.translators_layout = QtWidgets.QGridLayout(self.translators_box)
        self.translators_layout.setObjectName("translators_layout")
        self.pickup_box_layout.addWidget(self.translators_box)
        self.expansions_box = QtWidgets.QGroupBox(self.pickups_scroll_contents)
        self.expansions_box.setObjectName("expansions_box")
        self.expansions_layout = QtWidgets.QGridLayout(self.expansions_box)
        self.expansions_layout.setObjectName("expansions_layout")
        self.pickup_box_layout.addWidget(self.expansions_box)
        self.keys_box = QtWidgets.QGroupBox(self.pickups_scroll_contents)
        self.keys_box.setObjectName("keys_box")
        self.keys_layout = QtWidgets.QGridLayout(self.keys_box)
        self.keys_layout.setObjectName("keys_layout")
        self.pickup_box_layout.addWidget(self.keys_box)
        self.events_box = QtWidgets.QGroupBox(self.pickups_scroll_contents)
        self.events_box.setObjectName("events_box")
        self.events_layout = QtWidgets.QVBoxLayout(self.events_box)
        self.events_layout.setObjectName("events_layout")
        self.pickup_box_layout.addWidget(self.events_box)
        self.pickups_scroll_area.setWidget(self.pickups_scroll_contents)
        self.gridLayout.addWidget(self.pickups_scroll_area, 1, 0, 1, 1)
        self.location_box = QtWidgets.QGroupBox(self.centralWidget)
        self.location_box.setObjectName("location_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.location_box)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.resource_filter_check = QtWidgets.QCheckBox(self.location_box)
        self.resource_filter_check.setChecked(True)
        self.resource_filter_check.setObjectName("resource_filter_check")
        self.verticalLayout_2.addWidget(self.resource_filter_check)
        self.hide_collected_resources_check = QtWidgets.QCheckBox(self.location_box)
        self.hide_collected_resources_check.setObjectName("hide_collected_resources_check")
        self.verticalLayout_2.addWidget(self.hide_collected_resources_check)
        self.possible_locations_tree = QtWidgets.QTreeWidget(self.location_box)
        self.possible_locations_tree.setObjectName("possible_locations_tree")
        self.verticalLayout_2.addWidget(self.possible_locations_tree)
        self.gridLayout.addWidget(self.location_box, 1, 1, 1, 3)
        TrackerWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(TrackerWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 932, 21))
        self.menuBar.setObjectName("menuBar")
        TrackerWindow.setMenuBar(self.menuBar)

        self.retranslateUi(TrackerWindow)
        QtCore.QMetaObject.connectSlotsByName(TrackerWindow)

    def retranslateUi(self, TrackerWindow):
        TrackerWindow.setWindowTitle(QtWidgets.QApplication.translate("TrackerWindow", "Tracker", None, -1))
        self.undo_last_action_button.setText(QtWidgets.QApplication.translate("TrackerWindow", "Undo last action", None, -1))
        self.actions_title_label.setText(QtWidgets.QApplication.translate("TrackerWindow", "<html><head/><body><p>History of all actions that have been performed.</p><p>Press &quot;Undo last action&quot; to remove the last action from the list.</p></body></html>", None, -1))
        self.configuration_label.setText(QtWidgets.QApplication.translate("TrackerWindow", "Trick Level: ???; Elevators: Vanilla; Item Loss: ???", None, -1))
        self.upgrades_box.setTitle(QtWidgets.QApplication.translate("TrackerWindow", "Upgrades", None, -1))
        self.translators_box.setTitle(QtWidgets.QApplication.translate("TrackerWindow", "Translators", None, -1))
        self.expansions_box.setTitle(QtWidgets.QApplication.translate("TrackerWindow", "Expansions", None, -1))
        self.keys_box.setTitle(QtWidgets.QApplication.translate("TrackerWindow", "Keys", None, -1))
        self.events_box.setTitle(QtWidgets.QApplication.translate("TrackerWindow", "Events", None, -1))
        self.location_box.setTitle(QtWidgets.QApplication.translate("TrackerWindow", "Current location: ", None, -1))
        self.resource_filter_check.setText(QtWidgets.QApplication.translate("TrackerWindow", "Show only resources", None, -1))
        self.hide_collected_resources_check.setText(QtWidgets.QApplication.translate("TrackerWindow", "Hide collected resources", None, -1))
        self.possible_locations_tree.headerItem().setText(0, QtWidgets.QApplication.translate("TrackerWindow", "Accessible Locations", None, -1))

