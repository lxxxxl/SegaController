#!/usr/bin/env python

import threading
from enum import Enum

from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout

)
from PyQt6.QtCore import (
    QTimer, QIODevice, QProcess,
    QJsonDocument, QJsonValue, 
    pyqtSignal
)
from PyQt6.QtSerialPort import QSerialPort

class Keys(Enum):
        """enum of keys on Sega controller"""
        UP      = 0
        DOWN    = 1
        LEFT    = 2
        RIGHT   = 3

        START   = 4
        MODE    = 5

        A       = 6
        B       = 7
        C       = 8

        X       = 9
        Y       = 10
        Z       = 11

        @classmethod
        def has_value(cls, value):
            return value in cls._value2member_map_

class MainWindow(QMainWindow):
    """Main application window"""

    # association of Sega key to keyboard key
    keyassoc = {
        Keys.UP:    'Up',
        Keys.DOWN:  'Down',
        Keys.LEFT:  'Left',
        Keys.RIGHT: 'Right',
        Keys.START: 'Return',
        Keys.MODE:  'BackSpace',
        Keys.A:     'z',
        Keys.B:     'x',
        Keys.C:     'c',
        Keys.X:     'a',
        Keys.Y:     's',
        Keys.Z:     'd'
    }

 
 
    # association of labels and corresponding controller buttons
    labelassoc = {}


    # Serial port device
    device = None
    # Serial port speed
    speed = None
    # Poll sleep not need
    # sleep = None

    def __init__(self):
        """init main window """
        super(MainWindow, self).__init__()

        self.setWindowTitle('Sega Controller')
        self.setFixedSize(200, 200)

        # setup layouts
        centralWidget = QWidget()
        vertical_layout = QVBoxLayout()
        centralWidget.setLayout(vertical_layout)
        self.setCentralWidget(centralWidget)

        self.lbl_connected = QLabel('Not Connected')
        self.lbl_connected.setStyleSheet('color: red')
        vertical_layout.addWidget(self.lbl_connected)


        # layout for button labels
        horizontal_widget = QWidget()
        horizontal_layout = QHBoxLayout()
        horizontal_widget.setLayout(horizontal_layout)
        vertical_layout.addWidget(horizontal_widget)

        vertical_widget1 = QWidget()
        vertical_layout1 = QVBoxLayout()
        vertical_widget1.setLayout(vertical_layout1)
        vertical_widget2 = QWidget()
        vertical_layout2 = QVBoxLayout()
        vertical_widget2.setLayout(vertical_layout2)

        horizontal_layout.addWidget(vertical_widget1)
        horizontal_layout.addWidget(vertical_widget2)

        for key in [Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT, Keys.START, Keys.MODE]:
            self.labelassoc[key] = QLabel(Keys(key).name)
            vertical_layout1.addWidget(self.labelassoc[key])
        for key in [Keys.A, Keys.B, Keys.C, Keys.X, Keys.Y, Keys.Z]:
            self.labelassoc[key] = QLabel(Keys(key).name)
            vertical_layout2.addWidget(self.labelassoc[key])

        # Setup button
        btn_setup = QPushButton('Setup')
        btn_setup.clicked.connect(self.setup_click)
        vertical_layout.addWidget(btn_setup)

        # Connection timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)
        self.timer.start(1 * 1000) # fire every 1 second

        # Serial port instance
        self.port = QSerialPort()
        self.port_connected = False
        self.port.readyRead.connect(self.serial_read)
        self.port.errorOccurred.connect(self.serial_error)

        # Configuration window
        self.config_window = ConfigWindow()
        self.config_window.config_changed.connect(self.config_changed)
        self.config_window.read_config()
        self.timeout()  # call timeout to not wait for first timer tick

    def write_config(self):
        """Write config file"""
        pass

    def port_connect(self):
        """Connect to port"""
        pass
    
    def timeout(self):
        """Process connection timer"""
        if self.port_connected:
            self.timer.stop()
            return
        if self.device != None:
            self.port.setPortName(self.device)
            self.port.setBaudRate(self.speed)
            self.port_connected = self.port.open(QIODevice.OpenModeFlag.ReadOnly)
            if self.port_connected:
                self.lbl_connected.setText('Connected')
                self.lbl_connected.setStyleSheet('font-weight: bold')

    def setup_click(self):
        """Setup button click slot"""
        
        self.config_window.show()

    def config_changed(self, device, speed):
        """Apply new config data"""
        self.device = device
        self.speed = speed

    def serial_error(self, error):
        """Handle serial device disconnect"""
        if error == QSerialPort.SerialPortError.ReadError and self.port_connected:
            self.port.close()
            self.port_connected = False
            self.lbl_connected.setText('Not conencted')
            self.lbl_connected.setStyleSheet('color: red')
            self.timer.start(1 * 1000) # fire every 1 second

    def serial_read(self):
        """Thread for reading data from serial port"""
        b = self.port.read(128)
        if len(b) == 0:
            return
        # key code stored in first 4 bits
        key = b[0] & 0x0F
        # key press status stored in 7nth bit (1 - pressed, 0 - released)
        keypressed = b[0] & 0x80
        if not Keys.has_value(key):
            return
        if keypressed:
            self.keydown(Keys(key))
        else:
            self.keyup(Keys(key))

    def keydown(self, key):
        """process key press"""
        if not key in self.keyassoc:
            return
        keyevent = self.keyassoc[key]
        QProcess.startDetached('xdotool', ['keydown', keyevent])
        #print(f'xdotool keydown {keyevent}')
        self.labelassoc[key].setStyleSheet('font-weight: bold')

    def keyup(self, key):
        """process key release"""
        if not key in self.keyassoc:
            return
        keyevent = self.keyassoc[key]
        QProcess.startDetached('xdotool', ['keyup', keyevent])
        #print(f'xdotool keyup {keyevent}')
        self.labelassoc[key].setStyleSheet('font-weight: normal')

    def run_process(self, cmd):
        process = QProcess()
        process.start(cmd)
        process.waitForFinished()


