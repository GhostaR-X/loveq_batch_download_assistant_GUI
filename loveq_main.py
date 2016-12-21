#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QProgressBar, QLabel
from PyQt5 import QtGui
from loveq_ui import Ui_LoveQ_Download_Assistant
from datetime import datetime
import urllib.request
import time

from PyQt5.QtCore import QThread, pyqtSignal, QDate 

class LOVEQ_MAIN( QWidget ):
    def __init__( self ):
        #----初始化常量----
        # Monday = 1,Tuesday = 2, ... Sunday = 7
        self.week_table = ('None','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
        self.base_url = "http://dl.loveq.cn/program/"
        self.loveq_launch_date = datetime(2003,5,11)   #节目开播日期 
        self.today_date = datetime.now() 
        #----初始化变量----
        self.save_dir = os.path.abspath('.')  #当前目录的绝对路径       
        self.start_date = datetime.now()      #默认起始日期为今天 
        self.end_date = self.start_date       #默认结束日期为今天

        self.task_label_dict = {}
        self.task_progress_dict = {}

        #----初始化GUI界面----
        super(LOVEQ_MAIN,self).__init__()         #用LOVEQ_MAIN父类的__init__函数QWidget.__init__()来初始化LOVEQ_MAIN的对象
        self.ui = Ui_LoveQ_Download_Assistant()  
        self.ui.setupUi( self )                   #导入loveq.ui生成的loveq_ui.py的界面

        #init child controls' status
        #--time--
        self.ui.startDateEdit.setCalendarPopup(True)               #设置弹出日历
        self.ui.startDateEdit.setDateTime(self.today_date)         #默认起始日期为今天
        self.ui.endDateEdit.setCalendarPopup(True)                 #设置弹出日历
        self.ui.endDateEdit.setDateTime(self.today_date)           #默认结束日期为今天

        #--output directory--
        self.ui.saveDirEdit.setText( self.save_dir )               #默认保存路径为当前路径

        #--Slot Setup--
        self.ui.saveDirBtn.clicked.connect( self.slot_SetSaveDir )   #槽函数不用加括号
        self.ui.downloadBtn.clicked.connect( self.slot_StartTask )   #槽函数不用加括号               

        #--GUI widget show--
        self.show()

        '''self.create_task_label( 1, "www.baidu.com" )
        self.create_task_label( 2, "www.jd.com" )
        self.create_task_label( 3, "www.baidu.com" )
        self.create_task_label( 4, "www.baidu.com" )
        self.create_task_label( 5, "www.baidu.com" )
        self.create_task_progressbar( 1 )
        self.create_task_progressbar( 2 )
        self.create_task_progressbar( 3 )
        self.create_task_progressbar( 4 )
        self.create_task_progressbar( 5 )'''


    def is_available_date( self, date ):
        if date < self.loveq_launch_date or date >= self.today_date:
            return False
        day_of_week = date.dayOfWeek()    
        if self.week_table[day_of_week] != 'Saturday' and self.week_table[day_of_week] != 'Sunday':
            return False
        else:
            return True 

    def get_target_url( self, date ):  
        str_date = date.toString("yyyy-MM-dd")    
        #print(str_date)
        target_url = self.base_url + "LoveQ.cn_" + str_date + "-1.mp3"
        return target_url

    def get_save_filename( self, date ):
        str_date = date.toString("yyyy-MM-dd")  
        filename = self.save_dir + '/' + str_date + "-LoveQ.mp3"
        #print(filename)
        return filename
    

    def slot_SetSaveDir( self ):                                      #定义槽函数 
        output_dir = QFileDialog.getExistingDirectory(self,  
                                    "选择保存路径",                      #QFileDialog 对话框 Title 
                                    ".")                                 #默认路径  
        if output_dir != '' :                                       #''等于选择了cancel 
            self.ui.saveDirEdit.setText( output_dir ) 

    def create_task_label( self, task_num, url ):
        if task_num > 5:
            return 0

        task_label_num = "task_label_" + str( task_num ) 
        self.task_label_dict[task_label_num] = QLabel( self )       
        if task_num == 1:
            self.task_label_dict[task_label_num].setGeometry(5, 242, 500, 25)
        elif task_num == 2: 
            self.task_label_dict[task_label_num].setGeometry(5, 267, 500, 25)
        elif task_num == 3: 
            self.task_label_dict[task_label_num].setGeometry(5, 292, 500, 25)
        elif task_num == 4: 
            self.task_label_dict[task_label_num].setGeometry(5, 317, 500, 25)
        elif task_num == 5: 
            self.task_label_dict[task_label_num].setGeometry(5, 342, 500, 25)
        self.task_label_dict[task_label_num].setObjectName("task_label")
        self.task_label_dict[task_label_num].setText("Downloading %s,waiting..." %(url))
        self.task_label_dict[task_label_num].show()

        return task_label_num

    def create_task_progressbar( self, task_num ):
        if task_num > 5:
            return 0

        task_progress_num = "task_progress_" + str( task_num )
        self.task_progress_dict[task_progress_num] = QProgressBar(self)
        if task_num == 1:
            self.task_progress_dict[task_progress_num].setGeometry(470, 247, 200, 15)
        elif task_num == 2:
            self.task_progress_dict[task_progress_num].setGeometry(470, 273, 300, 15) 
        elif task_num == 3:
            self.task_progress_dict[task_progress_num].setGeometry(470, 297, 300, 15) 
        elif task_num == 4:
            self.task_progress_dict[task_progress_num].setGeometry(470, 323, 300, 15) 
        elif task_num == 5:
            self.task_progress_dict[task_progress_num].setGeometry(470, 347, 300, 15) 
        self.task_progress_dict[task_progress_num].setValue(0) 
        self.task_progress_dict[task_progress_num].show() 

        return task_progress_num            

    def slot_StartTask( self ):
        self.save_dir = self.ui.saveDirEdit.text()             #更新保存路径
        print("save_dir=",self.save_dir)  

        self.start_date = self.ui.startDateEdit.date()         #更新起始日期  date() = 获取Start_dateEdit的日期信息 
        print("start_date=",self.start_date)

        self.end_date = self.ui.endDateEdit.date()             #更新结束日期 
        print("end_date=",self.end_date)
        
        if self.end_date == self.start_date :
            if self.is_available_date( self.start_date ) == False: 
                QMessageBox.warning (self,                         #使用infomation信息框  
                                    "Warning",  
                                    "It is not an available date for download!",  
                                    QMessageBox.Ok)    
                #print("It is not an available date for download!")
                #exit() 
            else:
                target_url = self.get_target_url( self.start_date )
                save_file = self.get_save_filename( self.start_date )                

                #print ("Downloading %s,waiting..." %(target_url))
                #self.ui.consoleTextEdit.append("Downloading %s,waiting..." %(target_url))
                self.task_label_num    = self.create_task_label( 1, target_url )
                self.task_progress_num = self.create_task_progressbar( 1 )

                try :
                    self.downloadThread = DownloadThread( target_url, save_file, self.task_progress_num )
                    self.downloadThread.start()
                    #urllib.request.urlretrieve( target_url, save_file, self.workThread.cbfunc_progress )
                    #print("LoveQ Download Task Finish!")
                    #self.ui.consoleTextEdit.append("LoveQ Download Task Finish!")
                except urllib.request.HTTPError as e :                   
                    print("LoveQ Download Task Fail!")
                    print("Error Code:", e.getcode())
        else:   #self.end_date != self.start_date
            print("LoveQ Download Tasks from",self.start_date,"to",self.end_date,"Start!")            
            if self.start_date > self.end_date : 
                sign = -1
            else :
                sign = 1    
            while True:     #simulate  do...while 
                if self.is_available_date( self.start_date ) == False:   
                    #print('unavailable')
                    self.start_date = QDate.fromJulianDay( self.start_date.toJulianDay() + sign )  

                    if self.end_date == self.start_date or self.start_date >= self.today_date or self.start_date < self.loveq_launch_date :
                        break
                    else :
                        continue
                else :
                    #print(start_date)
                    target_url = self.get_target_url( self.start_date )
                    save_file = self.get_save_filename( self.start_date )
                    #print ("Downloading %s,waiting..." %(target_url))
                    self.ui.consoleTextEdit.append("Downloading %s,waiting..." %(target_url))
                    try :
                        #urllib.request.urlretrieve( target_url, save_file,self.cbfunc_progress )
                        self.downloadThread = DownloadThread( target_url, save_file )
                        self.downloadThread.start()
                    except urllib.request.HTTPError as e :
                        print("Download   ",target_url,"Fail!") 
                        print("Error Code:", e.getcode())                          

                    self.start_date = QDate.fromJulianDay( self.start_date.toJulianDay() + sign ) 

                if self.end_date == self.start_date :
                    break 

            print("LoveQ Download Tasks Finish!")



class DownloadThread( QThread ): 
    dlFinishSignal = pyqtSignal(str)                 #先定义信号,定义参数为str类型

    def __init__( self , target_url, save_file, progressbar_num ): 
        super(DownloadThread,self).__init__() 
        self.target_url = target_url
        self.save_file = save_file
        self.progressbar_num = progressbar_num

        self.dlFinishSignal.connect(self.print_prompt)               #将信号连接到函数print_prompt

    def run( self ):
        print("Downlaod Thread Start!") 
        urllib.request.urlretrieve( self.target_url, self.save_file, self.cbfunc_progress )

    def print_prompt( self, str ):
        #loveq.ui.consoleTextEdit.append( str ) 
        loveq.task_progress_dict[self.task_label_num].setText( str )    

    def cbfunc_progress( self, blocknum, blocksize, totalsize ) :  #callbackfunc_progress
        percent = 100 * blocknum * blocksize / totalsize
        #loveq.ui.downloadProgressBar.setValue(percent) 
        #print( "blocknum=",blocknum )
        print( "%3d%%" %(percent),end='\r')
        if percent >= 100 :
            percent = 100
            print("")   #change line
            #self.dlFinishSignal.emit("Download %s Finish!" %(target_url))

        #loveq.ui.downloadProgressBar.setValue(percent) 
        loveq.task_progress_dict[self.progressbar_num].setValue( percent ) 

if __name__=="__main__":   
    app = QApplication(sys.argv)  
    loveq = LOVEQ_MAIN() 
    sys.exit(app.exec_())  