#!/usr/bin/python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------------
#Author      : GhostaR
#Email       : GhostaR@163.com
#Last Date   : 2016-10-21 
#Description : This is an tool app,use to change .ui or .qrc file(which is designed by Qt Designer) to .py file(use for PyQt5), 
#              you should put this file and the .ui/.qrc file in the same folder,then run this file in command line,
#              it will atuo generate the related .py file for PyQt5.
#------------------------------------------------------------------------------------------------------------------------------   
import os

for root, dirs, files in os.walk('.'):
    for file in files:
        if os.path.splitext( file )[1] == '.ui':
            os.system('pyuic5.bat -o %s_ui.py %s' %(file.rsplit('.',1)[0],file)) 
            #file.rsplit('.',1) 即 把file字符串从右向左处理，以'.'为分隔符，只分割一次(如file=loveq.ui，那么变成了['loveq','ui'])，
            #file.rsplit('.',1)[0] 即只取文件名(loveq)，不要后缀(ui)
            print("Convert %s to %s_ui.py Finish!" %(file,file.rsplit('.',1)[0]))
            #exit()
        elif os.path.splitext( file )[1] == '.qrc': 
            os.system('pyrcc5.exe -o %s_rc.py %s' %(file.rsplit('.',1)[0],file)) 
            print("Convert %s to %s_rc.py Finish!" %(file,file.rsplit('.',1)[0]))
            #exit()
        
    #print("Can't Find .ui/.qrc file!")       