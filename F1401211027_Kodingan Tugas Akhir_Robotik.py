# Diprogram oleh : Muhammad Nibroos Abrar - F1401211027
# Departemen Teknik Mesin dan Biosistem, FATETA-IPB University

import sys
import cv2
import numpy as np
import pathlib
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QCheckBox, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QGridLayout, QMessageBox, QAction
from PyQt5.uic import loadUi
from datetime import datetime
import csv
import os
import openpyxl
import pyautogui
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from numpy.lib.twodim_base import mask_indices
# from object_detector import *

class Robotik(QDialog):
    def __init__(self):
        super(Robotik, self).__init__()
        loadUi("./tampilanawal.ui", self)

        self.start.clicked.connect(self.gotodashboard) # Mengaktifkan button start untuk menuju halaman kedua
        self.setWindowTitle('ROBOTIK NIBROOS') #menampilkan judul pada window GUI

    # Menampilkan halaman kedua
    def gotodashboard(self):
        halamanutama = MainWindow()
        widget.addWidget(halamanutama)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./robotik.ui", self) #membaca ui dari qtdesigner
        self.buka.clicked.connect(self.uploadfoto) # Mengaktifkan button buka gambar
        self.keluar.clicked.connect(self.Keluar) # Mengaktifkan button keluar
        self.analisis.clicked.connect(self.Analys) # Mengaktifkan button analisis
        self.simpan.clicked.connect(self.Save) # Mengaktifkan button simpan
        self.mask_check.stateChanged.connect(self.Analys) #Mengaktifkan fungsi checkbox
        self.excel.clicked.connect(self.SaveToExcel) # Mengaktifkan fungsi tombol save to excel
        self.result_image = None #Menginisiasi kondisi awal Qlabel hasil ketika belum klik 'analisis'
        self.setWindowTitle('ROBOTIK NIBROOS') #memberi headline pada tampilan gui
        
        # Membuat workbook Excel
        self.workbook = openpyxl.load_workbook("./datamentahRobotik.xlsx")
        self.sheet = self.workbook.active
        self.row_counter = 1


        # Mengatur nilai minimum dan maksimum untuk slider dan spinbox
        self.hmax.setMinimum(0)
        self.hmax.setMaximum(255)
        self.smax.setMinimum(0)
        self.smax.setMaximum(255)
        self.vmax.setMinimum(0)
        self.vmax.setMaximum(255)
        self.hmin.setMinimum(0)
        self.hmin.setMaximum(255)
        self.smin.setMinimum(0)
        self.smin.setMaximum(255)
        self.vmin.setMinimum(0)
        self.vmin.setMaximum(255)
        
        # Mengaktifkan slider
        self.hmax.sliderMoved.connect(self.update_hmax_spin)
        self.smax.sliderMoved.connect(self.update_smax_spin)
        self.vmax.sliderMoved.connect(self.update_vmax_spin)
        self.hmin.sliderMoved.connect(self.update_hmin_spin)
        self.smin.sliderMoved.connect(self.update_smin_spin)
        self.vmin.sliderMoved.connect(self.update_vmin_spin)
        
        # mengaktifkan Spinbox
        self.hmax_spin.valueChanged.connect(self.update_hmax_slider)
        self.smax_spin.valueChanged.connect(self.update_smax_slider)
        self.vmax_spin.valueChanged.connect(self.update_vmax_slider)
        self.hmin_spin.valueChanged.connect(self.update_hmin_slider)
        self.smin_spin.valueChanged.connect(self.update_smin_slider)
        self.vmin_spin.valueChanged.connect(self.update_vmin_slider)
        
        # Inisialisasi nilai slider dan spinbox
        self.update_hmax_spin(self.hmax.sliderPosition())
        self.update_smax_spin(self.smax.sliderPosition())
        self.update_vmax_spin(self.vmax.sliderPosition())
        self.update_hmin_spin(self.hmin.sliderPosition())
        self.update_smin_spin(self.smin.sliderPosition())
        self.update_vmin_spin(self.vmin.sliderPosition())
        
        
    # Membatasi nilai miniumum dan maksimum spinbox serta menyelaraskannya dengan slider
    def update_hmax_spin(self, value):
        self.hmax_spin.setValue(value)
        self.hmax_spin.setMaximum(value)

    def update_smax_spin(self, value):
        self.smax_spin.setValue(value)
        self.smax_spin.setMaximum(value)

    def update_vmax_spin(self, value):
        self.vmax_spin.setValue(value)
        self.vmax_spin.setMaximum(value)

    def update_hmin_spin(self, value):
        self.hmin_spin.setValue(value)
        self.hmin_spin.setMinimum(value)

    def update_smin_spin(self, value):
        self.smin_spin.setValue(value)
        self.smin_spin.setMinimum(value)

    def update_vmin_spin(self, value):
        self.vmin_spin.setValue(value)
        self.vmin_spin.setMinimum(value)

    def update_hmax_slider(self, value):
        self.hmax.setValue(value)
        self.hmax_spin.setMaximum(value)

    def update_smax_slider(self, value):
        self.smax.setValue(value)
        self.smax_spin.setMaximum(value)

    def update_vmax_slider(self, value):
        self.vmax.setValue(value)
        self.vmax_spin.setMaximum(value)

    def update_hmin_slider(self, value):
        self.hmin.setValue(value)
        self.hmin_spin.setMinimum(value)

    def update_smin_slider(self, value):
        self.smin.setValue(value)
        self.smin_spin.setMinimum(value)

    def update_vmin_slider(self, value):
        self.vmin.setValue(value)
        self.vmin_spin.setMinimum(value)
        
   
    # Membuka File Foto
    def uploadfoto(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Pilih File Citra',  "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files ()", '')[0]
        self.img = cv2.imread(self.img_name, 1)
        
        #self.ImageInsertedCheck = self.asal.pixmap()
        Pathimg_name = pathlib.Path(self.img_name)
        self.PictureName = Pathimg_name.stem #Membaca nama file
        self.GroupName = self.img_name.split('/')[-2] # Membaca nama folder
        self.nama_file.setText(f'{self.GroupName}: {self.PictureName}') # Menampilkan nama folder dan nama file pada Qlabel
        #self.label_NamaFile.setText(f'{self.GroupName} {self.PictureName}')
        
         #self.img_shape = img.shape
        open_path = self.img_name.replace(".png", "_hasil_threshold.png").replace(".jpg", "_hasil_threshold.jpg").replace(".bmp", "_hasil_threshold.bmp") 
        cv2.imwrite(open_path, self.img) #mengatur agar file dapat dibuka sesuai dengan lokasi file yang dipilih
        pixmap_source = QPixmap(open_path)
        self.asal.setPixmap(pixmap_source) 
        self.asal.setScaledContents(True)  # Mengatur agar gambar ditampilkan sesuai dengan ukuran QLabel pada gui
        
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV) #mengonversi citra rgb menjadi hsv
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) #mengonversi citra rgb menjadi gray
        
        # menghubungkan slider terhadap hasil pengolahan citra
        self.hmax.sliderMoved.connect(self.Analys)
        self.smax.sliderMoved.connect(self.Analys)
        self.vmax.sliderMoved.connect(self.Analys)
        self.hmin.sliderMoved.connect(self.Analys)
        self.smin.sliderMoved.connect(self.Analys)
        self.vmin.sliderMoved.connect(self.Analys)
    
    # Proses Analisis  
    def Analys(self):
        hMin = sMin = vMin = hMax = sMax = vMax = 0
        #hMin = psMin = pvMin = phMax = psMax = pvMax = 0
        #img = cv2.imread('./Citra_Asal.jpg', 1)
        #output = img
       
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
        mask = cv2.inRange(self.hsv, lower, upper)
        
        # Apply morphological operations to improve the binary image
        kernel = np.ones((5,5), np.uint8)
        secondTresh = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        finalthresh = cv2.morphologyEx(secondTresh, cv2.MORPH_CLOSE, kernel)

        res = cv2.bitwise_and(self.img, self.img, mask=finalthresh)
        # res = cv2.dilate(mask,kernel,iterations = 1)
        # # Erosi mask dengan kernel berukuran 3x3
        # res = cv2.erode(mask,kernel,iterations = 1)
        # # Smoothing citra dengan Gaussian Blur
        # res = cv2.GaussianBlur(self.img,(5,5),0)
        # res = cv2.medianBlur(res, 5)
        
        # Menghitung masing-masing komponen nilai RGB
        self.count = cv2.countNonZero(finalthresh) # Menghitung warna piksel
        sum_color_per_row = np.sum(res, axis=0)
        sum_color = np.sum(sum_color_per_row, axis=0)
        totalColor = sum_color/self.count

        r,g,b = self.hitungRGB(totalColor)
        H,S,I = self.hitungHSV(r,g,b)
        tinggi_cm,lebar_cm,area,berat,V,keras = self.hitungDimensiCitra(g)
        
        #format angka desimal
        # R = round(r,2)
        # G = round(g,2)
        # B = round(b,2)
        R = (f'{r:.2f}')
        G = (f'{g:.2f}')
        B = (f'{b:.2f}')
        Hue = (f'{H:.2f} \u00b0')
        Sat = (f'{S:.2f} %') 
        Intensity = (f'{I:.2f} %')
        
        # Konversi nilai desimal red, green, blue ke rentang 0-255
        
        # red_val_int = convert_to_255(r)
        # green_val_int = convert_to_255(g)
        # blue_val_int = convert_to_255(b)

        # self.red_val.setText(str(red_val_int))
        # self.green_val.setText(str(green_val_int))
        # self.blue_val.setText(str(blue_val_int))

        self.red_val.setText(str(R))
        self.green_val.setText(str(G))
        self.blue_val.setText(str(B))

        self.pixel_val.setText(str(self.count))
        self.hue_val.setText(str(Hue))
        self.sat_val.setText(str(Sat))
        self.intens_val.setText(str(Intensity))
        self.mayor_val.setText(str(tinggi_cm))
        self.minor_val.setText(str(lebar_cm))
        self.luas_val.setText(str(area))
        self.massa_val.setText(str(berat))
        self.brix_val.setText(str(V))
        self.kekerasan_val.setText(str(keras))

        # Create HSV Image and threshold into a range.
        #output = cv2.bitwise_and(img,img, mask= mask)
        
        # Simpan hasil thresholding dan masking sementara agar dapat digunakan kembali ke fungsi lainnya
        self.result_image = finalthresh.copy()
        self.result_image_mask = res.copy()
        
        # Membuat fungsi threshold 
        save_path = self.img_name.replace(".png", "_hasil_threshold.png").replace(".jpg", "_hasil_threshold.jpg").replace(".bmp", "_hasil_threshold.bmp") # mengatur agar file hasil tidak menimpa file asal
        cv2.imwrite(save_path, finalthresh)
        pixmap_source = QPixmap(save_path) #./Citra Hasil/Threshold.jpg
        self.hasil.setPixmap(pixmap_source)
        self.hasil.setScaledContents(True)  # Mengatur agar gambar ditampilkan sesuai dengan ukuran QLabel
        if self.mask_check.isChecked(): #kondisi ketika checkbox masking dicentang
            mask_path = self.img_name.replace(".png", "_hasil_masking.png").replace(".jpg", "_hasil_masking.jpg").replace(".bmp", "_hasil_masking.bmp") # mengatur agar file hasil tidak menimpa file asal
            cv2.imwrite(mask_path, res)
            pixmap_mask = QPixmap(mask_path)
            self.hasil.setPixmap(pixmap_mask)
            self.hasil.setScaledContents(True)  # Mengatur agar gambar ditampilkan sesuai dengan ukuran QLabel
        else: #kondisi ketika checkbox masking tidak dicentang
            self.hasil.setPixmap(pixmap_source)
            self.hasil.setScaledContents(True)  # Mengatur agar gambar ditampilkan sesuai dengan ukuran QLabel
        
    
    def hitungRGB(self, totalColor):
        # Mengitung nilai RGB
        B = ((totalColor)[0])
        G = ((totalColor)[1])
        R = ((totalColor)[2])

        # Mengkonversi nilai RGB menjadi HSI
        self.r = R / (R + B + G)
        self.g = G / (R + B + G)
        self.b = B / (R + B + G)

        return self.r,self.g,self.b

    def hitungHSV(self,r,g,b):
        self.H = 0
        self.S = 0
        self.I = 0

        Max = max(r,g,b)
        Min = min(r,g,b)
        Delta = Max - Min
        if Max == 0:
            self.S = 0
        else:
            self.S = (Delta / Max) * 100
        self.I = Max * 100
        if Max == Min: 
            self.H = 0
        elif Max == r: 
            self.H = (60 * ((g - b) / Delta) + 360) % 360
        elif Max == g:
            self.H = (60 * ((b - r) / Delta) + 120) % 360
        elif Max == b:
            self.H = (60 * ((r - g) / Delta) + 240) % 360

        return self.H,self.S,self.I

        
    def hitungDimensiCitra(self,g):
        # Menghitung nilai pixel
        P=int(self.count)
        
        # img=cv2.imread("tes hasil.png")
        # # Load Object Detector
        # detector = HomogeneousBgDetector()
        # ...
        # contours = detector.detect_objects(img)

        # # Draw objects boundaries
        # for cnt in contours:
        #     # Get rect
        #     rect = cv2.minAreaRect(cnt)
        #     (x, y), (w, h), angle = rect
        #     diameter_mayor = (w*3)/((8088)**(1/2))
        #     diameter_minor = (h*3)/((8088)**(1/2))
        #     # Display rectangle
        #     box = cv2.boxPoints(rect)
        #     box = np.int0(box)
        
        # Hitung tinggi dan lebar buah dalam cm
        tinggi_cm = (0.00006*(P)) + 3.3663
        lebar_cm = (0.00005*(P)) + 3.2945
        # tinggi_cm = diameter_mayor
        # lebar_cm = diameter_minor
        # Menghitung luas dan berat
        area = (0.0011*P) + 4.8091
        berat = (0.0035*P) - 26.802
        #format angka desimal
        tinggi_cm =(f'{tinggi_cm:.2f} cm')
        lebar_cm =(f'{lebar_cm:.2f} cm')
        area =(f'{area:.2f} cm\u00b2')
        berat =(f'{berat:.2f} gram')
        
        # Segmentasi warna jeruk pada citra
        #matang
        # lower_red = np.array([0, 100, 100])
        # upper_red = np.array([30, 255, 255])
        lower_orange = np.array([11, 70, 41])
        upper_orange = np.array([105, 255, 255])
        mask1 = cv2.inRange(self.hsv, lower_orange, upper_orange)
        #mentah
        # lower_red = np.array([160, 100, 100])
        # upper_red = np.array([179, 255, 255])
        lower_green = np.array([0, 46, 17])
        upper_green = np.array([109, 255, 255])
        mask2 = cv2.inRange(self.hsv, lower_green, upper_green)
        
        mask = mask1 + mask2
        
        # Dilasi mask dengan kernel berukuran 3x3
        kernel = np.ones((3,3),np.uint8)
        dilation = cv2.dilate(mask,kernel,iterations = 1)
        # Erosi mask dengan kernel berukuran 3x3
        erosion = cv2.erode(mask,kernel,iterations = 1)
        # Smoothing citra dengan Gaussian Blur
        blur = cv2.GaussianBlur(self.img,(3,3),0)
        
        # Hitung nilai kemanisan pada citra
        B_val = self.b 
        V = 20.03*B_val + 5.8435
        V =(f'{V:.2f} % brix')

        # Menghitung kekerasan
        B_val = self.b
        keras = 6.6847 * B_val + 0.8555
        keras = (f'{keras:.2f} kgf')

        return tinggi_cm,lebar_cm,area,berat,V,keras
    
    '''def Save(self):
        cv2.imshow('image',output)
        cv2.imwrite('./Citra_Hasil.jpg', output)
        pixmap_source = QPixmap('./Citra_Hasil.jpg')
        self.hasil.setPixmap(pixmap_source)''' 
        
    
    # Membuat perintah untuk menyimpan gambar 
    def Save(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Simpan File', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if save_path:
            if self.mask_check.isChecked(): #mengatur agar hasil masking dapat disimpan apabila checkbox mask dicentang
                if self.result_image is not None:
                    cv2.imwrite(save_path, self.result_image_mask)
            else: #mengatur agar hanya hasil threshold yang dapat disimpan apabila checkbox mask tidak dicentang
                if self.result_image is not None:
                    #self.saveToCSV(self.PictureName,self.GroupName,self.r,self.g,self.b,self.H,self.S,self.I,self.count)
                    cv2.imwrite(save_path, self.result_image)
                
                #self.statusBar().showMessage(f"Gambar berhasil disimpan sebagai {save_path}")
            #else:
                #self.statusBar().showMessage("Error: Gambar tidak terbaca atau kosong")
    
    def SaveToExcel(self):
        if self.row_counter == 1:
            # Menambahkan header jika baris pertama kosong
            headers = ["Nama File", "Red", "Green", "Blue", "Pixel Count", "Hue", "Saturation", "Intensity", "Tinggi (cm)", "Lebar (cm)", "Luas (cm^2)", "Berat (gram)", "Brix (%)", "Kekerasan (kgf)"]
            self.sheet.append(headers)
            self.row_counter += 1 #beralih ke baris berikutnya setelah headers terisi

        data_row = [
            self.PictureName,
            f"{float(self.red_val.text()):.5f}",  # 15 angka di belakang koma untuk mempertahankan jumlah nilai desimal asli
            f"{float(self.green_val.text()):.5f}",
            f"{float(self.blue_val.text()):.5f}",
            self.pixel_val.text(),
            self.hue_val.text(),
            self.sat_val.text(),
            self.intens_val.text(),
            self.mayor_val.text(),
            self.minor_val.text(),
            self.luas_val.text(),
            self.massa_val.text(),
            self.brix_val.text(),
            self.kekerasan_val.text(),
        ]
        self.sheet.append(data_row)
        # menyimpan hasil analisis citra ke dalam file excel yang sudah tersedia
        self.workbook.save("./datamentahRobotik.xlsx")
        

    def Keluar(self):
        sys.exit(app.exec_())
        
# def convert_to_255(value):
#     if np.isnan(value):
#         # Nilai default jika value adalah NaN
#         return 0  # Misalnya, mengembalikan nilai 0
#     else:
#         return int(value * 255)
       
app=QApplication(sys.argv)
mainwindow=Robotik()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
# widget.setFixedWidth(1920)
# widget.setFixedHeight(980)
widget.setWindowTitle('Robotik Nibroos')
widget.setGeometry(0,0,1920,980)
widget.show()
sys.exit(app.exec_()) 