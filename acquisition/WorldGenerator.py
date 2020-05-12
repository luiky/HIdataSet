import random
import math, numpy
import json
import time

from PySide2 import QtCore, QtGui, QtWidgets

from human import Human, Head
from robot import Robot
from midPoint import MidPoint
from regularobject import RegularObject
from irregularobject import IrregularObject
from room import Room
from interaction import Interaction

MAX_GENERATION_WAIT = 1.

class WorldGenerator(QtWidgets.QGraphicsScene):
    available_identifier = 0

    def __init__(self, data=None):
        super(WorldGenerator, self).__init__()
        self.setSceneRect(-400, -400, 800 - 2, 800 - 2)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        if data is None:
            self.generateRandomWorld()
        else:
            self.generateFromData(data)

    def generateFromData(self, raw_data):
        data = json.loads(raw_data)
        idMap = dict()
        self.clear()

        self.ds_identifier = int(data['identifier'].split()[0])

        self.room = Room(data['room'])
        self.addItem(self.room)

        self.humans = []
        for raw_human in data['humans']:
            human = Human.from_json(raw_human)
            self.addItem(human)
            self.humans.append(human)
            idMap[raw_human['id']] = human

        self.heads = []
        for raw_head in data['heads']:
            head = Head.from_json(raw_head)
            self.addItem(head)
            self.heads.append(head)
            idMap[raw_head['id']] = head
            
        self.objects = []
        for raw_object in data['objects']:
            obj = RegularObject.from_json(raw_object)
            self.addItem(obj)
            self.objects.append(obj)
            idMap[raw_object['id']] = obj

        self.interactions = []
        interactions_done = []
        for interaction_raw in data['links']:
            if not [interaction_raw[1], interaction_raw[0], interaction_raw[2]] in interactions_done:
                interactions_done.append(interaction_raw)
                human = idMap[interaction_raw[0]]
                other = idMap[interaction_raw[1]]
                interaction = Interaction(human, other)
                self.interactions.append(interaction)
                self.addItem(interaction)

        #self.irregularobjects = []
        #for raw_irregularobjects in data['irregularobjects']:
            #obj = IrregularObject.from_json(raw_irregularobjects)
            #self.addItem(obj)
            #self.irregularobjects.append(obj)
            #idMap[raw_irregularobjects['id']] = obj


        self.robot = Robot()
        self.robot.setPos(0, 0)
        self.addItem(self.robot)

    def generateRandomWorld(self):
        done = False
        self.ds_identifier = WorldGenerator.available_identifier
        WorldGenerator.available_identifier += 1
        while not done:
            try:
                self.generation_time = time.time()
                self.generate()
                done = True
                # print(time.time()-self.generation_time)
            except RuntimeError:
                pass        

    @staticmethod
    def distanceTo(something):
        return int(math.sqrt(something.xPos*something.xPos + something.yPos*something.yPos))

    @staticmethod
    def angleTo(something):
        angle = int(int(180.*math.atan2(something.yPos, something.xPos)/math.pi)+90.)
        if angle > 180.: angle = -360.+angle
        return angle

    def serialize(self, score=-1):
        structure = dict()
        structure['identifier'] = str(self.ds_identifier).zfill(5) + ' A'
        structure['score'] = 0
        if score > 0:
            structure['score'] = score
        structure['robot'] = {'id': 0}

        humansList = []
        for human in self.humans:
            h = dict()
            h['id'] = human.id
            h['xPos'] = +human.xPos
            h['yPos'] = +human.yPos
            h['orientation'] = +human.angle
            h['head_orientation'] = +human.angleHead
            humansList.append(h)
        structure['humans'] = humansList
        
        headsList = []
        for head in self.heads:
            h = dict()
            h['id'] = head.id
            h['xPos'] = +head.xPos
            h['yPos'] = +head.yPos
            h['orientation'] = +head.angle
            headsList.append(h)
        structure['heads'] = headsList

        objectsList = []
        for object in self.objects:
            o = dict()
            o['id'] = object.id
            o['xPos'] = +object.xPos
            o['yPos'] = +object.yPos
            o['orientation'] = +object.angle
            objectsList.append(o)
        structure['objects'] = objectsList

        structure['links'] = []
        for interaction in self.interactions:
            structure['links'].append( [interaction.a.id, interaction.b.id, 'interact'] )
            if type(interaction.b) is Human:
                structure['links'].append( [interaction.b.id, interaction.a.id, 'interact'] )

        #irregularObjectsList = []
        #for object in self.irregularobjects:
            #o = dict()
            #o['id'] = object.id
            #o['xPos'] = +object.xPos
            #o['yPos'] = +object.yPos             
            #o['w'] = +object.w             
            #o['h'] = +object.h
            #o['orientation'] = +object.angle
            #irregularObjectsList.append(o)
        #structure['irregularobjects'] = irregularObjectsList

        structure['room'] = [ [+point.x(), point.y()] for point in self.room.poly ]

        if score >= 0:
            print(json.dumps(structure))

        return structure

    def generateHuman(self, availableId):
        human = None
        while human is None:
            if time.time() - self.generation_time > MAX_GENERATION_WAIT:
                raise RuntimeError('MAX_GENERATION_ATTEMPTS')
            if QtCore.qrand() % 3 == 0:
                xx = int(random.normalvariate(0, 150))
                yy = int(random.normalvariate(0, 150))
            else:
                xx = QtCore.qrand()%800-400
                yy = QtCore.qrand()%800-400                
            
            angleHuman = (QtCore.qrand()%360)-180
            angleHead = angleHuman + random.choice([-1,1])*QtCore.qrand()%100
            human = Human(availableId, xx, yy, angleHuman, angleHead)
            if not self.room.containsPolygon(human.polygon()):
                human = None
        return human

    def generateComplementaryHuman(self, human, availableId):
        a = math.pi*human.angle/180.
        dist = float(QtCore.qrand()%300+50)
        human2 = None
        while human2 is None:
            if time.time() - self.generation_time > MAX_GENERATION_WAIT:
                raise RuntimeError('MAX_GENERATION_ATTEMPTS')
            xPos = human.xPos+dist*math.sin(a)
            yPos = human.yPos-dist*math.cos(a)
            human2 = Human(availableId, xPos, yPos, human.angle+180)
            if not self.room.containsPolygon(human2.polygon()):
                dist -= 5
                if dist < 20:
                    human.setAngle(human.angle+180)
                    a = math.pi*human.angle/180.
                    dist = float(QtCore.qrand()%300+50)
                human2 = None
        return human2
    
    #def generateHumanHead(self, human):
        #head = None
        #while head is None:
            ##print ("human.angle", human.angle)
            #angle = human.angle + random.choice([-1,1])*QtCore.qrand()%100                                    
            #if angle > 180.: angle = -360. + angle            
            #if angle < -180.: angle = angle + 360
            #head = Head(human.id, human.xPos, human.yPos, angle)
            ##if -180 <= a <= 180:            
        #return head

    def generateComplementaryObject(self, human, availableId):
        a = math.pi*human.angle/180.
        dist = float(QtCore.qrand()%250+50)
        obj = None
        while obj is None:
            if time.time() - self.generation_time > MAX_GENERATION_WAIT:
                raise RuntimeError('MAX_GENERATION_ATTEMPTS')
            xPos = human.xPos+dist*math.sin(a)
            yPos = human.yPos-dist*math.cos(a)
            obj = RegularObject(availableId, xPos, yPos, (human.angle+180)%360)
            if not self.room.containsPolygon(obj.polygon()):
                dist -= 5
                if dist <= 5:
                    obj.setAngle(human.angle+180)
                    a = math.pi*human.angle/180.
                    dist = float(QtCore.qrand()%300+50)
                obj = None
        return obj
    
    def generateInteractuatorHuman(self, human, availableId):
        a = math.pi*human.angle/180. #a radianes
        dist = float(QtCore.qrand()%300+50)
        human2 = None
        while human2 is None:
            if time.time() - self.generation_time > MAX_GENERATION_WAIT:
                raise RuntimeError('MAX_GENERATION_ATTEMPTS')
            xPos = human.xPos+dist*math.sin(a)
            yPos = human.yPos-dist*math.cos(a)
            l = [1,-1]
            option = random.choice (l)
            angle = human.angle+180 + (option*QtCore.qrand()%25)
            # print('angle human2:', angle)
            if angle > 180.: angle = -360. + angle
            # print('angle human2 normalize:', angle)
            angleHead = angle + random.choice([-1,1])*QtCore.qrand()%100
            human2 = Human(availableId, xPos, yPos, angle,angleHead)
            if not self.room.containsPolygon(human2.polygon()):
                dist -= 5
                if dist < 20:
                     human.setAngle(human.angle+180)
                     a = math.pi*human.angle/180.
                     dist = float(QtCore.qrand()%300+50)
                human2 = None
        return human2

    def generateObject(self, availableId):
        object = None
        while object is None:
            if time.time() - self.generation_time > MAX_GENERATION_WAIT:
                raise RuntimeError('MAX_GENERATION_ATTEMPTS')
            if QtCore.qrand() % 3 == 0:
                xx = int(random.normalvariate(0, 150))
                yy = int(random.normalvariate(0, 150))
            else:
                xx = QtCore.qrand()%800-400
                yy = QtCore.qrand()%800-400
            object = RegularObject(availableId, xx, yy, (QtCore.qrand()%360)-180)        
            if not self.room.containsPolygon(object.polygon()):
                object = None   
            
        return object

    def generateIrregularObject(self, availableId):
        object = None
        while object is None:
            if time.time() - self.generation_time > MAX_GENERATION_WAIT:
                raise RuntimeError('MAX_GENERATION_ATTEMPTS')
            if QtCore.qrand() % 3 == 0:
                xx = int(random.normalvariate(0, 150))
                yy = int(random.normalvariate(0, 150))
                ww = int(random.normalvariate(20, 50))
                hh = int(random.normalvariate(20, 50))
            else:
                xx = QtCore.qrand()%800-400
                yy = QtCore.qrand()%800-400
                ww = QtCore.qrand()%800/4-400/4
                hh = QtCore.qrand()%800/4-400/4
            if (ww>10 and hh>10):                
                object = IrregularObject(availableId, xx, yy, ww, hh, (QtCore.qrand()%360)-180)                     
            if object is not None:                   
                if not self.room.containsPolygon(object.polygon()):
                    object = None   
            
        return object

    def generate(self):
        regenerateScene = True
        while regenerateScene:

            availableId = 1
            regenerateScene = False
            self.clear()
            self.humans = []
            self.heads = []
            self.objects = []
            self.interactions = []            
            #self.irregularobjects =[]            

            self.room = Room()
            self.addItem(self.room)

            #ONLY TWO HUMAN BEINGS
            human = self.generateHuman(availableId)
            head = Head (human.id, human.xPos, human.yPos, human.angleHead )
            #head = self.generateHumanHead(human)
            availableId += 1
            self.addItem(human)
            self.humans.append(human)
            
            #heads
            self.addItem(head)
            #self.heads.append(head)
            
            human2 = None
            while human2 is None:                
                if QtCore.qrand()%2 == 0:
                    human2 = self.generateInteractuatorHuman(human, availableId)                                                                
                    #CHECK necesito crear interaccion?
                    # interaction = Interaction(human, human2)
                    # self.interactions.append(interaction)
                    # self.addItem(interaction)                    
                else:
                    human2 = self.generateHuman(availableId)                
                if human.polygon().intersects(human2.polygon()):                    
                    human2=None
                    
            head2 = Head (human2.id, human2.xPos, human2.yPos, human2.angleHead )
            #head2 = self.generateHumanHead(human2)
            #print ("-----")
            availableId += 1
            self.addItem(human2)
            self.humans.append(human2)
            #heads
            self.addItem(head2)
            #self.heads.append(head2)
            
            # Calculamos el punto medio de los dos humanos. Adri
            x1 = human.xPos
            y1 = human.yPos
            x2 = human2.xPos
            y2 = human2.yPos
            x_pm = (x1 + x2)/2 
            y_pm = (y1 + y2)/2 
            punto_medio = QtCore.QPointF(x_pm, y_pm) # Coordenada x e y.
            punto_human = QtCore.QPointF(x1, y1) # Coordenada humano 1
            punto_human2 = QtCore.QPointF(x2, y2) # Coordenada humano 2.  
            
            a = numpy.array((x1 ,y1))
            b = numpy.array((x2, y2))
            dist = numpy.linalg.norm(a-b)
            
            self.midPoint = MidPoint()            
            self.midPoint.setHumansPoints(punto_human,punto_human2)
            self.midPoint.setMidPoint(punto_medio)
            self.midPoint.setDist(dist)
            self.addItem(self.midPoint)

            

            #genero objetos  regulares 
            # objectCount = int(abs(random.normalvariate(1, 4))) % 5
            # #print ("objectCount",objectCount)
            # if objectCount == 0:
            #     objectCount = QtCore.qrand() % 3
            # for i in range(objectCount):
            #     # print (i)
            #     object = self.generateObject(availableId)                  
            #     #Chequeo sino intersecta con otro objeto ya creado
            #     if any (object.polygon().intersects(x.polygon()) for x in self.objects):                                 
            #         continue
            #     #check is colide with human beings
            #     if any (object.polygon().intersects(x.polygon()) for x in self.humans):                                                
            #         continue
                   
            #     availableId += 1
            #     self.addItem(object)
            #     self.objects.append(object)
            
            #genero objetos IRREGULARES
            #objectCount = int(abs(random.normalvariate(1, 4))) % 15
            ## print ("irregular objects",objectCount)
            #if objectCount == 0:
                #objectCount = QtCore.qrand() % 3

            #for i in range(objectCount):
                ## print (i)
                #object = self.generateIrregularObject(availableId)                
                ###check if intersect with regular IRREGULARobjects
                #if any (object.polygon().intersects(x.polygon()) for x in self.irregularobjects):                                  
                    #continue
                ##check if intersect with humans
                #if any (object.polygon().intersects(x.polygon()) for x in self.humans):                                  
                    #continue
                ##check if intersect with regular objects
                #if any (object.polygon().intersects(x.polygon()) for x in self.objects):                                                      
                    #continue
                   
                #availableId += 1
                #self.addItem(object)
                #self.irregularobjects.append(object)
            
            #print ("----Sel.irregularobjets: len", len(self.irregularobjects))                        
            #print ("----Self.objects: len", len(self.objects))
            self.robot = Robot()
            self.robot.setPos(0, 0)
            self.addItem(self.robot)



        #self.text = 'Humans:' + str(len(self.humans)) + ' ' + 'Objects:' + str(len(self.objects))+ ' ' + 'Irregular Objects:' + str(len(self.irregularobjects))



