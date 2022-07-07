import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QCursor
from decimal import Decimal
import math as Math

WIDTH = 400
HEIGHT = 600

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Simple Calculator')
        self.setFixedSize(QSize(WIDTH, HEIGHT))

        appWidget = QWidget()
        self.setCentralWidget(appWidget)

        self.mainLayout = QVBoxLayout()
        appWidget.setLayout(self.mainLayout)

    def addWidget(self, widget):
        self.mainLayout.addWidget(widget)

    def addLayout(self, layout):
        self.mainLayout.addLayout(layout)

# Main component of the application
class Calculator():

    def __init__(self):
        self.component = QVBoxLayout()
        self.buttonsLayout = QVBoxLayout()
        self.currentNumber = []
        self.values = []
        self.memoryValue = 0
        self.arithmeticSign = ''

        self.resultsDisplay = ResultsDisplay()

        self.component.addWidget(self.resultsDisplay)
        self.component.addLayout(self.buttonsLayout)

    def addButtons(self, *buttons):
        """
        Adds buttons to the app's GUI
        
        Arguments:
        buttons -- characters in a list (one row equals one list)
        """
        for row in buttons:
            buttonsRow = QHBoxLayout()
            for element in row:
                button = Button(element, self)
                buttonsRow.addWidget(button)
            self.buttonsLayout.addLayout(buttonsRow)

    # Adds sign (number or arithmetic sign) and executes specific task
    def addSign(self, value):
        """
        Checks whether sign that has to be added to Calculator is a number or
        a "normal sign" and then executes mathematical task assigned to it.

        Arguments:
        value -- string character representing a number or a matematical sign 
        """
        if value.isnumeric():
            self.currentNumber.append(value)

        elif value in ['/', 'x', '-', '+']:
            if len(self.currentNumber) > 0:
                self.values.append(Decimal(''.join(self.currentNumber)))
            self.currentNumber = []
            self.arithmeticSign = value

        elif value == '.':
            self.currentNumber.append('.')
            pass

        elif value == '=':
            if len(self.values) > 0 and len(self.currentNumber) > 0 and self.arithmeticSign == '':
                self.values[0] = Decimal(''.join(self.currentNumber))

            elif len(self.currentNumber) > 0:
                self.values.append(Decimal(''.join(self.currentNumber)))

            if len(self.values) >= 2 and self.arithmeticSign != '':
                self.values[0] = self.artihmeticOperation(self.arithmeticSign)
                self.memoryValue = self.values.pop()

            elif self.arithmeticSign != '':
                self.values[0] = self.artihmeticOperation(self.arithmeticSign, 
                    self.values[0], self.memoryValue)

            self.currentNumber = []

        elif value == '<':
            if len(self.currentNumber) > 0:
                self.currentNumber.pop()

        elif value == 'C':
            self.values.clear()
            self.currentNumber.clear()
            self.arithmeticSign = ''

        # Updates graphical results display
        try:
            if len(self.values) > 0:
                if self.values[0] > int(self.values[0]):
                    self.resultsDisplay.updateDisplay(self.values[0], 
                        self.arithmeticSign + ' ' + ''.join(self.currentNumber))
                else:
                    self.resultsDisplay.updateDisplay(int(self.values[0]),
                        self.arithmeticSign + ' ' + ''.join(self.currentNumber))
            else:
                self.resultsDisplay.updateDisplay('0', ''.join(self.currentNumber))
        except:
            self.resultsDisplay.updateDisplay('Error', '')

        print(self.currentNumber)
        print(self.values)

    def artihmeticOperation(self, sign, a=None, b=None):
        """
        Returns: number value of a and b variable operation result

        Arguments:
        sign -- mathematical operation sign
        a -- first variable to perform operation
        b -- second variable to perform operation
        """

        def addition(a, b):
            return a + b

        def subtraction(a, b):
            return a - b

        def division(a, b):
            if b == 0:
                return 'Error'
            return a / b

        def multiplication(a, b):
            return a * b

        operations = {'+': addition, '-': subtraction, '/': division, 
            'x': multiplication}

        a = self.values[0] if a is None else a
        b = self.values[1] if b is None else b
        return operations[sign](a, b)

    def calculate(self):
        return 0

class Button(QPushButton):

    def __init__(self, value, calculator):
        super(Button, self).__init__()

        self.value = value

        self.setText(value)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.onClick)

    def onClick(self):
        calculator.addSign(self.value)

class ResultsDisplay(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
    
        self.setObjectName('resultsDisplay')

        # result and currentNumber have alignment set here, because text-align
        # in qss doesn't work
        self.result = QLabel('0')
        self.result.setObjectName('result')
        self.result.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.currentNumber = QLabel('')
        self.currentNumber.setObjectName('currentNumber')
        self.currentNumber.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout = QVBoxLayout()
        layout.addWidget(self.result)
        layout.addWidget(self.currentNumber)

        self.setLayout(layout)

    def updateDisplay(self, result, currentNumber):
        self.result.setText(str(result))
        self.currentNumber.setText(str(currentNumber))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # Reading and setting styles
    with open('styles/main.qss', 'r') as f:
        style = f.read()
        window.setStyleSheet(style)

    calculator = Calculator()
    calculator.addButtons([' ', ' ', 'C', '<'], ['7', '8', '9', '/'], ['4', '5', '6', 'x'], 
    ['1', '2', '3', '-'], ['0', '.', '=', '+'])
    window.addLayout(calculator.component)

    window.show()
    app.exec()