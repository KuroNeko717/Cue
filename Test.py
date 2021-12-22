import sys
import PyQt5 
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class home_screen(QMainWindow):
    def __init__(self,ui_file):
        super(home_screen,self).__init__()
        uic.loadUi(ui_file,self)
        self.create_schedule = None
        self.button_readmore_schedule_homescreen.clicked.connect(self.o_create_schedule)
        self.show()

    def o_create_schedule(self):
        if self.create_schedule is None:
            self.create_schedule = create_schedule("Ui_files\Read_More_Form.ui")
            self.create_schedule.show()
        else:
            self.create_schedule.close()
            self.create_schedule = None


class create_schedule(QMainWindow):
    def __init__(self,ui_file):
        super(create_schedule,self).__init__()
        uic.loadUi(ui_file,self)




app=QApplication([])

if __name__ == "__main__":
    window=home_screen("Ui_files\Home_Screen_Window.ui")
    app.exec_()

