from functions import *
import sys
from threading import Thread
from PyQt5 import uic, QtWidgets

app = QtWidgets.QApplication([])


class Screen:

    def __init__(self):
        self.__main = uic.loadUi('main_window.ui')

        self.__x = 0
        self.__y = 0
        self.__cursor = Thread(target=self.__get_position, name='Cursor Position')
        self.__cursor.start()

        self.__actions = []

        self.__running = False
        self.__moving = Thread(target=self.__running_actions, name='Running Actions')
        self.__moving.start()

        # Linking Button functions
        self.__main.ButtonAdd.clicked.connect(self.__function_show_add)
        self.__main.ButtonDelete.clicked.connect(self.__delete_item)
        self.__main.ButtonClear.clicked.connect(self.__clear_list)
        self.__main.ButtonPlay.clicked.connect(self.__function_run)

        self.__main.ButtonCancel.clicked.connect(self.__function_cancel)
        self.__main.ButtonOk.clicked.connect(self.__function_ok)

        self.__main.ButtonOptions.clicked.connect(self.__function_show_options)
        self.__main.ButtonOptionsCancel.clicked.connect(self.__function_cancel)

        self.__main.ButtonHelp.clicked.connect(self.__function_show_help)
        self.__main.ButtonHelpCancel.clicked.connect(self.__function_cancel)

        self.__main.show()

    def __get_position(self):
        while True:
            sleep(0.1)
            self.__x = position()[0]
            self.__y = position()[1]
            self.__main.LabelPosition.setText(f'Cursor Position:\nX:{self.__x}\nY:{self.__y}')

            if app.activeWindow() is None and app.applicationState() > 2:
                sys.exit()

    def __running_actions(self):

        while True:
            sleep(0.1)
            if self.__running:
                for item in self.__actions:
                    if item[0] == 'Click':
                        execute_action(item, self.__running, click)
                    elif item[0] == 'Right Click':
                        execute_action(item, self.__running, rightClick)
                    elif item[0] == 'Middle Click':
                        execute_action(item, self.__running, middleClick)
                    elif item[0] == 'Double Click':
                        execute_action(item, self.__running, doubleClick)
                if self.__running:
                    self.__function_run()

            else:
                pass

            if app.activeWindow() is None and app.applicationState() > 2:
                sys.exit()

    def __function_show_add(self):
        self.__main.StackedWidget.setCurrentIndex(1)

    def __function_cancel(self):
        self.__main.ComboBox.setCurrentIndex(0)
        self.__main.InputPosX.clear()
        self.__main.InputPosY.clear()
        self.__main.SpinBoxInterval.setValue(0.50)
        self.__main.SpinBoxTimes.setValue(1)
        self.__main.CheckBox.setChecked(False)
        self.__main.InputWrite.clear()
        self.__main.ErrorPos.setText('')
        self.__main.ErrorWrite.setText('')
        self.__main.StackedWidget.setCurrentIndex(0)

    def __function_ok(self):
        error = 0
        self.__main.ErrorPos.setText('')
        self.__main.ErrorWrite.setText('')

        if len(self.__main.InputPosX.text()) == 0 or len(self.__main.InputPosY.text()) == 0:
            error += 1
            self.__main.ErrorPos.setText('*Missing Position X or Y!')

        else:
            list = [str(self.__main.ComboBox.currentText()),
                    int(self.__main.InputPosX.text()),
                    int(self.__main.InputPosY.text()),
                    float(self.__main.SpinBoxInterval.value()),
                    int(self.__main.SpinBoxTimes.value())]

            if self.__main.CheckBox.isChecked():
                if len(self.__main.InputWrite.text()) == 0:
                    error += 1
                    self.__main.ErrorWrite.setText('*There is not enough text to write!')
                else:
                    list.append(str(self.__main.InputWrite.text()))

            if error == 0:
                self.__actions.append(list)
                self.__function_cancel()
                self.__reload_list()
                print(self.__actions)

    def __function_run(self):
        if not self.__running and len(self.__actions) > 0:
            self.__running = True
            self.__main.ButtonPlay.setText('Stop')
        else:
            self.__main.ButtonPlay.setText('Play')
            self.__running = False

    def __reload_list(self):
        self.__main.ListWidget.clear()
        for item in self.__actions:
            self.__main.ListWidget.addItem(str(item))

    def __delete_item(self):
        if len(self.__actions) > 0:
            self.__actions.pop(self.__main.ListWidget.currentRow())
            self.__reload_list()
        else:
            pass

    def __clear_list(self):
        self.__main.ListWidget.clear()
        self.__actions.clear()

    def __function_show_options(self):
        self.__main.StackedWidget.setCurrentIndex(2)

    def __function_show_help(self):
        self.__main.StackedWidget.setCurrentIndex(3)
