#!/usr/bin/env python
#Author Fang Kong @Tsinghua Univ.
#email : kongf21@tsinghua.edu.cn

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import ang_window as aw
import pyqtgraph as pg
import numpy as np
from pyqtgraph import PlotWidget,plot
from re_read import *
from functools import partial

class angplot(PlotWidget):
    def __init__(self):
        super(angplot, self).__init__()

        #print(self.centralWidget.size())
        self.lastPoint=QPoint()


    def coord_conv(self,x,y):
        x=max(0,min(1024,x))
        y=max(0,min(755,y))

        return x/1024*640,y/755*480

    def coord2angle(self,x,y):
        return x/640*360-180,180-y/480*180

    def mousePressEvent(self, event):
        super(angplot,self).mousePressEvent(event)

        self.lastPoint=event.pos()
        #print(event.pos())
    def mouseMoveEvent(self, event):
        super(angplot, self).mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        global coords,ax,ay,bx,by
        startx, starty = self.lastPoint.x(), self.lastPoint.y()
        endx, endy = event.pos().x(), event.pos().y()
        #print(QPoint)
        truesx, truesy = self.coord_conv(startx, starty)
        trueex, trueey = self.coord_conv(endx, endy)
        #print(truesx,truesy)
        #print(self.coords)
        angstartx,angstarty=self.coord2angle(truesx,truesy)
        angex, angey = self.coord2angle(trueex, trueey)
        ax=min(angstartx,angex)
        ay=min(angstarty,angey)
        bx=max(angstartx,angex)
        by=max(angstarty,angey)


coords=[]
ax=ay=bx=by=0
class Anglewindow(QMainWindow,aw.Ui_ang):
    def __init__(self,parent=None):

        super(Anglewindow,self).__init__(parent)
        self.setupUi(self)
        pg.setConfigOption('background','w')
        self.drawing = False
        self.brushSize = 1
        self.brushColor = QColor(255,255,255)
        self.lastPoint = QPoint()
        self.filename=None
        pg.setConfigOption('leftButtonPan',False)
        #self.somewidget=SomeWidget()
        #self.setCentralWidget(self.somewidget)

        self.actionOpen_Star_File.triggered.connect(self.act_open)
        self.actionChoose_color.triggered.connect(partial(self.brush_settings,"color"))
        self.actionSet_Brush_Size.triggered.connect(partial(self.brush_settings,"size"))
        self.actionFade.triggered.connect(self.fade)
        self.percent=0.5
        self.action10.triggered.connect(partial(self.erase_percent,0.1))
        self.action30.triggered.connect(partial(self.erase_percent,0.3))
        self.action70.triggered.connect(partial(self.erase_percent,0.7))
        self.actionSave_Star_File.triggered.connect(self.save_star)

    def erase_percent(self,percent):
        self.percent=percent



    def brush_settings(self,type):
        if type=="size":
            self.brushSize=1
        if type=="color":
            self.brushColor=QColorDialog.getColor()

    def save_star(self):
        head_line=make_head(self.filename)
        outfilename=QFileDialog.getSaveFileName(self,'Save File As')[0]
        outfile=open(outfilename,'w+')
        lines=open(self.filename).read().split('\n')
        for li in range(head_line):
            if li<head_line:
                outfile.write(lines[li])
                outfile.write('\n')
        for coord in coords:
            outfile.write(lines[head_line+int(coord[2])])
            outfile.write('\n')

        pass

    def fade(self):
        global coords,ax,ay,bx,by
        #print(ax,ay,bx,by)
        total=len(coords)
        current=0
        bool_index=[]
        for coord in coords:
            print("\r", end="", flush=True)
            print(str(current)+'/'+str(total),end="")
            current+=1
            if coord[0]>ax and coord[0]<bx and coord[1]>ay and coord[1]< by and np.random.rand()<self.percent:
                bool_index.append(False)
            else:
                bool_index.append(True)
        coords=coords[np.array(bool_index)]

        self.plot_coords()

    def plot_coords(self):
        self.plot_window = angplot()
        # # self.plot_window.setBackground(Qt.white)
        #
        scatters = pg.ScatterPlotItem(size=self.brushSize, brush=pg.mkBrush(self.brushColor))
        # print(coords)
        #
        x = coords[:, 0]
        y = coords[:, 1]
        #
        scatters.setData(x, y)

        # # self.graphWidget.addItem(scatters)
        self.plot_window.addItem(scatters)
        # self.plot_window.scaleToImage(self.image)
        #
        self.setCentralWidget(self.plot_window)

    def plot_particles(self):
        print(self.filename)
        if self.filename==None:
            return
        global coords
        coords = read_starfile(self.filename)
        self.plot_coords()



    def act_open(self):

        self.filename=QFileDialog.getOpenFileName()[0]
        if self.filename==None:
            return
        try:
          self.plot_particles()
        except:
          return


if __name__ == '__main__':
    app=QApplication(sys.argv)
   # myform=Mywindow()

    c_window=Anglewindow()
    c_window.show()

    print('Entering Main window...')
    #myform.show()

    sys.exit(app.exec())
