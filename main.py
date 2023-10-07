#!/usr/bin/env python
#Author : Fang Kong

import multiprocessing
import time

from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QCheckBox,QFileDialog,QGraphicsPixmapItem,\
    QGraphicsScene,QGraphicsView,QAction
from PyQt5.QtGui import QImage,QPixmap,QMouseEvent,QCloseEvent
from PyQt5.QtCore import QThread,pyqtSignal,QMutex,QTimer,Qt
import sys
import main_window as mw
import child_window as cw
#import displayer as disp
from multiprocessing import Process,Manager,Value,Pool

import json
import ctf

import numpy as np
from glob import glob
import os
from functools import partial

snaps=Manager().dict()
results=Manager().list()
groups_results=Manager().list()
final_micro_dict=Manager().dict()
kill_signal=Value('i',0)
sigma=Value('f',0.5)

raw_data = Manager().dict()
#results_view=Manager().list()
def BackendReadProcess(micro_names,snaps,all_micros,kill_signal):
    todo_list=micro_names.copy()
    while(len(snaps)<len(all_micros)) and kill_signal.value==0:
        for micro_name in todo_list:
            try:
                snaps[micro_name]
                micro_names.remove(micro_name)
            except:
                img = np.uint8(ctf.show_mrc(micro_name, 0.1,sigma.value))

                snaps[micro_name]=img
        todo_list=micro_names.copy()

    if len(snaps)==len(all_micros):
        kill_signal.value=1

def BackendWriteProcess(micro_dict,good_dir,bad_dir):
    for item in micro_dict:
        micro_name=item.split('/')[-1]
        if micro_dict[item] == 1 and not os.path.exists(good_dir + micro_name):
            try:
                os.symlink(item,good_dir+micro_name)
            except:
                pass
            #os.popen('ln -s ' + item + " " + good_dir)
        elif  micro_dict[item] == -1 and not os.path.exists(bad_dir + micro_name):
            try:
                os.symlink(item, bad_dir+micro_name)
            except:
                pass
    pass


def _PoolReader(item,raw_data,data_len):
  print("\r",end="",flush=True)
  raw_data[item]=np.uint8(ctf.show_mrc(item,0.1,sigma.value))
  print(str(len(raw_data))+'/'+str(data_len),end="")
'''
class DrawT(QThread):
    Qob=None
    micro_name=""
    signal=pyqtSignal()
   # thread_lock.lock()
    def __init__(self, Qob,micro_name):
        super(DrawT, self).__init__()
        self.Qob = Qob
        self.micro_name=micro_name

    def run(self):
        self.scence = QGraphicsScene()
        try:
            img =  snaps[self.micro_name]
            y, x = img.shape
            byte_img = img.tobytes()
            Qimg = QImage(byte_img,x,y,x,QImage.Format_Grayscale8)
            pix = QPixmap.fromImage(Qimg)
            item = QGraphicsPixmapItem(pix)
            self.scence.addItem(item)
        except:
            #print('pic not ready')
            pass

        self.Qob.setScene(self.scence)
        self.Qob=None
        self.signal.emit()

       # print('Thread last word.')
'''
#'''
window_views={}
def cmd_exec( cmd, i):
    if (i == 0):
        return cmd
    else:
        c = os.popen(cmd)
        return c.read()


