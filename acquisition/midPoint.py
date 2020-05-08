import math

from PySide2 import QtCore, QtGui, QtWidgets

class MidPoint(QtWidgets.QGraphicsItem):
    BoundingRect = QtCore.QRectF(-20, -20, 40, 40)

    def __init__(self):
        super(MidPoint, self).__init__()

    def boundingRect(self):
        return MidPoint.BoundingRect

    def setDist (self, dist):
        self.dist=dist
    def setMidPoint (self, p):
        self.midPoint=p
    def setHumansPoints(self,p1,p2):
        self.human_point1=p1
        self.human_point2=p2        
    
    def paint(self, painter, option, widget):        
        #pass
        #painter.setBrush(QtCore.Qt.red)        
        
        line = QtCore.QLineF(self.human_point1,self.human_point2)
        painter.drawLine(line)
                
        if (self.dist >65 ):
            font = painter.font()
            font.setPixelSize(22)
            painter.setFont(font)
            text = f"{self.dist/100:.2f}" #truncate float to 2 decimal
            painter.drawText(self.midPoint,text+'m')        
        
        #punto_medio = QtCore.QPointF(x_pm, y_pm) # Coordenada x e y.

        #angleline = QtCore.QLineF()
        #angleline.setP1(self.midPoint)
        #angleline.setAngle(angleline.angleTo(line))                  
        #painter.drawLine(angleline)
        #print("angleTo",angleline.angleTo(line))
        
        # Body
        # painter.setBrush(QtCore.Qt.red)
        # bodyPolygon = QtGui.QPolygon()
        # bodyPolygon.append(QtCore.QPoint(-20, 20))
        # bodyPolygon.append(QtCore.QPoint(-20, -13))
        # bodyPolygon.append(QtCore.QPoint(-13, -20))

        # bodyPolygon.append(QtCore.QPoint(13, -20))
        # bodyPolygon.append(QtCore.QPoint(20, -13))
        # bodyPolygon.append(QtCore.QPoint(20, 20))

        # bodyPolygon.append(QtCore.QPoint(-20, 20))
        # painter.drawPolygon(bodyPolygon)
        # # Wheels
        # painter.setBrush(QtCore.Qt.black)
        # painter.drawRect(+18-4, -8, 8, 16)
        # painter.drawRect(-18-4, -8, 8, 16)

        # nosePolygon = QtGui.QPolygon()
        # nosePolygon.append(QtCore.QPoint(0, -22))
        # nosePolygon.append(QtCore.QPoint(-10, -15))
        # nosePolygon.append(QtCore.QPoint(10, -15))
        # nosePolygon.append(QtCore.QPoint(0, -22))
        # painter.drawPolygon(nosePolygon)
