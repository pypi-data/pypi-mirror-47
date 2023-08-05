# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/randovania/randovania/randovania/gui/logic_settings_window.ui',
# licensing of '/home/travis/build/randovania/randovania/randovania/gui/logic_settings_window.ui' applies.
#
# Created: Tue May 28 20:55:48 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LogicSettingsWindow(object):
    def setupUi(self, LogicSettingsWindow):
        LogicSettingsWindow.setObjectName("LogicSettingsWindow")
        LogicSettingsWindow.resize(519, 402)
        self.centralWidget = QtWidgets.QWidget(LogicSettingsWindow)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tab_widget = QtWidgets.QTabWidget(self.centralWidget)
        self.tab_widget.setObjectName("tab_widget")
        self.trick_level_tab = QtWidgets.QWidget()
        self.trick_level_tab.setObjectName("trick_level_tab")
        self.trick_level_top_layout = QtWidgets.QVBoxLayout(self.trick_level_tab)
        self.trick_level_top_layout.setObjectName("trick_level_top_layout")
        self.trick_level_scroll = QtWidgets.QScrollArea(self.trick_level_tab)
        self.trick_level_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.trick_level_scroll.setFrameShadow(QtWidgets.QFrame.Plain)
        self.trick_level_scroll.setWidgetResizable(True)
        self.trick_level_scroll.setObjectName("trick_level_scroll")
        self.trick_level_scroll_contents = QtWidgets.QWidget()
        self.trick_level_scroll_contents.setGeometry(QtCore.QRect(0, 0, 491, 339))
        self.trick_level_scroll_contents.setObjectName("trick_level_scroll_contents")
        self.trick_level_layout = QtWidgets.QVBoxLayout(self.trick_level_scroll_contents)
        self.trick_level_layout.setObjectName("trick_level_layout")
        self.logic_description_label = QtWidgets.QLabel(self.trick_level_scroll_contents)
        self.logic_description_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.logic_description_label.setWordWrap(True)
        self.logic_description_label.setObjectName("logic_description_label")
        self.trick_level_layout.addWidget(self.logic_description_label)
        self.logic_combo_box = QtWidgets.QComboBox(self.trick_level_scroll_contents)
        self.logic_combo_box.setObjectName("logic_combo_box")
        self.logic_combo_box.addItem("")
        self.logic_combo_box.addItem("")
        self.logic_combo_box.addItem("")
        self.logic_combo_box.addItem("")
        self.logic_combo_box.addItem("")
        self.logic_combo_box.addItem("")
        self.logic_combo_box.addItem("")
        self.trick_level_layout.addWidget(self.logic_combo_box)
        self.logic_level_label = QtWidgets.QLabel(self.trick_level_scroll_contents)
        self.logic_level_label.setMinimumSize(QtCore.QSize(0, 25))
        self.logic_level_label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.logic_level_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.logic_level_label.setWordWrap(True)
        self.logic_level_label.setObjectName("logic_level_label")
        self.trick_level_layout.addWidget(self.logic_level_label)
        self.trick_level_line = QtWidgets.QFrame(self.trick_level_scroll_contents)
        self.trick_level_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.trick_level_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.trick_level_line.setObjectName("trick_level_line")
        self.trick_level_layout.addWidget(self.trick_level_line)
        self.trick_level_help_label = QtWidgets.QLabel(self.trick_level_scroll_contents)
        self.trick_level_help_label.setObjectName("trick_level_help_label")
        self.trick_level_layout.addWidget(self.trick_level_help_label)
        self.trick_level_scroll.setWidget(self.trick_level_scroll_contents)
        self.trick_level_top_layout.addWidget(self.trick_level_scroll)
        self.tab_widget.addTab(self.trick_level_tab, "")
        self.elevator_tab = QtWidgets.QWidget()
        self.elevator_tab.setObjectName("elevator_tab")
        self.elevator_layout = QtWidgets.QVBoxLayout(self.elevator_tab)
        self.elevator_layout.setObjectName("elevator_layout")
        self.elevators_description_label = QtWidgets.QLabel(self.elevator_tab)
        self.elevators_description_label.setWordWrap(True)
        self.elevators_description_label.setObjectName("elevators_description_label")
        self.elevator_layout.addWidget(self.elevators_description_label)
        self.elevators_combo = QtWidgets.QComboBox(self.elevator_tab)
        self.elevators_combo.setObjectName("elevators_combo")
        self.elevators_combo.addItem("")
        self.elevators_combo.addItem("")
        self.elevator_layout.addWidget(self.elevators_combo)
        self.tab_widget.addTab(self.elevator_tab, "")
        self.goal_tab = QtWidgets.QWidget()
        self.goal_tab.setObjectName("goal_tab")
        self.goal_layout = QtWidgets.QVBoxLayout(self.goal_tab)
        self.goal_layout.setObjectName("goal_layout")
        self.skytemple_description = QtWidgets.QLabel(self.goal_tab)
        self.skytemple_description.setWordWrap(True)
        self.skytemple_description.setObjectName("skytemple_description")
        self.goal_layout.addWidget(self.skytemple_description)
        self.skytemple_combo = QtWidgets.QComboBox(self.goal_tab)
        self.skytemple_combo.setObjectName("skytemple_combo")
        self.skytemple_combo.addItem("")
        self.skytemple_combo.addItem("")
        self.skytemple_combo.addItem("")
        self.goal_layout.addWidget(self.skytemple_combo)
        self.skytemple_slider_layout = QtWidgets.QHBoxLayout()
        self.skytemple_slider_layout.setObjectName("skytemple_slider_layout")
        self.skytemple_slider = QtWidgets.QSlider(self.goal_tab)
        self.skytemple_slider.setMaximum(9)
        self.skytemple_slider.setPageStep(2)
        self.skytemple_slider.setOrientation(QtCore.Qt.Horizontal)
        self.skytemple_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.skytemple_slider.setObjectName("skytemple_slider")
        self.skytemple_slider_layout.addWidget(self.skytemple_slider)
        self.skytemple_slider_label = QtWidgets.QLabel(self.goal_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skytemple_slider_label.sizePolicy().hasHeightForWidth())
        self.skytemple_slider_label.setSizePolicy(sizePolicy)
        self.skytemple_slider_label.setMinimumSize(QtCore.QSize(20, 0))
        self.skytemple_slider_label.setAlignment(QtCore.Qt.AlignCenter)
        self.skytemple_slider_label.setObjectName("skytemple_slider_label")
        self.skytemple_slider_layout.addWidget(self.skytemple_slider_label)
        self.goal_layout.addLayout(self.skytemple_slider_layout)
        self.tab_widget.addTab(self.goal_tab, "")
        self.starting_area_tab = QtWidgets.QWidget()
        self.starting_area_tab.setObjectName("starting_area_tab")
        self.starting_area_layout = QtWidgets.QVBoxLayout(self.starting_area_tab)
        self.starting_area_layout.setObjectName("starting_area_layout")
        self.startingarea_description = QtWidgets.QLabel(self.starting_area_tab)
        self.startingarea_description.setWordWrap(True)
        self.startingarea_description.setObjectName("startingarea_description")
        self.starting_area_layout.addWidget(self.startingarea_description)
        self.startingarea_combo = QtWidgets.QComboBox(self.starting_area_tab)
        self.startingarea_combo.setObjectName("startingarea_combo")
        self.startingarea_combo.addItem("")
        self.startingarea_combo.addItem("")
        self.startingarea_combo.addItem("")
        self.starting_area_layout.addWidget(self.startingarea_combo)
        self.specific_starting_layout = QtWidgets.QHBoxLayout()
        self.specific_starting_layout.setObjectName("specific_starting_layout")
        self.specific_starting_world_combo = QtWidgets.QComboBox(self.starting_area_tab)
        self.specific_starting_world_combo.setEnabled(False)
        self.specific_starting_world_combo.setObjectName("specific_starting_world_combo")
        self.specific_starting_layout.addWidget(self.specific_starting_world_combo)
        self.specific_starting_area_combo = QtWidgets.QComboBox(self.starting_area_tab)
        self.specific_starting_area_combo.setEnabled(False)
        self.specific_starting_area_combo.setObjectName("specific_starting_area_combo")
        self.specific_starting_layout.addWidget(self.specific_starting_area_combo)
        self.starting_area_layout.addLayout(self.specific_starting_layout)
        self.tab_widget.addTab(self.starting_area_tab, "")
        self.translators_tab = QtWidgets.QWidget()
        self.translators_tab.setObjectName("translators_tab")
        self.translators_top_layout = QtWidgets.QGridLayout(self.translators_tab)
        self.translators_top_layout.setObjectName("translators_top_layout")
        self.translators_scroll = QtWidgets.QScrollArea(self.translators_tab)
        self.translators_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.translators_scroll.setFrameShadow(QtWidgets.QFrame.Plain)
        self.translators_scroll.setLineWidth(0)
        self.translators_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.translators_scroll.setWidgetResizable(True)
        self.translators_scroll.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.translators_scroll.setObjectName("translators_scroll")
        self.translators_scroll_contents = QtWidgets.QWidget()
        self.translators_scroll_contents.setGeometry(QtCore.QRect(0, 0, 285, 186))
        self.translators_scroll_contents.setObjectName("translators_scroll_contents")
        self.translators_layout = QtWidgets.QGridLayout(self.translators_scroll_contents)
        self.translators_layout.setObjectName("translators_layout")
        self.translators_description = QtWidgets.QLabel(self.translators_scroll_contents)
        self.translators_description.setWordWrap(True)
        self.translators_description.setObjectName("translators_description")
        self.translators_layout.addWidget(self.translators_description, 0, 0, 1, 3)
        self.always_up_gfmc_compound_check = QtWidgets.QCheckBox(self.translators_scroll_contents)
        self.always_up_gfmc_compound_check.setObjectName("always_up_gfmc_compound_check")
        self.translators_layout.addWidget(self.always_up_gfmc_compound_check, 1, 0, 1, 1)
        self.always_up_torvus_temple_check = QtWidgets.QCheckBox(self.translators_scroll_contents)
        self.always_up_torvus_temple_check.setObjectName("always_up_torvus_temple_check")
        self.translators_layout.addWidget(self.always_up_torvus_temple_check, 1, 1, 1, 1)
        self.always_up_great_temple_check = QtWidgets.QCheckBox(self.translators_scroll_contents)
        self.always_up_great_temple_check.setObjectName("always_up_great_temple_check")
        self.translators_layout.addWidget(self.always_up_great_temple_check, 1, 2, 1, 1)
        self.translator_randomize_all_button = QtWidgets.QPushButton(self.translators_scroll_contents)
        self.translator_randomize_all_button.setObjectName("translator_randomize_all_button")
        self.translators_layout.addWidget(self.translator_randomize_all_button, 2, 0, 1, 1)
        self.translator_vanilla_actual_button = QtWidgets.QPushButton(self.translators_scroll_contents)
        self.translator_vanilla_actual_button.setObjectName("translator_vanilla_actual_button")
        self.translators_layout.addWidget(self.translator_vanilla_actual_button, 2, 1, 1, 1)
        self.translator_vanilla_colors_button = QtWidgets.QPushButton(self.translators_scroll_contents)
        self.translator_vanilla_colors_button.setObjectName("translator_vanilla_colors_button")
        self.translators_layout.addWidget(self.translator_vanilla_colors_button, 2, 2, 1, 1)
        self.translators_scroll.setWidget(self.translators_scroll_contents)
        self.translators_top_layout.addWidget(self.translators_scroll, 0, 1, 1, 1)
        self.tab_widget.addTab(self.translators_tab, "")
        self.hint_tab = QtWidgets.QWidget()
        self.hint_tab.setObjectName("hint_tab")
        self.hint_layout = QtWidgets.QVBoxLayout(self.hint_tab)
        self.hint_layout.setObjectName("hint_layout")
        self.hint_sky_temple_key_label = QtWidgets.QLabel(self.hint_tab)
        self.hint_sky_temple_key_label.setWordWrap(True)
        self.hint_sky_temple_key_label.setObjectName("hint_sky_temple_key_label")
        self.hint_layout.addWidget(self.hint_sky_temple_key_label)
        self.hint_sky_temple_key_combo = QtWidgets.QComboBox(self.hint_tab)
        self.hint_sky_temple_key_combo.setObjectName("hint_sky_temple_key_combo")
        self.hint_sky_temple_key_combo.addItem("")
        self.hint_sky_temple_key_combo.addItem("")
        self.hint_sky_temple_key_combo.addItem("")
        self.hint_layout.addWidget(self.hint_sky_temple_key_combo)
        self.tab_widget.addTab(self.hint_tab, "")
        self.horizontalLayout.addWidget(self.tab_widget)
        LogicSettingsWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(LogicSettingsWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 519, 17))
        self.menuBar.setObjectName("menuBar")
        LogicSettingsWindow.setMenuBar(self.menuBar)

        self.retranslateUi(LogicSettingsWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(LogicSettingsWindow)

    def retranslateUi(self, LogicSettingsWindow):
        LogicSettingsWindow.setWindowTitle(QtWidgets.QApplication.translate("LogicSettingsWindow", "Someone forgot to name this", None, -1))
        self.logic_description_label.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p align=\"justify\">There are logic rules in place which prevent you from being locked out of progression and guaranteeing that you’ll be able to finish the game every time regardless of the distribution of items. More advanced trick levels assumes more knowledge of how the game works and ability to abuse game mechanics.</p><p align=\"justify\">No matter the level, it is always possible to softlock when you enter a room or area that you\'re unable to leave. For example, vanilla beam rooms without the necessary beam to escape, Dark World without Light Beam/Anihhilator Beam, Torvus Bog without Super Missile.</p><p align=\"justify\">However, it may be <span style=\" font-style:italic;\">necessary</span> to enter Dark World without a way to escape if that item is located in the Dark World.</p></body></html>", None, -1))
        self.logic_combo_box.setItemText(0, QtWidgets.QApplication.translate("LogicSettingsWindow", "No Tricks", None, -1))
        self.logic_combo_box.setItemText(1, QtWidgets.QApplication.translate("LogicSettingsWindow", "Trivial", None, -1))
        self.logic_combo_box.setItemText(2, QtWidgets.QApplication.translate("LogicSettingsWindow", "Easy", None, -1))
        self.logic_combo_box.setItemText(3, QtWidgets.QApplication.translate("LogicSettingsWindow", "Normal", None, -1))
        self.logic_combo_box.setItemText(4, QtWidgets.QApplication.translate("LogicSettingsWindow", "Hard", None, -1))
        self.logic_combo_box.setItemText(5, QtWidgets.QApplication.translate("LogicSettingsWindow", "Hypermode", None, -1))
        self.logic_combo_box.setItemText(6, QtWidgets.QApplication.translate("LogicSettingsWindow", "Minimal Checking", None, -1))
        self.logic_level_label.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p align=\"justify\">This mode requires no knowledge about the game, nor does it require any abuse of game mechanics, making it ideal for casual and first time players.</p></body></html>", None, -1))
        self.trick_level_help_label.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p>If you want to control the expected level of a specific trick, select the trick below and then move the slider to the level you want.</p><p>Configuring a trick\'s difficulty to above to global difficulty above <span style=\" font-weight:600;\">has no effect</span>.</p><p>Press the ? button to see which rooms use that trick on the selected level.</p></body></html>", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.trick_level_tab), QtWidgets.QApplication.translate("LogicSettingsWindow", "Trick Level", None, -1))
        self.elevators_description_label.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p>Controls what each elevator connects to.</p><p>Two-way: after taking an elevator, the elevator in the room you\'re left brings you to where you where.<br/>Between Areas: An elevator will never connect to another in the same area.</p></body></html>", None, -1))
        self.elevators_combo.setItemText(0, QtWidgets.QApplication.translate("LogicSettingsWindow", "Original Connections", None, -1))
        self.elevators_combo.setItemText(1, QtWidgets.QApplication.translate("LogicSettingsWindow", "Random: Two-way, between areas", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.elevator_tab), QtWidgets.QApplication.translate("LogicSettingsWindow", "Elevators", None, -1))
        self.skytemple_description.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p>Controls where the Sky Temple Keys will be located.</p><p>All Guardians and Sub-Guardians: One key will be placed in each of the guardians and sub-guardians.<br/>Guardians: One key will be placed as the reward of each of the guardians.<br/>Collect Sky Temple Keys: A configurable quantity will be shuffled over the game world.</p><p>The Guardians are: Amorbis, Chykka and Quadraxis.<br/>The Sub-Guardians are: Bomb Guardian, Jump Guardian, Boost Guardian, Grapple Guardian, Spider Guardian and Power Bomb Guardian.</p><p>You can always check Sky Temple Gateway for hints where the keys were placed.</p></body></html>", None, -1))
        self.skytemple_combo.setItemText(0, QtWidgets.QApplication.translate("LogicSettingsWindow", "Guardians and Sub-Guardians", None, -1))
        self.skytemple_combo.setItemText(1, QtWidgets.QApplication.translate("LogicSettingsWindow", "Guardians", None, -1))
        self.skytemple_combo.setItemText(2, QtWidgets.QApplication.translate("LogicSettingsWindow", "Collect Sky Temple Keys", None, -1))
        self.skytemple_slider_label.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "0", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.goal_tab), QtWidgets.QApplication.translate("LogicSettingsWindow", "Goal", None, -1))
        self.startingarea_description.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p>Choose the area where the game will start at.</p><p>Ship: Samus\' Ship at Temple Grounds - Landing Site. The vanilla location.<br/>Random Save Station: a random Save Station of the game will be chosen.<br/>Specific Area: A user provided choice. The specific location on the area depends on each one.</p><p><span style=\" font-weight:600;\">WARNING</span>: depending on the starting items that are configured, it may be impossible to start at the chosen place. In that case, the generation will fail.</p></body></html>", None, -1))
        self.startingarea_combo.setItemText(0, QtWidgets.QApplication.translate("LogicSettingsWindow", "Ship", None, -1))
        self.startingarea_combo.setItemText(1, QtWidgets.QApplication.translate("LogicSettingsWindow", "Random Save Station", None, -1))
        self.startingarea_combo.setItemText(2, QtWidgets.QApplication.translate("LogicSettingsWindow", "Specific Area (Choose Below)", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.starting_area_tab), QtWidgets.QApplication.translate("LogicSettingsWindow", "Starting Area", None, -1))
        self.translators_description.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p>Change which translator is required for all the gates in the game. Their colors are changed to match the necessary translator.</p><p>There are two vanilla options: using the actual translator requirements in the game, and using the vanilla gate colors.<br/>This is because in the original game, some translator gates are colored one way, but the translator requirement is something else.</p><p><br/>Some translator gates appears only after some event is triggered in game. The following options change them so they\'re always there. The Great Temple has a special case: if you enter Great Temple via Transport A, the Emerald gate will be permanently down.</p></body></html>", None, -1))
        self.always_up_gfmc_compound_check.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "GFMC Compound", None, -1))
        self.always_up_torvus_temple_check.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "Torvus Temple", None, -1))
        self.always_up_great_temple_check.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "Great Temple (Emerald)", None, -1))
        self.translator_randomize_all_button.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "Randomize All", None, -1))
        self.translator_vanilla_actual_button.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "Vanilla (Actual)", None, -1))
        self.translator_vanilla_colors_button.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "Vanilla (Colors)", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.translators_tab), QtWidgets.QApplication.translate("LogicSettingsWindow", "Translator Gates", None, -1))
        self.hint_sky_temple_key_label.setText(QtWidgets.QApplication.translate("LogicSettingsWindow", "<html><head/><body><p>Controls how precise the hints for Sky Temple Keys in Sky Temple Gateway are.</p><p><span style=\" font-weight:600;\">No hints</span>: The scans provide no useful information.</p><p><span style=\" font-weight:600;\">Show only the area name</span>: The scans will say the key is in &quot;Temple Grounds&quot;, &quot;Agon Wastes&quot;, etc.<br/>There is no difference between Aether and Dark Aether. So Agon Wastes means both light and dark world.</p><p><span style=\" font-weight:600;\">Show area and room name</span>: The scans will say the key is in &quot;Great Temple - Transport A Access&quot;, etc. For rooms with more than one item, there\'s no way to distinguish which one it is.</p></body></html>", None, -1))
        self.hint_sky_temple_key_combo.setItemText(0, QtWidgets.QApplication.translate("LogicSettingsWindow", "No hints", None, -1))
        self.hint_sky_temple_key_combo.setItemText(1, QtWidgets.QApplication.translate("LogicSettingsWindow", "Show only the area name", None, -1))
        self.hint_sky_temple_key_combo.setItemText(2, QtWidgets.QApplication.translate("LogicSettingsWindow", "Show area and room name", None, -1))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.hint_tab), QtWidgets.QApplication.translate("LogicSettingsWindow", "Hints", None, -1))

