# Program untuk menentukan batas atas dan batas bawah untuk filterisasi HSV
# Diprogram oleh : Mohamad Solahudin
# Departemen Teknik Mesin dan Biosistem, FATETA-IPB University
# Silahkan digunakan untuk keperluan non-komersial
# Jika ada kesulitan hubungi : mohamadso@apps.ipb.ac.id

import sys
import cv2
import numpy as np
import pylab as pl
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from numpy.lib.twodim_base import mask_indices

class MainWindow(QDialog):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("C:/Users/Nibroos/OneDrive/Documents/ipb capekk/robotik/Sesi UAS/New folder/robotik.ui", self)
        
        self.buka.clicked.connect(self.uploadfoto)
        self.keluar.clicked.connect(self.Keluar)
        self.hmax.sliderMoved.connect(self.Cari)
        self.smax.sliderMoved.connect(self.Cari)
        self.vmax.sliderMoved.connect(self.Cari)
        self.hmin.sliderMoved.connect(self.Cari)
        self.smin.sliderMoved.connect(self.Cari)
        self.vmin.sliderMoved.connect(self.Cari)

    def uploadfoto(self):

        self.img_name = QFileDialog.getOpenFileName(self, 'Pilih File Citra', '')[0]
        img = cv2.imread(self.img_name, 1)
        self.img_shape = img.shape
        cv2.imwrite('./Citra_Asal.jpg', img)
        pixmap_source = QPixmap('./Citra_Asal.jpg')
        self.Gambar.setPixmap(pixmap_source) 
        
      
    def Cari(self):
        hMin = sMin = vMin = hMax = sMax = vMax = 0
        hMin = psMin = pvMin = phMax = psMax = pvMax = 0
        img = cv2.imread('./Citra_Asal.jpg', 1)
        output = img
       
        # get current positions of all trackbars
        hMin = float(self.hmin.sliderPosition())
        sMin = float(self.smin.sliderPosition())
        vMin = float(self.vmin.sliderPosition())
        hMax = float(self.hmax.sliderPosition())
        sMax = float(self.smax.sliderPosition())
        vMax = float(self.vmax.sliderPosition())
 

        #Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)
        
        cv2.imshow('image',output)
        cv2.imwrite('./Citra_Hasil.jpg', output)
        pixmap_source = QPixmap('./Citra_Hasil.jpg')
        self.Gambar.setPixmap(pixmap_source) 


    def Keluar(self):
        sys.exit(app.exec_())
        
app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1366)
widget.setFixedHeight(768)
widget.show()
sys.exit(app.exec_())