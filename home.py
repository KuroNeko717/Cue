#################### Importing Libraries #########################
from xml.etree.ElementTree import ProcessingInstruction
from PyQt5 import uic, QtWidgets
from PyQt5 import QtGui,QtCore
from PyQt5 import  QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
import sqlite3
from functools import partial
import datetime
import os
import subprocess

#Class for the Cue Main Window
class home_screen(QMainWindow):
    def __init__(self,ui_file):
        super(home_screen,self).__init__()
        uic.loadUi(ui_file,self)
        
        ################# Connecting all the PyQt5 elements to their respective functions ##################
        ############################## Here the t stands for triggered #####################################
        
        #Connecting the actionCreate for creating a shedule in menubar to t_create_schedule function
        self.create_schedule = None
        self.actioncreate_s_hs.triggered.connect(self.t_create_schedule)
        
        #Connecting the actionCreate for viewing schedules in menubar to the t_vedit_schedule function
        self.vedit_schedule = None
        self.actionview_s_hs.triggered.connect(self.t_vedit_schedule)

        #Connecting the actionCreate for creating notes in menubar to the t_create_note function
        self.create_note = None
        self.actioncreate_n_hs.triggered.connect(self.t_create_note)

        #Connecting the actionCreate for viewing notes in menubar to the t_vedit_note function
        self.vedit_note = None
        self.actionview_n_hs.triggered.connect(self.t_vedit_note)
        

        #Connecting the actionCreate for viewing SRS in menubar to the t_doc_view_srs function
        self.option_srs= None
        self.actioncreate_cue_srs_hs.triggered.connect(self.t_doc_view_srs)

        #Connecting the actionCreate for viewing file locaiton in menubar to the t_file_loc function
        self.option_file_loc= None
        self.actionfiles_in_local_folder_hs.triggered.connect(self.t_file_loc)
        
        #Database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        
        #timer 
        timer =QtCore.QTimer(self)
        timer.timeout.connect(self.time_update)
        timer.start(1000)
        
        #frames variable
        self.frames = []
        self.generate_schedule()
        self.setup()
        self.show()
        
    
    #Updating the date and time on the MainWindow Homescreen
    def time_update(self):
        
        date = QtCore.QDate.currentDate()
        time = QtCore.QTime.currentTime()
        
        s_date = date.toString()
        s_time = time.toString()
        
        timestamp = "Date: {} Time: {}".format(s_date,s_time)
        self.date_time_label_hs.setText(timestamp)
    
    #Updating the entire MainWindow Homescreen
    def update(self):
        
        for i in reversed(range(self.verticalLayout.count())): 
            self.verticalLayout.itemAt(i).widget().setParent(None)
            
        self.frames = []
        self.generate_schedule()
    
    #Function to Create the table in the Cue Database
    def setup(self):
        self.c.execute("create table if not exists Schedule(id integer primary key, name varchar(250) not null, create_date timestamp not null, occurance varchar(50) not null, discription text not null, is_notify boolean not null)")
        self.c.execute("create table if not exists Notes(id integer primary key, title varchar(250) not null, create_date timestamp not null, discription text not null)")


    #Generating/ Creating the schedules in Homescreen to display today's schedules
    def generate_schedule(self):
        data = self.c.execute("select * from Schedule where create_date >= date('now','-1 day') and create_date <= date('now','+1 day')")
        
        for i in data:
            temp = self._gen_schedule(i[1], i[4], i[0])
            self.frames.append(temp)
            self.verticalLayout.addWidget(temp)

    #function for creating and giving values to the PyQt5 elements for each schedule in the comescreen
    def _gen_schedule(self,time,title,id):
        #Creating the PyQt5 elements such as frame, label, buttons etc.
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

        #Assigning values to the schedule elements in the homescreen
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
    
    #Function for when the delete button is clicked for a schedule in the homesreen
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
    
    #Function for when the edit button is clicked for a schedule in the homesreen
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

    #Function for when the read more button is clicked for a schedule in the homesreen
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

    #Function to pass the path of the ui file for Create Schedule
    def t_create_schedule(self):
        if self.create_schedule is None:
            self.create_schedule = create_schedule("Ui_files\\Schedules\\schedule_create_form.ui",self)
            self.create_schedule.show()
        else:
            self.create_schedule.close()
            self.create_schedule = None
            
    #Function to pass the path of the ui file for Viewing Schedule
    def t_vedit_schedule(self):
        if self.vedit_schedule is None:
            self.vedit_schedule = vedit_schedule("Ui_files\\Schedules\\schedule_view_form.ui")
            self.vedit_schedule.show()
        else:
            self.vedit_schedule.close()
            self.vedit_schedule = None

    #Function to pass the path of the ui file for Creating Notes
    def t_create_note(self):
        if self.create_note is None:
            self.create_note = create_note("Ui_files\\Notes\\notes_create_form.ui")
            self.create_note.show()
        else:
            self.create_note.close()
            self.create_note = None

    #Function to pass the path of the ui file for Viewing Schedules
    def t_vedit_note(self):
        if self.vedit_note is None:
            self.vedit_note = vedit_note("Ui_files\\Notes\\notes_view_form.ui",self)
        else:
            self.vedit_note.close()
            self.vedit_note = None

    #Function to pass Cue_SRS.pdf location path
    def t_doc_view_srs(self):
        if self.option_srs is None:
            filename= os.path.abspath("Documents\Cue_SRS.pdf")
            self.option_srs=OptionDisplaySRS(filename,self.option_srs)

    #Function to pass file location path
    def t_file_loc(self):
        if self.option_file_loc is None:
            filename= os.path.abspath("home.py")
            self.option_file_loc=OptionDisplayF_loc(filename,self.option_file_loc)           


