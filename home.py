from xml.etree.ElementTree import ProcessingInstruction
from PyQt5 import QtGui,QtCore
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow
import sqlite3
from functools import partial
import datetime

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
        
        #timer 
        timer =QtCore.QTimer(self)
        timer.timeout.connect(self.time_update)
        timer.start(1000)
        
        #frames variable
        self.frames = []
        
        #View/ Edit Note Menubar Action
        self.vedit_note = None
        self.actionview_n_hs.triggered.connect(self.t_vedit_note)
        self.generate_schedule()
        self.setup()
        self.show()
    
    def time_update(self):
        
        date = QtCore.QDate.currentDate()
        time = QtCore.QTime.currentTime()
        
        s_date = date.toString()
        s_time = time.toString()
        
        timestamp = "Date: {} Time: {}".format(s_date,s_time)
        
        self.date_time_label_hs.setText(timestamp)
    
    def update(self):
        
        for i in reversed(range(self.verticalLayout.count())): 
            self.verticalLayout.itemAt(i).widget().setParent(None)
            
        self.frames = []
        self.generate_schedule()
    
    def setup(self):
        self.c.execute("create table if not exists Schedule(id integer primary key, name varchar(250) not null, create_date timestamp not null, occurance varchar(50) not null, discription text not null, is_notify boolean not null)")
        self.c.execute("create table if not exists Notes(id integer primary key, title varchar(250) not null, create_date timestamp not null, discription text not null)")

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
        frame.setStyleSheet("background-color: rgb(44, 47, 51);\n"
        "color: rgb(255, 255, 255);")
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName("frame")
        time_label = QtWidgets.QLabel(frame)
        time_label.setGeometry(QtCore.QRect(10, 20, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        time_label.setFont(font)
        time_label.setStyleSheet("color: rgb(213, 210, 255);")
        time_label.setObjectName("time_label")
        line_3 = QtWidgets.QFrame(frame)
        line_3.setGeometry(QtCore.QRect(160, 0, 20, 91))
        line_3.setFrameShape(QtWidgets.QFrame.VLine)
        line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_3.setObjectName("line_3")
        content_label = QtWidgets.QLabel(frame)
        content_label.setGeometry(QtCore.QRect(180, 10, 431, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        content_label.setFont(font)
        content_label.setStyleSheet("color: rgb(213, 210, 255);")
        content_label.setObjectName("content_label")
        readmore_button = QtWidgets.QPushButton(frame)
        readmore_button.setGeometry(QtCore.QRect(380, 60, 121, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        readmore_button.setFont(font)
        readmore_button.setStyleSheet("color: rgb(213, 210, 255);")
        readmore_button.setObjectName("readmore_button")
        edit_button = QtWidgets.QPushButton(frame)
        edit_button.setGeometry(QtCore.QRect(650, 30, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        edit_button.setFont(font)
        edit_button.setStyleSheet("color: rgb(213, 210, 255);")
        edit_button.setObjectName("edit_button")
        delete_button = QtWidgets.QPushButton(frame)
        delete_button.setGeometry(QtCore.QRect(720, 30, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        delete_button.setFont(font)
        delete_button.setStyleSheet("color: rgb(213, 210, 255);")
        delete_button.setObjectName("delete_button")

        _translate = QtCore.QCoreApplication.translate
        time_label.setText(_translate("MainWindow", "{}".format(time)))
        content_label.setText(_translate("MainWindow", "{}".format(title)))
        readmore_button.setText(_translate("MainWindow", "Read More"))
        edit_button.setText(_translate("MainWindow", "Edit"))
        delete_button.setText(_translate("MainWindow", "Delete"))

        
        content_label.setText(_translate("MainWindow", "{}".format(title)))
        
        readmore_button.clicked.connect(partial(self.onclick_readMore, id))
        edit_button.clicked.connect(partial(self.onclick_edit,id))
        delete_button.clicked.connect(partial(self.onclick_delete,id))
        
        return frame
    
    def onclick_delete(self,id):
        x = self.c.execute("select * from Schedule where id = {}".format(id))
        
        for i in x:
            x = i
        
        self.delete_dialogue_box = None
        if self.delete_dialogue_box  is None:
            self.delete_dialogue_box  = delete_display("Ui_files\\Schedules\\schedule_delete_dialogbox.ui",x[0],self)
            self.delete_dialogue_box .show()
        else:
            self.delete_dialogue_box .close()
            self.delete_dialogue_box  = None
    
    def onclick_edit(self,id):
        
        data = self.c.execute("select * from Schedule where id = {}".format(id))
        
        for i in data:
            data = i
        
        self.edit_form= None
        if self.edit_form is None:
            self.edit_form = create_schedule("Ui_files\\Schedules\\schedule_create_form.ui",self,type="edit",data=data)
            self.edit_form.show()
        else:
            self.edit_form.close()
            self.edit_form = None
    
    def onclick_readMore(self,id):
        x = self.c.execute("select * from Schedule where id = {}".format(id))
        
        for i in x:
            x = i

        self.readmore_form= None
        if self.readmore_form is None:
            self.readmore_form = readmore_display("Ui_files\\Schedules\\schedule_readmore_form.ui",x[4])
            self.readmore_form.show()
        else:
            self.readmore_form.close()
            self.readmore_form = None

    #Create schedule Menubar Action Form Open/Close
    def t_create_schedule(self):
        if self.create_schedule is None:
            self.create_schedule = create_schedule("Ui_files\\Schedules\\schedule_create_form.ui",self)
            self.create_schedule.show()
        else:
            self.create_schedule.close()
            self.create_schedule = None
            
    #Edit/view schedule Menubar Action Form Open/Close
    def t_vedit_schedule(self):
        if self.vedit_schedule is None:
            self.vedit_schedule = vedit_schedule("Ui_files\\Schedules\\schedule_view_form.ui")
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
    def __init__(self,ui_file,parent_class,type="create",data=None):
        super(create_schedule,self).__init__()
        uic.loadUi(ui_file,self)
        self.date_dateedit_s_c.setDate(QtCore.QDate.currentDate())
        self.time_timeedit_s_c.setTime(QtCore.QTime.currentTime())
        
        #Close Button
        self.parent_class = parent_class
        self.save_close_button_s_c.clicked.connect(self.create)
        
        #database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        
        #data
        self.data = data
        self.type = type
        
        if self.type == "edit":
            
            if data != None:
                self.edit()
            
    def edit(self):
        self.create_new_label_s_c.setText("Edit Schedule")
        self.name_textedit_s_c.setText(self.data[1])
        self.occurence_combobox_s_c.setCurrentText(self.data[3])
        self.description_plaintextedit_s_c.setPlainText(self.data[4])
        self.notification_on_checkbox_s_c.setChecked(bool(self.data[5]))
        remind_date = datetime.datetime.strptime(self.data[2] , "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        remind_time = datetime.datetime.strptime(self.data[2] , "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
        self.date_dateedit_s_c.setDate(QtCore.QDate.fromString(remind_date, 'yyyy-MM-dd'))
        self.time_timeedit_s_c.setTime(QtCore.QTime.fromString(remind_time, QtCore.Qt.TextDate))
    
        
    def create(self):
        name = self.name_textedit_s_c.toPlainText()
        occurance = self.occurence_combobox_s_c.currentText()
        is_notification = self.notification_on_checkbox_s_c.isChecked()
        discription = self.description_plaintextedit_s_c.toPlainText()
        remind_date = self.date_dateedit_s_c.date()
        remind_time = self.time_timeedit_s_c.time()
        remind_datetime = datetime.datetime.combine(remind_date.toPyDate(),remind_time.toPyTime())
        
        if self.type == "create":
            self.c.execute(f"insert into Schedule(name,create_date,occurance,discription,is_notify) values(\"{name}\",\"{remind_datetime}\",\"{occurance}\",\"{discription}\",\"{is_notification}\")")
        elif self.type == "edit":
            self.c.execute(f"update Schedule set name=\"{name}\" , create_date=\"{remind_datetime}\", occurance=\"{occurance}\", discription=\"{discription}\", is_notify=\"{is_notification}\"  WHERE id = {self.data[0]}")
            print(self.data[0])
        
        self.conn.commit()
        self.close()
        self.parent_class.update()
        
class vedit_schedule(QMainWindow):
    def __init__(self,ui_file):
        super(vedit_schedule,self).__init__()
        uic.loadUi(ui_file,self)

class create_note(QMainWindow):
    
    def __init__(self,ui_file):
        super(create_note,self).__init__()
        uic.loadUi(ui_file,self)
        
        #database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        
        self.save_button_n_c.clicked.connect(self.create_note)
        
    def create_note(self):
        title = self.title_textedit_n_c.toPlainText()
        discription = self.content_textedit_n_c.toPlainText()
        create_date = QtCore.QDate.currentDate()
        create_date = create_date.toString("yyyy-MM-dd")
        
        self.c.execute(f"insert into Notes(title,create_date,discription) values(\"{title}\",\"{create_date}\",\"{discription}\")")
        self.conn.commit()
        self.close()
        

class vedit_note(QMainWindow):
    def __init__(self,ui_file):
        super(vedit_note,self).__init__()
        uic.loadUi(ui_file,self)

class readmore_display(QMainWindow):
    
    def __init__(self,ui_file,discription):
        super(readmore_display,self).__init__()
        uic.loadUi(ui_file,self)
        self.discription = discription
        self.re_translate()
        
    def re_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.content_label_s_rm.setText(_translate("Form", "{}".format(self.discription)))

class edit_display(QMainWindow):
    
    def __init__(self,ui_file,data,parent_data):
        super(edit_display,self).__init__()
        uic.loadUi(ui_file,self)
        self.parent_data = parent_data
        self.data = data
        self.re_translate()
        
    def re_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.name_textedit_s_e.setText(self.data[1])
        #self.date_dateedit_s_e.set

class delete_display(QDialog):
    
    def __init__(self,ui_file, id, parent_data):
        super(delete_display,self).__init__()
        uic.loadUi(ui_file,self)
        
        self.parent_data = parent_data
        
        self.id = id
        self.yes_button_s_d.clicked.connect(self.onclick_yes)
        self.no_button_s_d.clicked.connect(self.onclick_no)
        
        #database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        
    def onclick_yes(self):
        self.c.execute("delete from Schedule where id="+str(self.id))
        self.conn.commit()
        self.parent_data.update()
        self.close()
        
    def onclick_no(self):
        self.close()

app=QApplication([])

if __name__ == "__main__":
    window=home_screen("Ui_files\Home_Screen_Window.ui")
    app.exec_()