class Childwindow(QMainWindow,cw.Ui_childwindow):
    s=[]
    gpus=[]
    current_work_directory=""
    max_checked_groups=0
    # micro_dict, only exist in cache (also in .selection file)
    # micro_name : int  ,  -2 means unchecked,  -1 means bad ,1 means good
    micro_dict={}
    type_dict={"All":0,"Good":1,"Bad":-1,"Unchecked":-2}
    groupi=0
    groups=1
    have_selection_file=0
    views={}

    def keyPressEvent(self, e) :
        if (e.key()==Qt.Key_PageDown or e.key()==Qt.Key_Down or e.key()==Qt.Key_Right):
            self.next_page()
        elif(e.key()==Qt.Key_PageUp or e.key()==Qt.Key_Up or e.key()==Qt.Key_Left ):
            self.pre_page()
        elif (e.key()==Qt.Key_F5):
            self.show_page()

    def __init__(self,parent=None):

        super(Childwindow,self).__init__(parent)
        #global sigma
        self.setupUi(self)
        self.backreader=[]
        self.backwriter=[]
        self.Draw_Pool=[]
        self.but_save.clicked.connect(self.save_selection)
        self.but_reload.clicked.connect(self.act_reload)
        self.log_sigma.setReadOnly(False)
        self.timer=QTimer()
        self.timer.timeout.connect(self.check)
        self.write_timer=QTimer()
        self.write_timer.timeout.connect(self.write_log)
        #self.signal=DrawT()
        self.but_clear.clicked.connect(self.clear_all_text)
        self.actionSelect_From_Files.triggered.connect(partial(self.act_open,"files"))
        self.actionSelect_From_Path.triggered.connect(partial(self.act_open, "path"))
        self.but_invert.clicked.connect(self.invert_selection)

        for windowi in range(6):
            graph_object=self.findChild(QGraphicsView,"graph_"+str(windowi))
            graph_object.mousePressEvent=partial(self.mouse_select,windowi)
            window_views[windowi]=None

        self.timer.start(1*2000)
        #self.timer_refresh=QTimer()
        #self.timer_refresh.timeout.connect(self.auto_refresh)
        #self.timer_refresh.start(1*3000)
        self.reslen=0


    def clear_all_text(self):
        self.log_text.clear()
        self.log_log.clear()

    def mkdir(self,dir):

        if not os.path.exists(dir):
            os.system("mkdir "+dir)
        else:
            if self.OV:
                print('Deleting old files in '+dir+'...')

                #os.system("rm -rf " + dir + '*')
            pass
           # os.system("rm "+dir+'*')

    def save_log(self):
        self.main_text_append( + "  saved. ", self.log_log)
    def save_selection(self):
        self.OV=self.Override.isChecked()

        if self.reslen==0:
            return

        self.good_dir=self.current_work_directory+"/good/"
        self.bad_dir=self.current_work_directory+"/bad/"
        #self.update_micro_dict()
        self.update_current_page_micro_dict()
       # print('Checkpoint in save_selection,,,after update_current_page_micro_dict')
        try:
            with open(self.backup_selection_file,'w',encoding='utf-8') as f :
                json.dump(self.micro_dict,f,ensure_ascii=False,indent=4)
                self.mkdir(self.good_dir)
                self.mkdir(self.bad_dir)
                self.single_writer()
                #self.back_writer()
        except:
            pass


    def invert_selection(self):
        if self.reslen == 0:
            return
        for i in range(6):
            ckbox = self.findChild(QCheckBox, "ck_" + str(i))
            try:
                selected_name=self.group_results[i]
            except:
                continue
            # duplicate code
            if self.micro_dict[selected_name]==-1:
                self.micro_dict[selected_name]=1
            else:
                self.micro_dict[selected_name]=-1
            # duplicate code
            ckbox.click()
        pass

    def mouse_select(self,windowid,event):
        try:
            selected_name=self.group_results[windowid]
            if self.micro_dict[selected_name]==-1:
                self.micro_dict[selected_name]=1
            else:
                self.micro_dict[selected_name]=-1

            #self.main_text_append(selected_name+"  is  selected. ",self.log_log)
            ck_object=self.findChild(QCheckBox,"ck_"+str(windowid))
            ck_object.click()
        except:
            pass


    def main_text_append(self,message,Qobj):
        current_text=Qobj.toPlainText()
        out_text=current_text+str(message)+"\n"
        Qobj.setText(out_text)
        Qobj.moveCursor(self.log_text.textCursor().End)
        pass

    def read_selection(self):
        if self.current_work_directory=="":
            temp_result=results[0]
            temp_result_split=temp_result.split('/')
            micro_name=temp_result_split[-1]
            self.current_work_directory=temp_result.replace(micro_name,"")
        self.backup_selection_file=self.current_work_directory+'/.selection'

        try:
            with open(self.backup_selection_file,'r',encoding='utf-8') as f:
                self.micro_dict=json.load(f)
            self.have_selection_file=1
        except:
            self.have_selection_file=0

            pass

    def pre_page(self):

        if self.groupi>0:
            self.groupi -= 1
        self.show_page()


    def display(self,obj,result):
        global snaps
        scence= QGraphicsScene()
        try:
            img = snaps[result]
            y, x = img.shape
            byte_img = img.tobytes()

            Qimg = QImage(byte_img,x,y,x,QImage.Format_Grayscale8)

            pix = QPixmap.fromImage(Qimg)

            item = QGraphicsPixmapItem(pix)
            scence.addItem(item)
            obj.setScene(scence)

        except Exception as exc:
            #print(exc)
            pass

    def show_page(self):
        global sigma
        sigma.value = float(self.log_sigma.toPlainText())
        scence = QGraphicsScene()
        self.group_results = results[self.groupi * 6:self.groupi * 6 + 6]
        resi = 0
        strs=str(self.groupi+1)+" / "+str(self.groups)
        self.label_current_groupi.setText(strs)
        self.temp_windows=[]
        #print(self.micro_dict)
        for i in range(6):
            graphview = self.findChild(QGraphicsView, "graph_" + str(i))
            #window_views[i]=scence
            graphview.setScene(scence)
            ckbox = self.findChild(QCheckBox, "ck_" + str(i))
            ckbox.setText("")
        for result in self.group_results:
            ckbox = self.findChild(QCheckBox, "ck_" + str(resi))
            ckbox.setText(result)
            if ckbox.isChecked():
                try:
                    if (self.micro_dict[result] == -1):
                        ckbox.click()
                except:
                    print('No selection information of ' + result)
                    ckbox.click()
                    pass
            else:
                try:
                    if (self.micro_dict[result] !=-1):
                        ckbox.click()
                except:
                    print('No selection information of ' + result)
                    pass

            graphview = self.findChild(QGraphicsView, "graph_" + str(resi))
            self.display(graphview,result)

            resi += 1

        self.get_current_good_micros()
        current_good=len(self.good_micros)
        self.log_log.clear()
        self.main_text_append(str(current_good)+' marked as good.',self.log_log)
        '''
        for windowid in range(6):
            graphview = self.findChild(QGraphicsView, "graph_" + str(windowid))
            graphview.setScene(window_views[windowid])
       '''
    def get_current_good_micros(self):
        ''' this function need s to be more efficient...
        because not all micros in dict should be checked.
        '''

        self.good_micros={}
        self.bad_micros={}
        for item in self.micro_dict:
            if self.micro_dict[item]==1:
                self.good_micros[item]=1
            elif self.micro_dict[item]==-1:
                self.bad_micros[item]=-1

    def update_current_page_micro_dict(self):
        # this function is used for automaticly update micro_dict , when
        # 1. turn to next without mouse clicking .
        # 2. save current_all_selection .
        # so only called in next_page() and save_selection()

        current_checked = min(self.reslen, (self.max_checked_groups + 1) * 6)
        last_page_index=max(0,self.max_checked_groups*6)
        checked_groups = results[last_page_index:current_checked]

        for item in checked_groups:
            if (self.micro_dict[item] != -1):
                self.micro_dict[item] = 1

        global final_micro_dict

        final_micro_dict = self.micro_dict.copy()


    def next_page(self):
        #self.update_micro_dict()
        if self.groupi<self.groups-1:
          self.groupi += 1
          # turn to next (new) page by default means that current page changed.
          if self.groupi>self.max_checked_groups:
            self.update_current_page_micro_dict()
        self.max_checked_groups=max(self.groupi,self.max_checked_groups)
        self.show_page()

    def calc_len(self):
        self.groups=int(self.reslen/6)
        if self.groups*6<self.reslen:
            self.groups+=1

    def read_mem(self):
        self.reslen=len(results)
        self.calc_len()
        self.temp_snaps=snaps.copy()

        kill_signal.value=1
        for name in self.temp_snaps:
            if name not in results:
                snaps.__delitem__(name)
        kill_signal.value=0

    def readtype_selection(self):
        '''But just in case you are openning a new directory from current workspace,
        which means you should update snaps(in memory) and results'''
        self.readtype = self.type_dict[self.combo_readtype.currentText()]
        global results
        temp_results = results.copy()
        '''  If no .selection file, All micros should be considered and readtype you'd better use 0 '''
        for item in temp_results:
            if item not in self.micro_dict:
                '''First meet, mark as -2 means unchecked.'''
                self.micro_dict[item] = -2
            '''Mark -2 step should be exec before other steps...'''
            '''After this ,have selection file or not doesn't matter...'''
            if self.readtype!=0 and self.readtype != self.micro_dict[item]:
                results.remove(item)

    def write_log(self):
        #good_num=int(os.popen('ls good |wc -l').read().split('\n')[0])
        #bad_num=int(os.popen('ls bad |wc -l').read().split('\n')[0])
        # BUG fixed.
        # relative path should not be used here.


        try:
            good_num=len(os.listdir(self.good_dir))
        except:
            good_num=0
        try:
            bad_num = len(os.listdir(self.bad_dir))
        except:
            bad_num = 0

        self.log_log.clear()
        self.main_text_append('good : ' + str(good_num) + ' / ' + str(self.good_len), self.log_log)
        self.main_text_append('bad : ' + str(bad_num) + ' / ' + str(self.bad_len), self.log_log)
        if good_num==self.good_len and  bad_num==self.bad_len:
            self.write_timer.stop()
            self.backprocess.kill()
            self.log_log.clear()
            self.main_text_append('Done. All saved.',self.log_log)

        pass

    def single_writer(self):

        try:
          self.write_timer.start(1*1000)
        except:
          pass
        self.get_current_good_micros()
        self.good_len=len(self.good_micros)
        self.bad_len=len(self.bad_micros)

        self.backprocess = multiprocessing.Process(target=BackendWriteProcess,args=(self.micro_dict,self.good_dir,self.bad_dir))
        self.backprocess.start()
        '''
        for item in self.micro_dict:
            print(item)
            micro_name=item.split('/')[-1]
            if self.micro_dict[item] == 1:
                #current_good += 1
                if not os.path.exists(self.good_dir+micro_name):
                    #pass
                    os.popen('ln -s ' + item + " " + self.good_dir)
            elif self.micro_dict[item] == -1:
                #current_bad += 1
                if not os.path.exists(self.bad_dir+micro_name):
                    #pass
                    os.popen('ln -s ' + item + " " + self.bad_dir)

        pass
        '''

    def back_reader(self):
        #=======need 6 processes to read
        for pro_i in range(6):
            temp_group_results = []
            for window_i in range(self.groups):
                current_position=window_i*6+pro_i

                if current_position<self.reslen:
                    if results[current_position] not in snaps:
                        temp_group_results.append(results[current_position])

            backprocess=multiprocessing.Process(target=BackendReadProcess,args=(temp_group_results,snaps,results,kill_signal))
            backprocess.start()

            self.backreader.append(backprocess)


    def process_reader(self):
        pool=Pool(processes=self.cores)
        data_len=len(results)
        for item in results:
            pool.apply_async(_PoolReader,(item,snaps,data_len))
        pool.close()
        #pool.join()

    def act_reload(self):

        kill_signal.value=1
        global sigma
        sigma.value=float(self.log_sigma.toPlainText())
        #time.sleep(10)
        global results
        results = glob(self.current_work_directory + "/*.mrc")
        self.groupi=0
        self.max_checked_groups=0
        self.act_load()

    def act_load(self):
        self.reslen=len(results)
        self.cores=int(self.log_cores.toPlainText())
        #kill_signal.value=1
        if self.reslen>0:

            # read .selection file first
            # for a new Directory, .selection does not exist so
            # have_selection_file = 0 . Do not create file here. This tag was used for init micro_dict
            self.read_selection()
            #show all? good? bad ?.
            # FOR a new Dir, readtype = all and all regarded as GOOD
            self.readtype_selection()
            # have some micros been cached already?

            self.read_mem()
            # start to read all uncached micros
           # kill_signal.value = 0
            self.process_reader()
            #read_mrcfiles_from_path(filepath=self.current_work_directory,cores=32,raw_data=snaps)
            #self.back_reader()

            self.show_page()

    def act_open(self,type):
        kill_signal.value=1
        self.groupi=0
        self.groups=1
        self.max_checked_groups=self.groupi
        global results
        global snaps
       # print(type)
        if type=="path":
            self.current_work_directory=QFileDialog.getExistingDirectory(self,"Choose Path",os.getcwd())
            #print(self.current_work_directory)
            results=glob(self.current_work_directory+"/*.mrc")
        elif type=="files":
            results = QFileDialog.getOpenFileNames(self, "Choose Path", os.getcwd())[0]
        sigma.value = float(self.log_sigma.toPlainText())
        self.act_load()

    def check(self):
        if kill_signal.value==0:
            self.log_text.clear()
            self.main_text_append(str(len(snaps)) + " / " + str(len(results)) + "   loaded.",self.log_text)
        else:
            self.log_text.clear()

    def auto_refresh(self):
        if len(snaps)!=0:
            self.show_page()

    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
          for reader in self.backreader:
            reader.terminate()
          '''
          for writer in self.backwriter:
            writer.terminate()
          '''

          print('Exit normally')
        except:
          print('Something wrong during exit...')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app=QApplication(sys.argv)
   # myform=Mywindow()

    c_window=Childwindow()
    c_window.show()
    #but_kdisplay=myform.but_kdisplay
    #but_kdisplay.clicked.connect(c_window.showMaximized)

    print('Entering Main window...')
    #myform.show()

    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
