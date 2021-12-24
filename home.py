import sys
import PyQt5 
from PyQt5 import QtGui,QtCore
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import sqlite3
from functools import partial

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
        
        #database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        
        #frames variable
        self.frames = []
        
        #View/ Edit Note Menubar Action
        self.vedit_note = None
        self.actionview_n_hs.triggered.connect(self.t_vedit_note)
        self.generate_schedule()
        self.setup()
        self.show()
    
        

    def setup(self):
        self.c.execute("create table if not exists Schedule(id integer primary key, name varchar(250) not null, create_date timestamp not null, occurance varchar(50) not null, discription text not null, is_notify boolean not null)")

    #Schedule generation Function Calling
    def generate_schedule(self):
        
        data = self.c.execute("select * from Schedule where create_date >= date('now','-1 day') and create_date <= date('now','+1 day')")
        
        for i in data:
            temp = self._gen_schedule(i[1], i[4], i[0])
            self.frames.append(temp)
            self.verticalLayout.addWidget(temp)

    def _gen_schedule(self,time,title,id):
        
        frame = QtWidgets.QFrame()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
        frame.setSizePolicy(sizePolicy)
        frame.setMinimumSize(QtCore.QSize(0, 100))
        frame.setStyleSheet("background-color: rgb(44, 47, 51);\n" "color: rgb(255, 255, 255);")
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName("frame")
        horizontalLayoutWidget = QtWidgets.QWidget(frame)
        horizontalLayoutWidget.setGeometry(QtCore.QRect(630, 30, 126, 31))
        horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        horizontallayout = QtWidgets.QHBoxLayout(horizontalLayoutWidget)
        horizontallayout.setContentsMargins(0, 0, 0, 0)
        horizontallayout.setObjectName("horizontallayout")
        notification_on_checkbox = QtWidgets.QCheckBox(horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        notification_on_checkbox.setFont(font)
        notification_on_checkbox.setStyleSheet("color: rgb(213, 210, 255);")
        notification_on_checkbox.setObjectName("notification_on_checkbox")
        horizontallayout.addWidget(notification_on_checkbox)
        edit_button = QtWidgets.QToolButton(horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        edit_button.setFont(font)
        edit_button.setStyleSheet("color: rgb(213, 210, 255);")
        edit_button.setObjectName("edit_button")
        horizontallayout.addWidget(edit_button)
        delete_button = QtWidgets.QToolButton(horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        delete_button.setFont(font)
        delete_button.setStyleSheet("color: rgb(213, 210, 255);")
        delete_button.setObjectName("delete_button")
        horizontallayout.addWidget(delete_button)
        time_label = QtWidgets.QLabel(frame)
        time_label.setGeometry(QtCore.QRect(10, 20, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        time_label.setFont(font)
        time_label.setStyleSheet("color: rgb(213, 210, 255);")
        time_label.setObjectName("time_label")
        line = QtWidgets.QFrame(frame)
        line.setGeometry(QtCore.QRect(160, 0, 20, 91))
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        content_label = QtWidgets.QLabel(frame)
        content_label.setGeometry(QtCore.QRect(180, 10, 431, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        content_label.setFont(font)
        content_label.setStyleSheet("color: rgb(213, 210, 255);")
        content_label.setObjectName("content_label")
        readmore_button = QtWidgets.QPushButton(frame)
        readmore_button.setGeometry(QtCore.QRect(400, 60, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        readmore_button.setFont(font)
        readmore_button.setStyleSheet("color: rgb(213, 210, 255);")
        readmore_button.setObjectName("readmore_button")

        _translate = QtCore.QCoreApplication.translate
        notification_on_checkbox.setText(_translate("MainWindow", "ON"))
        edit_button.setText(_translate("MainWindow", "E"))
        delete_button.setText(_translate("MainWindow", "X"))
        time_label.setText(_translate("MainWindow", "{}".format(time)))
        content_label.setText(_translate("MainWindow", "{}".format(title)))
        readmore_button.setText(_translate("MainWindow", "Read More"))
        readmore_button.clicked.connect(partial(self.onclick_readMore, id))
        return frame
    
    def onclick_readMore(self,id):
        x = self.c.execute("select * from Schedule where id = {}".format(id))
        for i in x:
           print(i)
        self.readmore_button_o= None
        if self.readmore_button_o is None:
            self.readmore_button_o = readmore_display("Ui_files\\Schedules\\schedule_readmore_form.ui")
            self.readmore_button_o.show()
        else:
            self.readmore_button_o.close()
            self.readmore_button_o = None

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

class readmore_display(QMainWindow):
    def __init__(self,ui_file):
        super(readmore_display,self).__init__()
        uic.loadUi(ui_file,self)

app=QApplication([])

if __name__ == "__main__":
    window=home_screen("Ui_files\Home_Screen_Window.ui")
    app.exec_()

