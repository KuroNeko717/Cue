import sys
import PyQt5 
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class home_screen(QMainWindow):
    def __init__(self,ui_file):
        super(home_screen,self).__init__()
        uic.loadUi(ui_file,self)
        
        #Create Schedule
        self.create_schedule = None
        self.actioncreate_reminder_schedule_homescreen.triggered.connect(self.t_create_schedule)
        
        #Edit/view schedule
        self.edit_schedule = None
        self.actionedit_and_view_schedule_homescreen.triggered.connect(self.t_edit_schedule)
        
        self.show()

    #Edit/view schedule
    def t_create_schedule(self):
        if self.create_schedule is None:
            self.create_schedule = create_schedule("Ui_files\Schedule\Create_Form.ui")
            self.create_schedule.show()
        else:
            self.create_schedule.close()
            self.create_schedule = None
            
    #Edit/view schedule
    def t_edit_schedule(self):
        if self.edit_schedule is None:
            self.edit_schedule = edit_schedule("Ui_files\Schedule\Edit_Form.ui")
            self.edit_schedule.show()
        else:
            self.edit_schedule.close()
            self.edit_schedule = None


class create_schedule(QMainWindow):
    def __init__(self,ui_file):
        super(create_schedule,self).__init__()
        uic.loadUi(ui_file,self)
        
class edit_schedule(QMainWindow):
    def __init__(self,ui_file):
        super(create_schedule,self).__init__()
        uic.loadUi(ui_file,self)




app=QApplication([])

if __name__ == "__main__":
    window=home_screen("Ui_files\Home_Screen_Window.ui")
    app.exec_()

