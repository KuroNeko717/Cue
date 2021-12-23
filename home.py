import sys
import PyQt5 
from PyQt5 import QtGui,QtCore
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class home_screen(QMainWindow):
    def __init__(self,ui_file):
        super(home_screen,self).__init__()
        uic.loadUi(ui_file,self)
        
        #Create Schedule Menubar Action
        self.create_schedule = None
        self.actioncreate_s_hs.triggered.connect(self.t_create_schedule)
        
        #Edit/View Schedule Menubar Action
        self.vedit_schedule = None
        self.actionview_s_hs.triggered.connect(self.t_vedit_schedule)

        #Create Note Menubar Action
        self.create_note = None
        self.actioncreate_n_hs.triggered.connect(self.t_create_note)

        #View/ Edit Note Menubar Action
        self.vedit_note = None
        self.actionview_n_hs.triggered.connect(self.t_vedit_note)
        self.generate_schedule()

        self.show()

    #Schedule generation Function Calling
    def generate_schedule(self):

        for i in range(7):
            obj = schedule("timee", "do this")
            temp = obj.gen_schedule()
            self.verticalLayout.addWidget(temp)

    #Create schedule Menubar Action Form Open/Close
    def t_create_schedule(self):
        if self.create_schedule is None:
            self.create_schedule = create_schedule("Ui_files\\Schedules\\schedule_create_form.ui")
            self.create_schedule.show()
        else:
            self.create_schedule.close()
            self.create_schedule = None
            
    #Edit/view schedule Menubar Action Form Open/Close
    def t_vedit_schedule(self):
        if self.vedit_schedule is None:
            self.vedit_schedule = vedit_schedule("Ui_files\\Schedules\\schedule_edit_form.ui")
            self.vedit_schedule.show()
        else:
            self.vedit_schedule.close()
            self.vedit_schedule = None

    #Create Note Menubar Action Form Open/Close
    def t_create_note(self):
        if self.create_note is None:
            self.create_note = create_note("Ui_files\\Notes\\notes_create_form.ui")
            self.create_note.show()
        else:
            self.create_note.close()
            self.create_note = None

    #View/Edit Note Menubar Action Form Open/Close
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


class schedule(QMainWindow):
    
    def __init__(self, time, title):
        super(schedule,self).__init__()
        self.time = time
        self.title = title

    #Schedule generation
    def gen_schedule(self):
        
        self.frame = QtWidgets.QFrame()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 100))
        self.frame.setStyleSheet("background-color: rgb(44, 47, 51);\n" "color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(630, 30, 126, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontallayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontallayout.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout.setObjectName("horizontallayout")
        self.notification_on_checkbox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.notification_on_checkbox.setFont(font)
        self.notification_on_checkbox.setStyleSheet("color: rgb(213, 210, 255);")
        self.notification_on_checkbox.setObjectName("notification_on_checkbox")
        self.horizontallayout.addWidget(self.notification_on_checkbox)
        self.edit_button = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.edit_button.setFont(font)
        self.edit_button.setStyleSheet("color: rgb(213, 210, 255);")
        self.edit_button.setObjectName("edit_button")
        self.horizontallayout.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.delete_button.setFont(font)
        self.delete_button.setStyleSheet("color: rgb(213, 210, 255);")
        self.delete_button.setObjectName("delete_button")
        self.horizontallayout.addWidget(self.delete_button)
        self.time_label = QtWidgets.QLabel(self.frame)
        self.time_label.setGeometry(QtCore.QRect(10, 20, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: rgb(213, 210, 255);")
        self.time_label.setObjectName("time_label")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(160, 0, 20, 91))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.content_label = QtWidgets.QLabel(self.frame)
        self.content_label.setGeometry(QtCore.QRect(180, 10, 431, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.content_label.setFont(font)
        self.content_label.setStyleSheet("color: rgb(213, 210, 255);")
        self.content_label.setObjectName("content_label")
        self.readmore_button = QtWidgets.QPushButton(self.frame)
        self.readmore_button.setGeometry(QtCore.QRect(400, 60, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.readmore_button.setFont(font)
        self.readmore_button.setStyleSheet("color: rgb(213, 210, 255);")
        self.readmore_button.setObjectName("readmore_button")

        _translate = QtCore.QCoreApplication.translate
        self.notification_on_checkbox.setText(_translate("MainWindow", "ON"))
        self.edit_button.setText(_translate("MainWindow", "E"))
        self.delete_button.setText(_translate("MainWindow", "X"))
        self.time_label.setText(_translate("MainWindow", "{}".format(self.time)))
        self.content_label.setText(_translate("MainWindow", "{}".format(self.title)))
        self.readmore_button.setText(_translate("MainWindow", "Read More"))

        return self.frame


app=QApplication([])

if __name__ == "__main__":
    window=home_screen("Ui_files\Home_Screen_Window.ui")
    app.exec_()

