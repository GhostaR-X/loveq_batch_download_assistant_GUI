#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QProgressBar, QLabel
from loveq_ui import Ui_LoveQ_Download_Assistant
from datetime import datetime
import urllib.request
import time

from PyQt5.QtCore import QThread, pyqtSignal, QDate 
from PyQt5.QtGui import QIcon
import loveq_rc

class LOVEQ_MAIN( QWidget ):
    def __init__( self ):
        #----初始化常量---- 
        self.today_date = datetime.now() 
        #----初始化变量----
        self.save_dir = os.path.abspath('.')  #当前目录的绝对路径       
        self.start_date = datetime.now()      #默认起始日期为今天 
        self.end_date = self.start_date       #默认结束日期为今天

        self.task_label_dict = {}
        self.task_progress_dict = {}
        self.task_valid_num_table = [ True, True, True ]

        #----初始化GUI界面----
        super(LOVEQ_MAIN,self).__init__()         #用LOVEQ_MAIN父类的__init__函数QWidget.__init__()来初始化LOVEQ_MAIN的对象
        self.ui = Ui_LoveQ_Download_Assistant()       
        self.ui.setupUi( self )                   #导入loveq.ui生成的loveq_ui.py的界面

        #modify window title
        self.setWindowTitle("LoveQ_Batch_Download_Assistant     By GhostaR@163.com")     #手动修改窗口标题

        #init icon
        #self.setWindowIcon(QIcon('Assistant.ico'))  
        self.setWindowIcon(QIcon(':icon/Assistant.ico')) 

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

    def slot_SetSaveDir( self ):                                      #定义槽函数 
        output_dir = QFileDialog.getExistingDirectory(self,  
                                    "选择保存路径",                      #QFileDialog 对话框 Title 
                                    ".")                                 #默认路径  
        if output_dir != '' :                                       #''等于选择了cancel 
            self.ui.saveDirEdit.setText( output_dir ) 

    def slot_ShowWarningMessage( self, str ):                         #定义槽函数 
        QMessageBox.warning (self,                                  #使用infomation信息框  
                            "Warning",  
                            str,  
                            QMessageBox.Ok)

    def slot_CreateLabel( self, task_num, url ):
        if task_num >= 3:
            return -1

        task_label_num = "task_label_" + str( task_num ) 
        self.task_label_dict[task_label_num] = QLabel( self )

        self.task_label_dict[task_label_num].setGeometry(10, 158 + task_num * 25, 500, 25)

        self.task_label_dict[task_label_num].setObjectName("task_label")
        self.task_label_dict[task_label_num].setText("Downloading %s " %(url))
        self.task_label_dict[task_label_num].show()

        return task_label_num

    def slot_CreateProgress( self, task_num ):
        if task_num >= 3:
            return -1

        task_progress_num = "task_progress_" + str( task_num )
        self.task_progress_dict[task_progress_num] = QProgressBar(self)
        self.task_progress_dict[task_progress_num].setGeometry(460, 165 + task_num * 25, 200, 10)

        self.task_progress_dict[task_progress_num].setValue(0) 
        self.task_progress_dict[task_progress_num].show() 

        return task_progress_num 

    def slot_CreateDownloadTask( self, target_url, save_file, task_num ):
        self.downloadThread = DownloadThread( target_url, save_file, task_num )
        self.downloadThread.dlSignal_RefreshProgress.connect( self.slot_RefreshProgress )
        self.downloadThread.dlSignal_Finish.connect( self.slot_FinishDownload )
        self.downloadThread.start()

        self.ui.saveDirBtn.setEnabled(False)                   #让按键无效直到任务结束 
        self.ui.downloadBtn.setEnabled(False)
        self.ui.statusLabel.setText("Downloading...")

    def slot_RefreshProgress( self, progressbar , percent ):
        self.task_progress_dict[progressbar].setValue( percent ) 

    def slot_FinishDownload( self, task_num, url ):
        label_num = "task_label_" + str( task_num )
        task_progress_num = "task_progress_" + str( task_num )
        self.task_label_dict[label_num].setText( "Download    %s Finish!" %(url) ) 

        self.task_label_dict[label_num].hide()
        self.task_progress_dict[task_progress_num].hide() 
        self.TaskThread.release_task( task_num )  

        self.ui.saveDirBtn.setEnabled(True)                    #任务结束，让按键重新可用
        self.ui.downloadBtn.setEnabled(True)
        self.ui.statusLabel.setText("Task Finish!")
        

    def slot_StartTask( self ):
        self.save_dir = self.ui.saveDirEdit.text()             #更新保存路径
        self.start_date = self.ui.startDateEdit.date()         #更新起始日期  date() = 获取Start_dateEdit的日期信息 
        self.end_date = self.ui.endDateEdit.date()             #更新结束日期 

        #创建任务子进程
        self.TaskThread = TaskThread( self.save_dir, self.start_date, self.end_date )
        self.TaskThread.tskSignal_Warning.connect( self.slot_ShowWarningMessage )
        self.TaskThread.tskSignal_CreateLabel.connect( self.slot_CreateLabel )
        self.TaskThread.tskSignal_CreateProgress.connect( self.slot_CreateProgress )
        self.TaskThread.tskSignal_CreateDownloadTask.connect( self.slot_CreateDownloadTask )
        
        self.TaskThread.start()


