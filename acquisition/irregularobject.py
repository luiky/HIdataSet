import math
import random

from PySide2 import QtCore, QtGui, QtWidgets

from polygonmisc import rotatePolygon, translatePolygon

class IrregularObject(QtWidgets.QGraphicsItem):
    #BoundingRect = QtCore.QRectF(-20, -20, 40, 40)

    def __init__(self, id, xPos, yPos,w,h, angle):
        super(IrregularObject, self).__init__()
        self.id = id
        self.xPos = xPos
        self.yPos = yPos
        self.w = w
        self.h = h
        self.setAngle(angle)
        self.setPos(self.xPos, self.yPos)
        self.alto = int(QtCore.qrand()%255)
        # print ("random alto" , self.alto)  
              
        self.colour = QtGui.QColor(0,0,0,self.alto) #QtCore.Qt.green        
        #self.BoundingRect =QtCore.QRectF(-20, -20, 40, 40)
        self.BoundingRect =QtCore.QRectF(-w, -h, w*2, h*2)
        

    @classmethod
    def from_json(IrregularObject, json_data):
        id = json_data['id']
        xPos = json_data['xPos']
        yPos = json_data['yPos']
        w = json_data['w']
        h = json_data['h']
        angle = json_data['orientation']
        return IrregularObject(id, xPos, yPos, w, h, angle)


    def setAngle(self, a):
        self.angle = a
        if self.angle > 180.:
            self.angle = -360.+self.angle
        self.setRotation(self.angle)

    def polygon(self):
        #w = 20
        #h = 20
        polygon = QtGui.QPolygon()
        polygon.append( QtCore.QPoint(-self.w, -self.h) )
        polygon.append( QtCore.QPoint(-self.w, +self.h) )
        polygon.append( QtCore.QPoint(+self.w, +self.h) )
        polygon.append( QtCore.QPoint(+self.w, -self.h) )
        polygon.append( QtCore.QPoint(-self.w, -self.h) )
        polygon = rotatePolygon(polygon, theta=self.angle*math.pi/180.)
        polygon = translatePolygon(polygon, tx=self.xPos, ty=self.yPos)
        return polygon


    def boundingRect(self):
        return self.BoundingRect

    def paint(self, painter, option, widget):
        # Body     
        # painter.setBrush(QtGui.QColor(0,0,0,200))
        painter.setBrush(self.colour)        
        painter.drawRect(self.BoundingRect)

