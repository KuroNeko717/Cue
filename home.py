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
        self.actioncreate_s_hs.triggered.connect(self.t_create_schedule)
        
        #Edit/View Schedule
        self.vedit_schedule = None
        self.actionview_s_hs.triggered.connect(self.t_vedit_schedule)

        #Create Note
        self.create_note = None
        self.actioncreate_n_hs.triggered.connect(self.t_create_note)

        #View/ Edit Note
        self.vedit_note = None
        self.actionview_n_hs.triggered.connect(self.t_vedit_note)
        
        self.show()

    #Create schedule
    def t_create_schedule(self):
        if self.create_schedule is None:
            self.create_schedule = create_schedule("Ui_files\\Schedules\\schedule_create_form.ui")
            self.create_schedule.show()
        else:
            self.create_schedule.close()
            self.create_schedule = None
            
    #Edit/view schedule
    def t_vedit_schedule(self):
        if self.vedit_schedule is None:
            self.vedit_schedule = vedit_schedule("Ui_files\\Schedules\\schedule_edit_form.ui")
            self.vedit_schedule.show()
        else:
            self.vedit_schedule.close()
            self.vedit_schedule = None

    #Create Note
    def t_create_note(self):
        if self.create_note is None:
            self.create_note = create_note("Ui_files\\Notes\\notes_create_form.ui")
            self.create_note.show()
        else:
            self.create_note.close()
            self.create_note = None

    #View/Edit Note
    def t_vedit_note(self):
        if self.vedit_note is None:
            self.vedit_note = vedit_note("Ui_files\\Notes\\notes_view_form.ui")
            self.vedit_note.show()
        else:
            self.vedit_note.close()
            self.vedit_note = None


class create_schedule(QMainWindow):
    def __init__(self,ui_file):
        super(create_schedule,self).__init__()
        uic.loadUi(ui_file,self)
        
class vedit_schedule(QMainWindow):
    def __init__(self,ui_file):
        super(vedit_schedule,self).__init__()
        uic.loadUi(ui_file,self)

class create_note(QMainWindow):
    def __init__(self,ui_file):
        super(create_note,self).__init__()
        uic.loadUi(ui_file,self)

class vedit_note(QMainWindow):
    def __init__(self,ui_file):
        super(vedit_note,self).__init__()
        uic.loadUi(ui_file,self)


app=QApplication([])

if __name__ == "__main__":
    window=home_screen("Ui_files\Home_Screen_Window.ui")
    app.exec_()