class TaskThread( QThread ): 
    tskSignal_Finish  = pyqtSignal( str )                #先定义信号,定义参数为str类型
    tskSignal_Warning = pyqtSignal( str )
    tskSignal_CreateLabel = pyqtSignal( int, str )
    tskSignal_CreateProgress = pyqtSignal( int )
    tskSignal_CreateDownloadTask = pyqtSignal( str, str, int )

    def __init__( self , save_dir, start_date, end_date ): 
        super(TaskThread,self).__init__() 
        #----初始化常量----
        # Monday = 1,Tuesday = 2, ... Sunday = 7
        self.week_table = ('None','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
        self.base_url = "http://dl.loveq.cn/program/"
        self.loveq_launch_date = datetime(2003,5,11)   #节目开播日期 
        self.today_date = datetime.now() 
        #----初始化变量----
        self.save_dir = save_dir
        self.start_date = start_date
        self.end_date = end_date

        self.task_valid_num_table = [ True, True, True ]

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
        target_url = self.base_url + "LoveQ.cn_" + str_date + "-1.mp3"
        return target_url

    def get_save_filename( self, date ):
        str_date = date.toString("yyyy-MM-dd")  
        filename = self.save_dir + '/' + str_date + "-LoveQ.mp3"
        return filename

    #获取有效任务号
    def get_valid_task_number( self ):
        for idx,val in enumerate( self.task_valid_num_table ):
            if val == True:
                self.task_valid_num_table[idx] = False  #set unvalid
                return idx
        return -1

    #释放有效任务号
    def put_valid_task_number( self, task_num ):
        if task_num >= 3:
            return -1
        self.task_valid_num_table[task_num] = True      #set valid
        return 0 

    def create_task_label( self, task_num, url ):
        if task_num >= 3:
            return -1
        self.tskSignal_CreateLabel.emit( task_num, url )
        return task_num

    def create_task_progressbar( self, task_num ):
        if task_num >= 3:
            return -1

        self.tskSignal_CreateProgress.emit( task_num )    
        return task_num 

    def create_task( self, target_url, save_file ):
        task_num = self.get_valid_task_number() 

        if task_num == -1 :
            print("Tasks number is limited to 3,there is not valid task!")
            return -1 

        if self.create_task_label( task_num, target_url ) == -1 :
            print("Create task label fail!")
            return -2

        if self.create_task_progressbar( task_num ) == -1:
            print("Create task progressbar fail!")
            return -3 

        return task_num

    def release_task( self, task_num ):
        self.put_valid_task_number( task_num )  

    def run( self ):
        print("Task Thread Start!") 

        if self.start_date > self.end_date :
            self.tskSignal_Warning.emit( "End date must be later than start date!" ) 
        elif self.start_date <= self.end_date :
            if self.start_date == self.end_date : 
                if self.is_available_date( self.start_date ) == False:
                    self.tskSignal_Warning.emit( "It is not an available date for download!" )  
                    return
       
        while True:     #simulate  do...while    self.end_date > self.start_date  
            if self.is_available_date( self.start_date ) == False:   
                self.start_date = QDate.fromJulianDay( self.start_date.toJulianDay() + 1 )   

                if self.start_date > self.end_date or self.start_date >= self.today_date or self.start_date < self.loveq_launch_date :
                    break
                else :
                    continue
            else :
                target_url = self.get_target_url( self.start_date )
                save_file = self.get_save_filename( self.start_date )
                task_num = self.create_task( target_url, save_file )
                if task_num == -1:
                    time.sleep(5) 
                    print("try again!")
                    continue

                try :                    
                    self.tskSignal_CreateDownloadTask.emit( target_url, save_file, task_num )

                except urllib.request.HTTPError as e :
                    print("Download   ",target_url,"Fail!") 
                    print("Error Code:", e.getcode())                          

                self.start_date = QDate.fromJulianDay( self.start_date.toJulianDay() + 1 )  

            if self.start_date > self.end_date :
                break

            time.sleep(0.1) 

        #print("LoveQ Download Tasks Finish!")

        #urllib.request.urlretrieve( self.target_url, self.save_file, self.cbfunc_progress )




class DownloadThread( QThread ):
    dlSignal_Finish = pyqtSignal( int, str )                #先定义信号,定义参数为str类型
    dlSignal_RefreshProgress = pyqtSignal( str, int ) 

    def __init__( self , target_url, save_file, task_num ): 
        super(DownloadThread,self).__init__() 
        self.target_url = target_url
        self.save_file = save_file
        self.task_num = task_num
        self.progressbar_num = "task_progress_" + str( task_num )
        self.label_num = "task_label_" + str( task_num )


    def run( self ):
        print("Download Thread Start!") 
        urllib.request.urlretrieve( self.target_url, self.save_file, self.cbfunc_progress )

    def cbfunc_progress( self, blocknum, blocksize, totalsize ) :  #callbackfunc_progress
        percent = 100 * blocknum * blocksize / totalsize
        #print( "blocknum=",blocknum )
        #print( "%3d%%" %(percent),end='\r')
        if percent >= 100 :
            percent = 100
            #print("")   #change line
            self.dlSignal_Finish.emit( self.task_num, self.target_url )

        self.dlSignal_RefreshProgress.emit( self.progressbar_num ,percent )  

if __name__=="__main__":   
    app = QApplication(sys.argv)  
    loveq = LOVEQ_MAIN() 
    sys.exit(app.exec_())  