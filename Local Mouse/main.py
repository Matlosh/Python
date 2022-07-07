import sys
from PyQt5.QtGui import QTabletEvent
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QMenu, QVBoxLayout, QWidget, QStackedLayout, QPushButton, QGridLayout, QStackedWidget, QAction, QInputDialog, QLineEdit, QLabel
from PyQt5.QtCore import QPoint, QSize, QRect, QSettings
from globalVariables import *
from Elements import Rect, MenuBar, Button
from Connection import Connection

# Main application window
class MainWindow(QMainWindow):

  def __init__(self, x, y, appWidth, appHeight):
    super().__init__()
    self.setWindowTitle('Local Mouse Client App')
    self.setGeometry(x, y, appWidth, appHeight)
    self.setMinimumSize(appWidth, appHeight)
    self.setMaximumSize(appWidth, appHeight)

# App
class App:

  def __init__(self):
    self.mainWindow = MainWindow(100, 100, APP_WIDTH, APP_HEIGHT)

    self.stackedWidget = QStackedWidget()
    self.mousePanel = QWidget()
    self.settingsGeneralPanel = QWidget()
    self.mainWindow.setCentralWidget(self.stackedWidget)

    self.connection = Connection()

    self.variables = {}

    # self.stackedWidget.removeWidget(nazwaWidgetu)
    # self.stackedWidget.addWidget(nazwaWidgetu)

    self.loadVariables()
    self.setupUI()

  def loadVariables(self):
    try:
      file = open(SETTINGS_FILE_NAME, 'r')
      for line in file:
        name = ''
        value = ''
        isValue = False
        isName = True
        for character in line:
          if character == '[':
            isValue = True
          elif character == ']':
            isValue = False
          elif character == ' ':
            isName = False
          elif character != ':' and isName == True and isValue == False:
            name += character
          elif isValue == True:
            value += character
        self.variables[name] = value
      file.close()
      self.connection.setHostAndPort(self.variables['Connection'], int(self.variables['Port']))
    except:
      pass

  def setupUI(self):
    # Menu bar and items
    menuBar = MenuBar(self.stackedWidget)
    tools = menuBar.addMenu('Tools')
    mouse = tools.addAction('Mouse')
    settings = menuBar.addMenu('Settings')
    general = settings.addAction('General')
    self.mainWindow.setMenuBar(menuBar)

    # "Tools -> General" GUI
    mousePanelLayout = QVBoxLayout()

    mouseAreaLayout = QGridLayout()
    mouseArea = Rect('MouseArea', 0, 0, APP_WIDTH-40, APP_HEIGHT-240, self.stackedWidget, self.connection)
    mouseAreaLayout.addWidget(mouseArea, 0, 0)

    mouseButtonsLayout = QHBoxLayout()
    mouseLeftButton = Rect('MouseLeftButton', 0, 0, 170, 50, self.stackedWidget, self.connection)
    mouseRightButton = Rect('MouseRightButton', 0, 0, 170, 50, self.stackedWidget, self.connection)
    mouseButtonsLayout.addWidget(mouseLeftButton)
    mouseButtonsLayout.addWidget(mouseRightButton)

    mousePanelLayout.addLayout(mouseAreaLayout)
    mousePanelLayout.addLayout(mouseButtonsLayout)

    self.mousePanel.setLayout(mousePanelLayout)

    # "Settings -> General" GUI

    settingsGeneralLayout = QGridLayout()

    connectionIPLabel = QLabel("Server's IP")
    connectionIP = QLineEdit()
    settingsGeneralLayout.addWidget(connectionIPLabel, 0, 0)
    settingsGeneralLayout.addWidget(connectionIP, 0, 1)

    connectionPortLabel = QLabel("Server's Port")
    connectionPort = QLineEdit()
    settingsGeneralLayout.addWidget(connectionPortLabel, 1, 0)
    settingsGeneralLayout.addWidget(connectionPort, 1, 1)

    saveButton = Button('SaveGeneralSettings', 'Save')
    settingsGeneralLayout.addWidget(saveButton, 2, 0, 1, 2)

    self.settingsGeneralPanel.setLayout(settingsGeneralLayout)

    ## Signals

    self.stackedWidget.addWidget(self.mousePanel)
    mouse.triggered.connect(lambda: menuBar.showChosenUIElement(self.mousePanel))
    general.triggered.connect(lambda: menuBar.showChosenUIElement(self.settingsGeneralPanel))
    saveButton.pressed.connect(lambda: saveButton.onClick(self.variables, self.connection, Connection=connectionIP, Port=connectionPort))

  def show(self):
    self.mainWindow.show()

application = QApplication([])
app = App()
app.show()
sys.exit(application.exec_())