#Class for creating the schedules
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
    
    #Formating the values shown in the schedule edit window
    def edit(self):
        self.create_new_label_s_c.setText("Edit Schedule")
        self.name_textedit_s_c.setText(self.data[1])
        self.occurence_combobox_s_c.setCurrentText(self.data[3])
        self.description_plaintextedit_s_c.setPlainText(self.data[4])
        self.notification_on_checkbox_s_c.setChecked(bool(self.data[5]))
        try:
            remind_date = datetime.datetime.strptime(self.data[2] , "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            remind_time = datetime.datetime.strptime(self.data[2] , "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
        except:
            remind_date = datetime.datetime.strptime(self.data[2] , "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
            remind_time = datetime.datetime.strptime(self.data[2] , "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M:%S") 

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
        
        self.conn.commit()
        self.close()
        self.parent_class.update()
        
class vedit_schedule(QMainWindow):
    
    def __init__(self,ui_file):
        super(vedit_schedule,self).__init__()
        uic.loadUi(ui_file,self)
        
        self.conn = sqlite3.connect('Cue.db')
        self.c = self.conn.cursor()
        
        self.frames = []
        
        self.generate_schedule()
        
        self.search_button.clicked.connect(self.update)
        
    #Updating the entire MainWindow Homescreen
    def update(self):
        
        for i in reversed(range(self.verticalLayout.count())): 
            self.verticalLayout.itemAt(i).widget().setParent(None)
            
        self.frames = []
        self.search_schedules()
    
    #getting the filtered values
    def search_schedules(self):
        search_text = self.search.toPlainText()
        to_date = self.to_date_s_v.date()
        from_date = self.from_date_s_v.date()
        self.generate_schedule(search_text,to_date,from_date)
    
   #Generating/ Creating the schedules in Homescreen to display today's schedules
    def generate_schedule(self,is_search=False ,search_text="", to_date=QtCore.QDate.currentDate(), from_date=QtCore.QDate.currentDate()):
        
        if not is_search:
            data = self.c.execute("select * from Schedule")
        else:
            data = self.c.execute(f"select * from Schedule where create_date >= \"{from_date.toPyDate()}\" and create_date <= \"{to_date.toPyDate()}\" and name like \"{search_text}\"")
        
        for i in data:
            temp = self._gen_schedule(i[1], i[4], i[0]) 
            self.frames.append(temp)
            self.verticalLayout.addWidget(temp)

    #function for creating and giving values to the PyQt5 elements for each schedule in the comescreen
    def _gen_schedule(self,time,title,id):
        #Creating the PyQt5 elements such as frame, label, buttons etc.
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

        #Assigning values to the schedule elements in the homescreen
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
    
    #Function for when the delete button is clicked for a schedule in the homesreen
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
    
    #Function for when the edit button is clicked for a schedule in the homesreen
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

    #Function for when the read more button is clicked for a schedule in the homesreen
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
    def __init__(self,ui_file,parent_class,*args, **kwargs):
        super(vedit_note,self).__init__(*args, **kwargs)
        uic.loadUi(ui_file,self)

        self.nframes = []
        self.parent_class = parent_class

        #database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()

        self.generate_note()
        self.show()

    def generate_note(self):
        search_text=self.search.toPlainText()

        if search_text != "" and search_text != None:
            data=self.c.execute(f"select* from Notes where title like \"{search_text}\"")
        else:
            data=self.c.execute(f"select* from Notes")

        for i in data:
            temp=self._gen_note(i[1],i[3],i[2],i[0])
            self.nframes.append(temp)
            self.verticalLayout.addWidget(temp)
        self.search.textChanged.connect(self.update_notes)

    def update_notes(self):
        for i in reversed(range(self.verticalLayout.count())): 
            self.verticalLayout.itemAt(i).widget().setParent(None)
            
        self.nframes = []
        self.generate_note()
        
    def _gen_note(self,title,description,date,id):
        frame = QtWidgets.QFrame()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
        frame.setSizePolicy(sizePolicy)
        frame.setMinimumSize(QtCore.QSize(0, 100))
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setLineWidth(5)
        frame.setMidLineWidth(5)
        frame.setObjectName("frame")
        label_title = QtWidgets.QLabel(frame)
        label_title.setGeometry(QtCore.QRect(0, 10, 131, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        label_title.setFont(font)
        label_title.setStyleSheet("background-color: rgb(44, 47, 51);")
        label_title.setAlignment(QtCore.Qt.AlignCenter)
        label_title.setObjectName("label_title")
        label_description = QtWidgets.QLabel(frame)
        label_description.setGeometry(QtCore.QRect(130, 10, 671, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        label_description.setFont(font)
        label_description.setStyleSheet("background-color: rgb(170, 255, 127);\n" "color: rgb(0, 0, 0);")
        label_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        label_description.setObjectName("label_description")
        label_date_created = QtWidgets.QLabel(frame)
        label_date_created.setGeometry(QtCore.QRect(660, 60, 141, 21))
        label_date_created.setStyleSheet("background-color: rgb(170, 255, 127);\n" "color: rgb(0, 0, 0);")
        label_date_created.setObjectName("label_date_created")
        
        #Assigning values to the schedule elements in the homescreen
        _translate = QtCore.QCoreApplication.translate
        label_title.setText(_translate("MainWindow", "{}".format(title)))
        label_description.setText(_translate("MainWindow", "{}".format(description)))
        label_date_created.setText(_translate("MainWindow","Date Created: "+"{}".format(date)))
        label_title.mousePressEvent=partial(self.onclick_readMore_notes,id)
        label_description.mousePressEvent=partial(self.onclick_readMore_notes,id)

        return frame


    #Function for when the Title or description is clicked for a Note when viewing notes
    def onclick_readMore_notes(self,id,*args, **kwargs):
        x = self.c.execute("select * from Notes where id = {}".format(id))
        
        
        for i in x:
            x = i
        
        self.readmore_form= None
        if self.readmore_form is None:
            self.readmore_form = readmore_display_notes("Ui_files\\Notes\\notes_readmore_form.ui",x[3],x[2],x[1],id,self)
            self.readmore_form.show()
        else:
            self.readmore_form.close()
            self.readmore_form = None

class readmore_display_notes(QMainWindow):
    
    def __init__(self,ui_file,discription,date,title,id,parent_data):
        super(readmore_display_notes,self).__init__()
        uic.loadUi(ui_file,self)
        self.discription = discription
        self.date=date
        self.title=title
        self.parent_data = parent_data
        
        #database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        self.re_translate(id)

    def re_translate(self,id):
        _translate = QtCore.QCoreApplication.translate
        self.content.setText(_translate("Form", "{}".format(self.discription)))
        self.label_date.setText(_translate("Form", "Date Created: "+"{}".format(self.date)))
        self.label_title.setText(_translate("Form", "{}".format(self.title)))
        self.delete_button_notes.clicked.connect(partial(self.onclick_delete_notes,id))
        self.edit_button_notes.clicked.connect(partial(self.onclick_edit_notes,id))

    def onclick_edit_notes(self,id):
        
        x = self.c.execute(f"select * from Notes where id =\"{id}\"")
        
        for i in x:
            data = i
            
        self.edit_dialogue_box = None
        if self.edit_dialogue_box  is None:
            self.edit_dialogue_box  = edit_display("Ui_files\\Notes\\notes_edit_form.ui",data,self,self.parent_data)
        else:
            self.edit_dialogue_box.close()
            self.edit_dialogue_box  = None

#Function for when the delete button is clicked for a note
    def onclick_delete_notes(self,id):
        x = self.c.execute(f"select * from Notes where id = \"{id}\"")
        
        for i in x:
            data = i
        
        self.delete_dialogue_box = None
        if self.delete_dialogue_box  is None:
            self.delete_dialogue_box  = delete_notes_dialog("Ui_files\\Notes\\notes_delete_dialogbox.ui",data[0],self,self.parent_data)
        else:
            self.delete_dialogue_box.close()
            self.delete_dialogue_box  = None

class edit_display(QMainWindow):
    
    def __init__(self,ui_file,data,parent_data,super_parent):
        super(edit_display,self).__init__()
        uic.loadUi(ui_file,self)
        self.parent_data = parent_data
        self.super_parent = super_parent
        self.data = data
        self.re_translate()
        
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        
        self.id = data[0]
        self.save_button_n_e.clicked.connect(self.onclick_yes)
        self.delete_button_n_e.clicked.connect(self.onclick_no)
        
        self.show()
        
    def onclick_yes(self):
        
        title_text = self.title_textedit_n_e.toPlainText()
        content_text = self.content_textedit_n_e.toPlainText()
        self.c.execute(f"update Notes set title =\"{title_text}\", discription = \"{content_text}\" where id = \"{self.data[0]}\"")
        self.conn.commit()
        self.super_parent.update_notes()
        self.parent_data.close()
        self.close()
        
    def onclick_no(self):
        self.close()
        
    def re_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.title_textedit_n_e.setText(self.data[1])
        self.content_textedit_n_e.setText(self.data[3])

class delete_notes_dialog(QDialog):
    
    def __init__(self,ui_file, id, parent_data,super_parent):
        super(delete_notes_dialog,self).__init__()
        uic.loadUi(ui_file,self)
        
        #database variables
        self.conn = sqlite3.connect("Cue.db")
        self.c = self.conn.cursor()
        
        self.super_parent = super_parent
        self.parent_data = parent_data
        
        self.id = id
        self.confirm_button_n_d.clicked.connect(self.onclick_yes)
        self.cancel_button_n_d.clicked.connect(self.onclick_no)
        
        self.show()
    
        
    def onclick_yes(self):
        self.c.execute("delete from Notes where id="+str(self.id))
        self.conn.commit()
        self.super_parent.update_notes()
        self.parent_data.close()
        self.close()
        
    def onclick_no(self):
        self.close()

class readmore_display(QMainWindow):
    
    def __init__(self,ui_file,discription):
        super(readmore_display,self).__init__()
        uic.loadUi(ui_file,self)
        self.discription = discription
        self.re_translate()
        
    def re_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.content_label_s_rm.setText(_translate("Form", "{}".format(self.discription)))
        

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

#Class for the Menubar Option SRS Display function
class OptionDisplaySRS(QMainWindow):
    def __init__(self,filename,option_srs):
        super(OptionDisplaySRS,self).__init__()
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.gen_display(filename,option_srs)
    
    def gen_display(self,filename,option_srs):
        settings = self.view.settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        url = QtCore.QUrl.fromLocalFile(filename)
        self.view.load(url)
        self.view.resize(640, 480)
        if option_srs is None:
            self.view.show()
        else:
            self.view.close()
            option_srs= None

#Class for the Menubar Option Show File Location function
class OptionDisplayF_loc(QMainWindow):
    def __init__(self,filename,option_file_loc):
        super(OptionDisplayF_loc,self).__init__()
        self.show_file_loc(filename,option_file_loc)
    
    def show_file_loc(self,filename,option_file_loc):
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        # explorer would choke on forward slashes
        path = os.path.normpath(filename)

        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', path])

app=QApplication([])

if __name__ == "__main__":
    window=home_screen("Ui_files\Home_Screen_Window.ui")
    app.exec_()

