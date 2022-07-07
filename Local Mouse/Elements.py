from PyQt5.QtWidgets import QWidget, QMenuBar, QPushButton
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QColor
from globalVariables import *

# Creating widgets
class Rect(QWidget):

  # WIDGETS MUST BE DRAWN FIRST, AFTER THAT THEY CAN BE ADDED
  
  def __init__(self, widgetType, posX, posY, width, height, mainWidget, connection=''):
    super().__init__()
    self.newRect = QRect(posX, posY, width, height)
    self.setMaximumSize(width+1, height+1)
    self.widgetType = widgetType

    self.mainWidget = mainWidget
    self.connection = connection

    self.x = 0
    self.y = 0

  def paintEvent(self, event):
    painter = QPainter()
    painter.begin(self)
    painter.setPen(QColor(0, 0, 0))
    painter.drawRect(self.newRect)
    painter.end()

  def mousePressEvent(self, event):
    if self.widgetType == 'MouseArea':
      print('Okay')
      self.x = event.pos().x()
      self.y = event.pos().y()
    if self.widgetType == 'MouseLeftButton':
      print('Left button pressed')
      self.connection.sendMouseOperation(button = 'left')
    if self.widgetType == 'MouseRightButton':
      print('Right button pressed')
      self.connection.sendMouseOperation(button = 'right')

  def mouseMoveEvent(self, event):
    if self.widgetType == 'MouseArea':
      print('Moving')
      self.connection.sendMouseOperation(x = event.pos().x() - self.x, y = event.pos().y() - self.y)

# Creating menu bars
class MenuBar(QMenuBar):

  def __init__(self, mainWidget):
    super().__init__()

    self.mainWidget = mainWidget

  def showChosenUIElement(self, widgetToShow):
    self.mainWidget.removeWidget(self.mainWidget.currentWidget())
    self.mainWidget.addWidget(widgetToShow)

# Creating buttons
class Button(QPushButton):

  def __init__(self, buttonName, buttonText):
    super().__init__(buttonText)

    self.buttonName = buttonName

  def onClick(self, variables, connection, **lineEdits):
    if self.buttonName == 'SaveGeneralSettings':
      file = open(SETTINGS_FILE_NAME, 'w')
      for name, value in lineEdits.items():
        file.write(name + ': ' + '[' + value.text() + ']' + '\n')
        variables[name] = value.text()
      file.close()
      connection.setHostAndPort(variables['Connection'], int(variables['Port']))