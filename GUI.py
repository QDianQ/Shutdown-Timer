from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, \
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QLabel, \
    QSpacerItem, QSizePolicy, QMessageBox, QAction, QMenu, qApp, QSystemTrayIcon, QStyle
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
import PC

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.exit_tray = None
        self.open_tray = None
        self.tray_menu = None
        self.tray_icon = None
        self.timer = None
        self.timeSB_seconds = None
        self.timeSB_minutes = None
        self.timeSB_hours = None
        self.cancelBtn = None
        self.okBtn = None
        self.statusPC = None
        self.icon = '.\source\icon\power-button.png'
        self.initUI()
        self.path = ''

    def initUI(self):

        self.setWindowTitle('Shutdown timer')
        self.setWindowIcon(QIcon(self.icon))

        # ======================== Initialization of objects =====================================#

        main_layout, time_layout_label, time_layout_spin = QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        central_layout, right_layout, left_layout = QVBoxLayout(), QVBoxLayout(), QVBoxLayout()

        self.tray_icon = QSystemTrayIcon()
        self.tray_menu = QMenu()

        self.open_tray = QAction("Open", self)
        # self.exit_tray = QAction("Exit", self)

        self.open_tray.triggered.connect(self.showNormal)
        # self.exit_tray.triggered.connect(self.closeTimer)

        self.statusPC = QComboBox()

        self.okBtn, self.cancelBtn = QPushButton("Ok"), QPushButton("Cancel")

        creator = QLabel("Created by Unfriendly")

        self.timeSB_hours, self.timeSB_minutes, self.timeSB_seconds = QSpinBox(), QSpinBox(), QSpinBox()

        vSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vSpacerMinimum = QSpacerItem(20,40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        central_widget = QWidget()



        #========================================================================================#

        # =========================== Set properties =============================================#
        creator.setAlignment(Qt.AlignRight)

        self.tray_icon.setIcon(QIcon(self.icon))
        self.tray_menu.addAction(self.open_tray)
        self.tray_menu.addAction(self.exit_tray)

        self.tray_icon.setContextMenu(self.tray_menu)


        self.statusPC.addItems(['Shutdown','Restart'])
        self.statusPC.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.statusPC.setMaximumSize(100, 999999)

        self.timeSB_hours.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeSB_minutes.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeSB_seconds.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeSB_hours.setMaximumSize(60, 999999)
        self.timeSB_minutes.setMaximumSize(60, 999999)
        self.timeSB_seconds.setMaximumSize(60, 999999)

        self.okBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.okBtn.clicked.connect(self.clickOK)

        self.cancelBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cancelBtn.clicked.connect(self.clickCancel)
        self.cancelBtn.setEnabled(False)


        # ========================================================================================#

        # ============================== Building layouts ========================================#
        central_layout.addLayout(main_layout)
        central_layout.addWidget(creator)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        left_layout.addItem(vSpacer)
        left_layout.addWidget(self.statusPC)
        left_layout.addItem(vSpacerMinimum)
        left_layout.addLayout(time_layout_label)
        left_layout.addLayout(time_layout_spin)
        left_layout.addItem(vSpacer)

        time_layout_label.addWidget(QLabel("Hours"))
        time_layout_label.addWidget(QLabel("Minutes"))
        time_layout_label.addWidget(QLabel("Seconds"))

        time_layout_spin.addWidget(self.timeSB_hours)
        time_layout_spin.addWidget(self.timeSB_minutes)
        time_layout_spin.addWidget(self.timeSB_seconds)

        right_layout.addItem(vSpacer)
        right_layout.addWidget(self.okBtn)
        right_layout.addWidget(self.cancelBtn)
        right_layout.addItem(vSpacer)

        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        self.tray_icon.show()

    def clickOK(self):
        self.timerStart()

        time = int(self.timeSB_hours.text()) * 60 * 60 + int(self.timeSB_minutes.text()) * 60 + int(self.timeSB_seconds.text())

        if self.statusPC.currentIndex() == 0:
            PC.shutdown(time)
        if self.statusPC.currentIndex() == 1:
            PC.reboot(time)

        self.okBtn.setEnabled(False)
        self.cancelBtn.setEnabled(True)

        self.statusPC.setEnabled(False)

        self.timeSB_seconds.setEnabled(False)
        self.timeSB_minutes.setEnabled(False)
        self.timeSB_hours.setEnabled(False)

    def clickCancel(self):

        PC.abortShutdown()

        self.cancelBtn.setEnabled(False)
        self.okBtn.setEnabled(True)

        self.statusPC.setEnabled(True)

        self.timeSB_seconds.setEnabled(True)
        self.timeSB_minutes.setEnabled(True)
        self.timeSB_hours.setEnabled(True)
        self.timer.stop()

    def timerStart(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.dip)
        self.timer.start(1000)


    def dip(self):

        seconds = int(self.timeSB_seconds.text())
        minutes = int(self.timeSB_minutes.text())
        hours = int(self.timeSB_hours.text())

        if seconds == 0 and minutes == 0 and hours == 0:
            self.timer.stop()
            return

        if seconds != 0:
            seconds -= 1
            self.timeSB_seconds.setValue(seconds)
        elif minutes != 0:
            seconds = 59
            minutes -= 1
            self.timeSB_seconds.setValue(seconds)
            self.timeSB_minutes.setValue(minutes)
        else:
            seconds = 59
            minutes = 59
            hours -= 1
            self.timeSB_seconds.setValue(seconds)
            self.timeSB_minutes.setValue(minutes)
            self.timeSB_hours.setValue(hours)

    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Should stop the timer?",
                                     QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            # self.timer.stop()
            PC.abortShutdown()
            event.accept()
        else:
            event.ignore()


    # def closeTimer(self):
    #     close = QMessageBox.question(self,
    #                                  "QUIT",
    #                                  "Should stop the timer?",
    #                                  QMessageBox.Yes | QMessageBox.No)
        # if close == QMessageBox.Yes:
        #     pass
        # else:
        #     pass

    def hideEvent(self, event):
        self.hide()



def start():

    app = QApplication([])

    mw = MainWindow()
    mw.setFixedSize(300, 200)
    mw.show()

    app.exec()