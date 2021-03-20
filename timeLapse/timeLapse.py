
from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import subprocess
import time
"""
import multiprocessing as mp
from multiprocessing import Process, Pipe

aD = Krita.activeDocument()
path = 'C:\\Users\\Gregor\\Desktop\\image.png'
iO = krita.InfoObject()
aD.setBatchmode(True)
print(aD.batchmode())

iO.setProperties({"alpha":True,"compression":5,"forceSRGB":False,"indexed":True,"interlaced":False,"saveSRGBProfile":False,"transparencyFillcolor":[255,255,255]})
if (aD.exportImage(path,iO)):
    print("success")
"""

"""
_________________________________________________________________
--- this makes krita crash
--- new approach QTimer
--- also look into exporting vs saving than loading and exporting
_________________________________________________________________

class WorkerThread(QThread):
    def run():
        doc = Krita.instance().activeDocument()
        doc.setBatchmode(True)
"""

class timeLapseDocker(DockWidget):


    """
    _________________________________________________________
    --- part of failed multi processing approach see line 119
    _________________________________________________________
    timerIn_conn, timerOut_conn = Pipe()
    iO = None
    aD = None
    path = None
    p = None
    def rec(in_conn,document,path,io,sT):
        c = 0
        while in_conn.recv() == 1:
            document.exportImage(path+str(c),io)
            c += 1
            time.sleep(sT)
    """


    def __init__(self):
        super().__init__()
        self.fieldPath = QLineEdit()
        self.fieldFFMPath = QLineEdit()

        self.setWindowTitle("Time Lapse")
        mainWidget = QWidget(self)
        RGBWidget = QWidget(self)
        self.setWidget(mainWidget)
        #vLayout = QVBoxLayout()
        hLayout = QHBoxLayout()
        gLayout = QGridLayout()
        #fLayout = QFormLayout()
        mainWidget.setLayout(gLayout)
        RGBWidget.setLayout(hLayout)

        self.saveCounter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.saveImage)

        self.buttonStartRecording = QPushButton("Start")
        self.buttonStartRecording.clicked.connect(self.startRec)
        self.buttonStartRecording.setEnabled(True)
        self.buttonStopRecording = QPushButton("Stop")
        self.buttonStopRecording.clicked.connect(self.stopRec)
        self.buttonStopRecording.setEnabled(False)

        self.checkBoxAlpha = QCheckBox("Alpha")
        self.checkBoxForceSRGB = QCheckBox("Force SRGB")
        self.checkBoxInterlaced = QCheckBox("Interlaced")
        self.checkBoxSaveSRGBProfile = QCheckBox("Save SRGB Profile")

        self.fieldCompression = QSpinBox()
        self.fieldCompression.setRange(1,9)
        self.fieldCompression.setPrefix("Compression -  ")
        self.fieldFPS = QSpinBox()
        self.fieldFPS.setRange(24,60)
        self.fieldFPS.setPrefix("Frames per second -  ")
        self.fieldImageInterval = QSpinBox()
        self.fieldImageInterval.setRange(10,7200)
        self.fieldImageInterval.setPrefix("Take an image every  ")
        self.fieldImageInterval.setSuffix("  seconds")

        rx = QRegExp("(C|D):\\\\([a-zA-Z]+\\\\*)*")
        validator = QRegExpValidator(rx, self)

        self.PathLabel = QLabel("Path:  ")
        self.FFMPathLabel = QLabel("FFmpeg Path:")
        self.fieldPath.setValidator(validator)
        self.fieldFFMPath.setValidator(validator)

        self.RGBLabel = QLabel("Transparency Fillcolor: ")
        self.RField = QSpinBox()
        self.RField .setRange(0,255)
        self.RField.setPrefix("R  ")

        self.GField = QSpinBox()
        self.GField.setRange(0,255)
        self.GField.setPrefix("G  ")

        self.BField = QSpinBox()
        self.BField.setRange(0,255)
        self.BField.setPrefix("B  ")

        RGBWidget.layout().addWidget(self.RGBLabel)
        RGBWidget.layout().addWidget(self.RField)
        RGBWidget.layout().addWidget(self.GField)
        RGBWidget.layout().addWidget(self.BField)

        mainWidget.layout().addWidget(self.fieldCompression,0,0)
        mainWidget.layout().addWidget(self.fieldFPS,0,1)
        mainWidget.layout().addWidget(self.fieldImageInterval,1,0,1,2)
        mainWidget.layout().addWidget(RGBWidget,2,0,1,2)

        mainWidget.layout().addWidget(self.checkBoxAlpha,3,0)
        mainWidget.layout().addWidget(self.checkBoxForceSRGB,4,0)
        mainWidget.layout().addWidget(self.checkBoxInterlaced,3,1)
        mainWidget.layout().addWidget(self.checkBoxSaveSRGBProfile,4,1)

        mainWidget.layout().addWidget(self.buttonStartRecording,5,0,)
        mainWidget.layout().addWidget(self.buttonStopRecording,5,1)

        mainWidget.layout().addWidget(self.PathLabel,6,0)
        mainWidget.layout().addWidget(self.fieldPath,6,1)
        mainWidget.layout().addWidget(self.FFMPathLabel,7,0)
        mainWidget.layout().addWidget(self.fieldFFMPath,7,1)



    """
    _____________________________________________________________________________
    ---this approach does not work due to problems pickeling certain objects
    ---new approach: QThread using signals and slots

    ---maybe try using multiprocessing and passing raw pixel data through Pipe(),
       using pil to render might be a major performance improvement
       and/or solve the issue with Qtimer not exporting when brush is down
    _____________________________________________________________________________

        def startRecProcess(self):
            self.aD = Krita.instance().activeDocument()
            self.aD.setBatchmode(True)
            self.iO = krita.InfoObject()
            self.path = self.fieldPath.text()
            self.iO.setProperties({"alpha":True,"compression":5,"forceSRGB":False,"indexed":True,"interlaced":False,"saveSRGBProfile":False,"transparencyFillcolor":[255,255,255]})
            self.p = Process(target=self.rec, args=(self.timerOut_conn,self.aD,self.path,self.iO,10))
            self.p.start()
            self.timerIn_conn.send(1)


        def stopRec(self):
            self.timerIn_conn.send(0)

    """


    def startRec(self):
        self.buttonStopRecording.setEnabled(True)
        self.buttonStartRecording.setEnabled(False)
        self.setUiEnabled(False)
        self.iO = krita.InfoObject()
        self.iO.setProperties({
            "alpha":self.checkBoxAlpha.isChecked(),
            "compression":self.fieldCompression.value(),
            "forceSRGB":self.checkBoxForceSRGB.isChecked(),
            "indexed":True,"interlaced":self.checkBoxInterlaced.isChecked(),
            "saveSRGBProfile":self.checkBoxSaveSRGBProfile.isChecked(),
            "transparencyFillcolor":[self.RField.value(),self.GField.value(),self.BField.value()]
        })
        self.doc = Krita.instance().activeDocument()
        self.doc.setBatchmode(True)
        self.timer.start(self.fieldImageInterval.value()*1000)

    def stopRec(self):
        self.timer.stop()
        self.buttonStartRecording.setEnabled(True)
        self.buttonStopRecording.setEnabled(False)
        self.setUiEnabled(True)

    def setUiEnabled(x):
        self.fieldFPS.setEnabled(x)
        self.fieldPath.setEnabled(x)
        self.fieldFFMPath.setEnabled(x)
        self.fieldCompression.setEnabled(x)
        self.fieldImageInterval.setEnabled(x)
        self.BField.setEnabled(x)
        self.GField.setEnabled(x)
        self.RField.setEnabled(x)
        self.checkBoxAlpha.setEnabled(x)
        self.checkBoxForceSRGB.setEnabled(x)
        self.checkBoxInterlaced.setEnabled(x)
        self.checkBoxSaveSRGBProfile.setEnabled(x)

    def saveImage(self):
        counter = self.saveCounter
        if (self.doc.exportImage(self.fieldPath.text()+f"\\{counter}.png",self.iO)):
            self.saveCounter += 1



    def canvasChanged(self, canvas):
        pass



Krita.instance().addDockWidgetFactory(DockWidgetFactory("timeLapse", DockWidgetFactoryBase.DockRight, timeLapseDocker))
