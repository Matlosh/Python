import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget, QPushButton, QMainWindow, QGridLayout, QVBoxLayout, QFileDialog, QSlider, QComboBox, QInputDialog, QLineEdit, QGraphicsDropShadowEffect
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QRect, Qt, QTimer, QFile
from PyQt5.QtGui import QRawFont, QFontDatabase, QFont, QColor

import moviepy
from moviepy.editor import VideoFileClip

app = QApplication([])

class VEApp():

  def __init__(self):
    # App window
    self.window = QWidget()

    # Layouts
    self.videoLayout = QHBoxLayout()
    self.sliderLayout = QHBoxLayout()
    self.controlsLayout = QHBoxLayout()
    self.boxLayout = QHBoxLayout()
    self.settingsLayout = QHBoxLayout()
    self.toolsLayout = QHBoxLayout()
    self.resultLayout = QVBoxLayout()
    self.mainLayout = QVBoxLayout()

    self.currentFileName = ''
    self.originalFile = True

    # Video and Player
    self.video = QVideoWidget()
    self.video.setFixedSize(300, 165)
    self.video.move(0, 0)
    self.player = QMediaPlayer()
    self.player.setVideoOutput(self.video)
    self.playerSlider = QSlider(Qt.Horizontal)

    self.timer = QTimer(interval=1000)

    QFontDatabase.addApplicationFont('fonts/MontserratAlternates-Regular.ttf')
    self.primaryFont = QFont('Montserrat Alternates')

    self.shadow = QGraphicsDropShadowEffect(blurRadius = 3, xOffset = 0, yOffset = 0, color = QColor(255, 255, 255, 150))

    # Buttons
    self.buttons = {
      'setVideo': self.addButton('Set video', 'background-color: #6620c9; border-radius: 12px; border: 1px solid #4d1897; color: #ffffff; font-size: 12px; padding: 5px 36px;'),
      'deleteVideo': self.addButton('Delete video', 'background-color: #198754; border-radius: 12px; border: 1px solid #13653f; color: #ffffff; font-size: 12px; padding: 5px 36px;'),
      'chooseFile': self.addButton('Choose file to edit', 'background-color: #3369ff; border-radius: 12px; border: 1px solid #264fbf; color: #ffffff; font-size: 12px; padding: 5px 36px;')
    }

    # Play and pause buttons
    self.controls = {
      'play': self.addButton('Play', 'background-color: #dc3545; border-radius: 12px; border: 1px solid #a52834; color: #ffffff; font-size: 12px; padding: 5px 36px;'),
      'pause': self.addButton('Pause', 'background-color: #fd7e14; border-radius: 12px; border: 1px solid #dd6e12; color: #ffffff; font-size: 12px; padding: 5px 36px;'),
      'volUp': self.addButton('Volume Up', 'background-color: #ffc107; border-radius: 12px; border: 1px solid #dfa906; color: #ffffff; font-size: 12px; padding: 5px 36px;'),
      'volDown': self.addButton('Volume Down', 'background-color: #20c997; border-radius: 12px; border: 1px solid #1cb084; color: #ffffff; font-size: 12px; padding: 5px 24px;')
    }

    # Mainly slaider and video lengths
    self.playerControls = {
      'videoCurrentTime': self.addButton('0:00', 'border: 2px solid white; color: white; height: 20px; width: 40px;'),
      'videoLength': self.addButton('0:00', 'border: 2px solid white; color: white; height: 20px; width: 40px;')
    }

    # Texts
    self.texts = {
      'result': self.addText('', 'font-size: 1px;') 
    }

    # Widgets with video editing settings
    self.editVideoSettings = {
      'tools': self.addComboBox('border: 2px solid #ffe4B3; color: #ffffff; font-size: 12px; padding: 3px 12px;', 'Margin', 'Color change'),
      'fileName': self.addLineEdit('File name...', 'border-radius: 12px; border: 2px solid #f5b3ff; color: #ffffff; font-size: 12px; padding: 5px 36px;', 150),
      'submit': self.addButton('Submit changes', 'background-color: #e59626; border-radius: 12px; border: 1px solid #c88321; color: #ffffff; font-size: 12px; padding: 5px 36px;')
    }

    #################################
    # STREFA BLEDOW
    #
    # x2 przycisniecie na setVideo psuje slider
    # przycisk 'submit' nie może być pusty
    # po potwierdzeniu zmian pola się nie resetują
    # pasek nie zmienia wartości jeśli jest przesunięty (dopiero zmienia po odpaleniu)
    #
    #################################

    self.startSettings()

  # Values set on start of the app
  def startSettings(self):
    self.window.setWindowTitle('Video Editor')
    self.window.setGeometry(100, 100, 600, 400)
    self.window.move(60, 15)
    self.window.setStyleSheet('background-color: #202124;')

  # Creates Push Button and returns it
  def addButton(self, buttonValue, cssValue=''):
    button = QPushButton(buttonValue)
    button.setStyleSheet(cssValue)
    button.setFont(self.primaryFont)
    button.setGraphicsEffect(self.shadow)
    return button

  # Creates Text and returns it
  def addText(self, textValue, cssValue=''):
    text = QLabel(textValue)
    text.setStyleSheet(cssValue)
    text.setFont(self.primaryFont)
    text.setGraphicsEffect(self.shadow)
    return text

  # Creates Combo Box and returns it
  def addComboBox(self, cssValue='', *items):
    comboBox = QComboBox()
    comboBox.setStyleSheet(cssValue)
    comboBox.addItems(items)
    comboBox.setFont(self.primaryFont)
    comboBox.setGraphicsEffect(self.shadow)
    return comboBox

  # Creates Line Edit and returns it
  def addLineEdit(self, placeHolderText='', cssValue='', maximumWidth=80):
    lineEdit = QLineEdit()
    lineEdit.setStyleSheet(cssValue)
    lineEdit.setPlaceholderText(placeHolderText)
    lineEdit.setMaximumWidth(maximumWidth)
    lineEdit.setFont(self.primaryFont)
    return lineEdit

  # Plays video
  def playVideo(self):
    self.player.play()
    self.playerSlider.setMaximum(self.player.duration())
    self.player.setVolume(50) # Delete this later
    time = self.addButton(str((self.player.duration() // 1000) // 60) + ':' + str((self.player.duration() // 1000) - ((self.player.duration() // 1000) // 60) * 60), 'border: 2px solid white; color: white; height: 20px; width: 40px;')
    self.sliderLayout.replaceWidget(self.playerControls['videoLength'], time)
    self.playerControls['videoLength'] = time
    self.timer.start()

  # Pauses video
  def pauseVideo(self):
    self.player.pause()
    print(self.player.position())
    self.timer.stop()

  # Makes video louder
  def volumeUp(self):
    self.player.setVolume(self.player.volume() + 10)

  # Makes video quieter
  def volumeDown(self):
    self.player.setVolume(self.player.volume() - 10)

  # Event on "Set video" button
  def setVideo(self):
    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.currentFileName)))
    self.player.setPosition(0)
    self.video.show()
    self.player.play()
    self.player.pause()

  # Event on "Delete video" button
  def deleteVideo(self):
    self.player.stop()
    self.player.setMedia(QMediaContent())
    if self.originalFile == False:
      if QFile.remove(self.currentFileName):
        print('Deleted!')
      else:
        print('Not deleted :(')

  # Event on "Choose file to edit" button
  def openFile(self):
    if self.originalFile == False:
      self.deleteVideo()
    fileName = QFileDialog.getOpenFileName()
    self.texts['selectedFileName'] = self.addText(fileName[0], 'color: red;')
    self.resultLayout.removeWidget(self.texts['result'])
    self.texts['result'] = self.texts['selectedFileName']
    self.resultLayout.addWidget(self.texts['selectedFileName'])
    self.currentFileName = fileName[0]
    self.originalFile = True

  # Adds all buttons/texts/etc. to the corresponding layouts
  def addWidgets(self):
    self.videoLayout.addWidget(self.video)

    self.sliderLayout.addWidget(self.playerControls['videoCurrentTime'])
    self.sliderLayout.addWidget(self.playerSlider)
    self.sliderLayout.addWidget(self.playerControls['videoLength'])

    for keys in self.controls.keys():
      self.controlsLayout.addWidget(self.controls[keys])

    for keys in self.buttons.keys():
      self.boxLayout.addWidget(self.buttons[keys])

    for keys in self.editVideoSettings.keys():
      self.settingsLayout.addWidget(self.editVideoSettings[keys])

    # for test
    self.resultLayout.addWidget(self.texts['result'])

  # Moves video to time equals on slider
  def changeVideoTime(self):
    self.player.setPosition(self.playerSlider.value())

  # Changes video timer
  def changeTimer(self):
    currentSeconds = self.player.position() // 1000
    if currentSeconds - (currentSeconds // 60) * 60 < 10:
      time = self.addButton(str(currentSeconds // 60) + ':' + '0' + str(currentSeconds - (currentSeconds // 60) * 60), 'border: 2px solid white; color: white; height: 20px; width: 40px;')
    else:
      time = self.addButton(str(currentSeconds // 60) + ':' + str(currentSeconds - (currentSeconds // 60) * 60), 'border: 2px solid white; color: white; height: 20px; width: 40px;')
    self.sliderLayout.replaceWidget(self.playerControls['videoCurrentTime'], time)
    self.playerControls['videoCurrentTime'] = time
    self.playerSlider.blockSignals(True) # Blocking signals prevents from video lag when changing slider
    self.playerSlider.setValue(self.playerSlider.value() + 1000)
    self.playerSlider.blockSignals(False)

  # Returns clip with edited properties
  def editedClip(self, properties, currentTool):
    return {
      'Margin': VideoFileClip(self.currentFileName).margin(**properties),
      'Color change': VideoFileClip(self.currentFileName).margin(**properties) # change this later
    }.get(currentTool)

  # Submits changes and sends video to the moviepy edit
  def submitChanges(self):
    #clip1 = VideoFileClip(self.currentFileName).margin(**{'right': 20, 'left': 8, 'top': 4, 'color': (130, 130, 130)})
    
    currentTool = self.editVideoSettings['tools'].currentText()
    properties = {}
    for widgets in range(self.toolsLayout.count()):
      properties[self.toShowValues[currentTool][widgets]] = int(float(self.toolsLayout.takeAt(0).widget().text()))

    clip1 = self.editedClip(properties, currentTool)
    clip1.resize(width=480).write_videofile(self.editVideoSettings['fileName'].text() + '.mp4')
    self.deleteVideo()
    self.originalFile = False
    self.currentFileName = self.editVideoSettings['fileName'].text() + '.mp4'
    self.setVideo() # there

  # Shows specified values needed by choosed tools
  def changeTool(self):
    self.inputs = {
      'top': self.addLineEdit('Top value', 'border-radius: 12px; border: 2px solid #858585; color: #ffffff; font-size: 12px; padding: 2px 5px;', 100),
      'left': self.addLineEdit('Left value', 'border-radius: 12px; border: 2px solid #858585; color: #ffffff; font-size: 12px; padding: 2px 5px;', 100),
      'right': self.addLineEdit('Right value', 'border-radius: 12px; border: 2px solid #858585; color: #ffffff; font-size: 12px; padding: 2px 5px;', 100),
      'bottom': self.addLineEdit('Bottom value', 'border-radius: 12px; border: 2px solid #858585; color: #ffffff; font-size: 12px; padding: 2px 5px;', 100),
      #'color': ..., QColorDialog
      'opacity': self.addLineEdit('Opacity value', 'border-radius: 12px; border: 2px solid #858585; color: #ffffff; font-size: 12px; padding: 2px 5px;', 100)
    }
    
    self.toShowValues = {
      'Margin': ['top', 'left', 'right', 'bottom', 'opacity'],
      'Color change': ['top', 'bottom'] # there
    }

    currentTool = self.editVideoSettings['tools'].currentText()

    testLayout = QHBoxLayout()

    if currentTool in self.toShowValues.keys():
      for i in range(self.toolsLayout.count()):
        item = self.toolsLayout.takeAt(0).widget()
        self.toolsLayout.removeWidget(item)
      for items in self.toShowValues[currentTool]:
        self.toolsLayout.addWidget(self.inputs[items])

  # Main program function
  def run(self):
    self.addWidgets()

    self.mainLayout.addLayout(self.videoLayout)
    self.mainLayout.addLayout(self.sliderLayout)
    self.mainLayout.addLayout(self.controlsLayout)
    self.mainLayout.addLayout(self.boxLayout)
    self.mainLayout.addLayout(self.settingsLayout)
    self.mainLayout.addLayout(self.toolsLayout)
    self.mainLayout.addLayout(self.resultLayout)

    self.controls['play'].clicked.connect(lambda: self.playVideo())
    self.controls['pause'].clicked.connect(lambda: self.pauseVideo())
    self.controls['volUp'].clicked.connect(lambda: self.volumeUp())
    self.controls['volDown'].clicked.connect(lambda: self.volumeDown())
    self.buttons['setVideo'].clicked.connect(lambda: self.setVideo())
    self.buttons['deleteVideo'].clicked.connect(lambda: self.deleteVideo())
    self.buttons['chooseFile'].clicked.connect(lambda: self.openFile())
    self.playerSlider.valueChanged.connect(lambda: self.changeVideoTime())

    self.editVideoSettings['tools'].currentTextChanged.connect(lambda: self.changeTool())
    self.editVideoSettings['submit'].clicked.connect(lambda: self.submitChanges())

    # timer, interval
    
    self.timer.timeout.connect(lambda: self.changeTimer())
    self.window.setLayout(self.mainLayout)
    self.window.show()

application = VEApp()
application.run()

sys.exit(app.exec_())