class ConfigWindow(QMainWindow):
    """Configuration window"""

    # config read/change signal
    config_changed = pyqtSignal(str, int)

    def __init__(self):
        """init configuration window """
        super(ConfigWindow, self).__init__()

        self.setWindowTitle('Configuration')
        self.setFixedSize(150, 150)

        # setup layout
        centralWidget = QWidget()
        vertical_layout = QVBoxLayout()
        centralWidget.setLayout(vertical_layout)
        self.setCentralWidget(centralWidget)

        # add controls
        lbl_device = QLabel('Device')
        self.edit_device = QLineEdit()
        lbl_speed = QLabel('Speed')
        self.edit_speed = QLineEdit()
        btn_save = QPushButton('Save')

        btn_save.clicked.connect(self.save_click)

        vertical_layout.addWidget(lbl_device)
        vertical_layout.addWidget(self.edit_device)
        vertical_layout.addWidget(lbl_speed)
        vertical_layout.addWidget(self.edit_speed)
        vertical_layout.addWidget(btn_save)

    def read_config(self):
        """Read config file"""
        with open('config.json','r') as f:
            data = f.read()

        json_document = QJsonDocument.fromJson(data.encode())
        json = json_document.object()

        if 'device' in json:
            self.edit_device.setText(json['device'].toString())
        if 'speed' in json:
            self.edit_speed.setText(str(json['speed'].toInt()))

        # emit signal with new config data
        self.config_changed.emit(
            self.edit_device.text(),
            int(self.edit_speed.text(), 10))

    def save_click(self):
        """Save config to file"""
        json = {}
        json['device'] = QJsonValue(self.edit_device.text())
        json['speed'] = QJsonValue(int(self.edit_speed.text(), 10))

        json_document = QJsonDocument()
        json_document.setObject(json)

        with open('config.json','w') as f:
            f.write(bytes(json_document.toJson()).decode())

        # emit signal with new config data
        self.config_changed.emit(
            self.edit_device.text(),
            int(self.edit_speed.text(), 10))

        self.close()

app = QApplication([])
w = MainWindow()
w.show()
app.exec()