#!/usr/bin/env python
#Author Fang K
#Contact Me : kongf21@mails.tsinghua.edu.cn

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
        global coords,rectleft,recttop,rectwidth,rectheight
        #global startpos,endpos

        startx, starty = self.lastPoint.x(), self.lastPoint.y()
        endx, endy = event.pos().x(), event.pos().y()

        rectleft=min(startx,endx)
        recttop=min(starty,endy)
        rectwidth=abs(startx-endx)
        rectheight=abs(starty-endy)



        # truesx, truesy = self.coord_conv(startx, starty)
        # trueex, trueey = self.coord_conv(endx, endy)
        #
        # angstartx,angstarty=self.coord2angle(truesx,truesy)
        # angex, angey = self.coord2angle(trueex, trueey)
        # ax=min(angstartx,angex)
        # ay=min(angstarty,angey)
        # bx=max(angstartx,angex)
        # by=max(angstarty,angey)



coords=[]
ax=ay=bx=by=0
class Anglewindow(QMainWindow,aw.Ui_ang):
    def __init__(self,parent=None):

        super(Anglewindow,self).__init__(parent)
        self.setupUi(self)
        pg.setConfigOption('background','w')
        self.scatters=None
        self.drawing = False
        self.brushSize = 1
        self.brushColor = QColor(255,255,0)
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
        self.actionSet_Erase_Percent.triggered.connect(self.erase_percent)
        self.actionSave_Star_File.triggered.connect(self.save_star)

    def erase_percent(self,percent):
        self.percent=0
        percent,ok=QInputDialog.getDouble(self,'Percent','',0.33,-1,1,2)
        if ok:
            self.percent=percent

    def brush_settings(self,type):
        if type=="size":
            size,ok = QInputDialog.getInt(self,'Brush Size','',1,1,20,1)
            if ok:
                self.brushSize=size

        if type=="color":
            self.brushColor=QColorDialog.getColor()

        if self.scatters is not None:
            self.scatters.setSize(self.brushSize)
            self.scatters.setBrush(pg.mkBrush(self.brushColor))

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
        global coords
        global rectleft,recttop,rectwidth,rectheight
        #print(rectleft,recttop,rectwidth,rectheight)
        map_rect=self.scatters.mapRectFromDevice(QRectF(rectleft,recttop,rectwidth,rectheight))
        #print(map_rect)
        l,b,r,t=map_rect.left(),map_rect.bottom(),map_rect.right(),map_rect.top()

        minx,maxx,miny,maxy=min(l,r),max(l,r),min(b,t),max(b,t)

        total=len(coords)
        current=0
        bool_index=[]
        percent=abs(self.percent)
        if self.percent<0:
          base_b=True
        else:
          base_b=False
        for coord in coords:
            print("\r", end="", flush=True)
            print(str(current)+'/'+str(total),end="")
            current+=1
            if coord[0]>minx and coord[0]<maxx and coord[1]>miny and coord[1]< maxy and np.random.rand()<percent:
                bool_index.append(base_b)
            else:
                bool_index.append(not base_b)
        coords=coords[np.array(bool_index)]

        self.plot_coords()

    def plot_coords(self):
        self.plot_window = angplot()

        self.scatters = pg.ScatterPlotItem(size=self.brushSize, brush=pg.mkBrush(self.brushColor))

        # print(coords)

        x = coords[:, 0]
        y = coords[:, 1]
        #
        #scatters.setData(x, y)
        #Use addPoint instead.
        self.scatters.addPoints(x,y)


        # # self.graphWidget.addItem(scatters)
        self.plot_window.addItem(self.scatters)
        # self.plot_window.scaleToImage(self.image)
        #
        self.setCentralWidget(self.plot_window)

    def plot_particles(self):
        #print(self.filename)
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