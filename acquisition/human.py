import math
from PySide2 import QtCore, QtGui, QtWidgets

from polygonmisc import rotatePolygon, translatePolygon


class Human(QtWidgets.QGraphicsItem):
    #BoundingRect = QtCore.QRectF(-20, -10, 40, 20)
    BoundingRect = QtCore.QRectF(-30, -15, 60, 30)

    def __init__(self, id, xPos, yPos, angle, angleHead=None):
        super(Human, self).__init__()
        self.id = id
        self.xPos = xPos
        self.yPos = yPos
        self.setAngle(angle)
        #self.itemHead =QtWidgets.QGraphicsItem()        
        if angleHead is None:
            self.setAngleHead(angle)
        else:
            self.setAngleHead(angleHead)
            
        self.setPos(self.xPos, self.yPos)
        self.setZValue(1)
        self.colour = QtCore.Qt.transparent
        self.pixmapBody = QtGui.QPixmap("body.png")      
        #self.pixmapHead = QtGui.QPixmap("head.png")        
        #self.pixmap = QtGui.QPixmap("person.png")
        
        self.factor = 1.5 #multiplicar tamaño del poligono, para estar acorde con el boundingrect

    @classmethod
    def from_json(Human, json_data):
        id = json_data['id']
        xPos = json_data['xPos']
        yPos = json_data['yPos']
        angle = json_data['orientation']
        return Human(id, xPos, yPos, angle)

    def setAngle(self, a):
        self.angle = a
        if self.angle > 180.:
            self.angle = -360.+self.angle
        self.setRotation(self.angle) #qt
        
    def setAngleHead(self, a):
        self.angleHead = a
        if self.angleHead > 180.: 
            self.angleHead = -360. + self.angleHead        
        if self.angleHead < -180.: 
            self.angleHead = self.angleHead + 360                                        
    def boundingRect(self):
        return Human.BoundingRect

    def polygon(self):
        w = 20 *self.factor
        h = 10 *self.factor
        polygon = QtGui.QPolygon()
        polygon.append( QtCore.QPoint(-w, -h) )
        polygon.append( QtCore.QPoint(-w, +h) )
        polygon.append( QtCore.QPoint(+w, +h) )
        polygon.append( QtCore.QPoint(+w, -h) )
        polygon.append( QtCore.QPoint(-w, -h) )
        polygon = rotatePolygon(polygon, theta=self.angle*math.pi/180.)
        polygon = translatePolygon(polygon, tx=self.xPos, ty=self.yPos)
        return polygon

    def paint(self, painter, option, widget):
        painter.setBrush(self.colour)
        # painter.drawRect(self.BoundingRect)
        #print ("self.angle", self.angle)
        #print ("self.angleHead",self.angleHead)
        #print ("self.rotation",self.rotation())
        painter.drawPixmap(self.BoundingRect.toRect(),self.pixmapBody)        
        #painter.drawPixmap(self.BoundingRect.toRect(),self.pixmapHead)
        
        #id
        #painter.drawText(20,20,str(self.id))    
        # # Body
        # painter.setBrush(self.colour)
        # painter.drawEllipse(self.BoundingRect)
        # # Eyes
        # painter.setBrush(QtCore.Qt.white)
        # painter.drawEllipse(+8-4, -8-4, 8, 8)
        # painter.drawEllipse(-8-4, -8-4, 8, 8)
        # # Pupils
        # painter.setBrush(QtCore.Qt.black)
        # painter.drawEllipse(QtCore.QRectF(-8-2, -9-2, 4, 4))
        # painter.drawEllipse(QtCore.QRectF(+8-2, -9-2, 4, 4))

class Head(QtWidgets.QGraphicsItem):
    #BoundingRect = QtCore.QRectF(-20, -10, 40, 20)
    BoundingRect = QtCore.QRectF(-30, -15, 60, 30)

    #def __init__(self, id, xPos, yPos, angle):
    def __init__(self, id, xPos, yPos, angle):
        super(Head, self).__init__()
        self.id = id
        self.xPos = xPos
        self.yPos = yPos
        self.setAngle(angle)
        self.setPos(self.xPos, self.yPos)
        self.setZValue(1)
        self.colour = QtCore.Qt.transparent
        self.pixmap = QtGui.QPixmap("head.png")        
        self.factor = 1.5 #multiplicar tamaño del poligono, para estar acorde con el boundingrect

    @classmethod
    def from_json(Head, json_data):
        id = json_data['id']
        xPos = json_data['xPos']
        yPos = json_data['yPos']
        angle = json_data['orientation']
        return Head(id, xPos, yPos, angle)

    def setAngle(self, a):
        self.angle = a
        if self.angle > 180.:
            self.angle = -360.+self.angle
        self.setRotation(self.angle)

    def boundingRect(self):
        return Head.BoundingRect

    def polygon(self):
        w = 20 *self.factor
        h = 10 *self.factor
        polygon = QtGui.QPolygon()
        polygon.append( QtCore.QPoint(-w, -h) )
        polygon.append( QtCore.QPoint(-w, +h) )
        polygon.append( QtCore.QPoint(+w, +h) )
        polygon.append( QtCore.QPoint(+w, -h) )
        polygon.append( QtCore.QPoint(-w, -h) )
        polygon = rotatePolygon(polygon, theta=self.angle*math.pi/180.)
        polygon = translatePolygon(polygon, tx=self.xPos, ty=self.yPos)
        return polygon

    def paint(self, painter, option, widget):
        painter.setBrush(self.colour)
        # painter.drawRect(self.BoundingRect)
        painter.drawPixmap(self.BoundingRect.toRect(),self.pixmap) 
        
