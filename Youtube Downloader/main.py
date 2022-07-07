# polish characters
from __future__ import unicode_literals

from _ast import arg

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QComboBox
from PyQt5 import QtCore

from pytube import YouTube


class YDA(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pathEdt = QLineEdit()
        self.urlEdt = QLineEdit()
        self.video = QPushButton()
        self.audio = QPushButton()
        self.error = QLabel()
        self.afterDownload = QLabel()
        # video - 0, audio - 1
        self.vora = 0
        self.downloadList = QComboBox()
        # index from list to downloa
        self.downloadIndex = 0
        self.mime_type = ''
        self.resolution = ''
        self.fps = 0
        self.video_codec = ''
        self.audio_codec = ''
        self.progressive = False
        self.abr = ''
        self.interface()

    def interface(self):

        pathText = QLabel('Path', self)
        urlText = QLabel('URL', self)
        self.error = QLabel('Error has occurred. Check path and url.')
        self.afterDownload = QLabel('File downloaded succesfully!')
        self.error.hide()
        self.afterDownload.hide()

        pathText.setStyleSheet('font-size: 20px;')
        pathText.setAlignment(QtCore.Qt.AlignCenter)
        urlText.setStyleSheet('font-size: 20px;')
        urlText.setAlignment(QtCore.Qt.AlignCenter)

        self.error.setStyleSheet('font-size: 15px; color: red;')
        self.afterDownload.setStyleSheet('font-size: 15px; color: green;')

        self.downloadList.setStyleSheet('font-size: 10px;')

        submit = QPushButton('Download', self)
        self.video = QPushButton('Video', self)
        self.audio = QPushButton('Only audio', self)

        self.video.setStyleSheet('font-size: 15px;')
        self.audio.setStyleSheet('font-size: 15px;')

        ukladT = QGridLayout()
        ukladT.addWidget(pathText, 0, 0)
        ukladT.addWidget(urlText, 0, 1)
        ukladT.addWidget(self.pathEdt, 1, 0)
        ukladT.addWidget(self.urlEdt, 1, 1)
        ukladT.addWidget(self.video, 2, 0)
        ukladT.addWidget(self.audio, 2, 1)
        ukladT.addWidget(self.downloadList, 3, 0, 1, 2)
        ukladT.addWidget(submit, 4, 0, 1, 2)
        ukladT.addWidget(self.error, 5, 0, 1, 2)
        ukladT.addWidget(self.afterDownload, 5, 0, 1, 2)

        self.setLayout(ukladT)
        submit.clicked.connect(self.download)
        self.video.clicked.connect(self.videoButton)
        self.video.clicked.connect(self.downloadListFill)
        self.audio.clicked.connect(self.audioButton)
        self.audio.clicked.connect(self.downloadListFill)
        self.downloadList.activated[str].connect(self.listClick)

        self.resize(700, 180)
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QIcon('YDAicon.ico'))
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def download(self):
        path = self.pathEdt.text()
        url = self.urlEdt.text()
        self.error.hide()
        self.afterDownload.hide()

        try:
            yt = YouTube(url)
            if self.vora == 0:
                if self.progressive:
                    yt.streams.filter(mime_type=self.mime_type, resolution=self.resolution,
                                      fps=self.fps, video_codec=self.video_codec,
                                      audio_codec=self.audio_codec, progressive=self.progressive).first().download(path)
                else:
                    yt.streams.filter(mime_type=self.mime_type, resolution=self.resolution,
                                      fps=self.fps, video_codec=self.video_codec,
                                      progressive=self.progressive).first().download(path)
            else:
                yt.streams.filter(mime_type=self.mime_type, abr=self.abr,
                                  audio_codec=self.audio_codec).first().download(path)
            self.afterDownload.show()
        except:
            self.error.show()
            print('error')

    def videoButton(self):
        self.vora = 0

        if self.vora == 0:
            self.video.setStyleSheet('font-size: 15px; background-color: #C8DAFF;')
            self.audio.setStyleSheet('font-size: 15px;')

    def audioButton(self):
        self.vora = 1

        if self.vora == 1:
            self.video.setStyleSheet('font-size: 15px;')
            self.audio.setStyleSheet('font-size: 15px; background-color: #C8DAFF;')

    def downloadListFill(self):
        url = self.urlEdt.text()
        self.error.hide()
        self.afterDownload.hide()

        try:
            yt = YouTube(url)

            self.downloadList.clear()

            if self.vora == 0:
                for i in range(len(yt.streams.filter(progressive=True))):
                    self.downloadList.addItem(str(yt.streams.filter(progressive=True)[i]))
                for i in range(len(yt.streams.filter(only_video=True))):
                    self.downloadList.addItem(str(yt.streams.filter(only_video=True)[i]))
            else:
                for i in range(len(yt.streams.filter(only_audio=True))):
                    self.downloadList.addItem(str(yt.streams.filter(only_audio=True)[i]))
        except:
            self.error.show()

    def listClick(self):
        items = str(self.downloadList.currentText())
        itemsList = items.split('"')

        try:
            if self.vora == 0:
                if len(itemsList) > 15:
                    self.audio_codec = itemsList[11]
                    self.progressive = itemsList[13]
                else:
                    self.progressive = itemsList[11]
                self.mime_type = itemsList[3]
                self.resolution = itemsList[5]
                self.fps = int(itemsList[7].rstrip('fps'))
                self.video_codec = itemsList[9]
                if self.progressive == 'True':
                    self.progressive = True
                else:
                    self.progressive = False
            else:
                self.mime_type = itemsList[3]
                self.abr = itemsList[5]
                self.audio_codec = itemsList[7]
        except:
            self.error.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = YDA()
    sys.exit(app.exec_())