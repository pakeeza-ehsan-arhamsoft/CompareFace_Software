from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import math
from PIL import Image
import pickle
import tempfile
# import cv2


class Start_Page2(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = uic.loadUi("UI_Designs/Page_2.ui", self)
        self.pg2_btn3 = self.findChild(QPushButton, "pushButton")
        self.pg2_btn2 = self.findChild(QPushButton, "pushButton_2")

        x = QRegExpValidator(QRegExp(r'^[\x20-\x7E]*$'))

        self.input_case_no = self.findChild(QLineEdit, "input_case_no")
        self.input_case_no.setValidator(x)
        self.input_ps = self.findChild(QLineEdit, "input_ps")
        self.input_exm_name = self.findChild(QLineEdit, "input_exm_name")
        self.input_exm_bp = self.findChild(QLineEdit, "input_exm_bp")
        self.input_remarks = self.findChild(QLineEdit, "input_remarks")

        # self.img_upload = False
        self.path_name = ''


        self.frame = self.findChild(QLabel, "frame")
        self.frame.mousePressEvent = self.upload_photo

    def show_popup(self, txt):
        msg = QMessageBox()
        msg.setWindowTitle("Error Message!")
        msg.setText(txt)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def send_data(self):
        flag = True
        frame_path = os.path.abspath('Group70.png')
        if self.input_case_no.text() == '':
            flag = False
            self.show_popup("Please enter case number!")
        if self.input_ps.text() == '':
            flag = False
            self.show_popup("Please enter PS!")
        if self.input_exm_name.text() == '':
            flag = False
            self.show_popup("Please enter Examiner's name!")
        if self.input_exm_bp.text() == '':
            flag = False
            self.show_popup("Please enter Examiner's BP number!")
        if self.input_remarks.text() == '':
            flag = False
            self.show_popup("Please enter Remarks!")
        if self.path_name == '':
            flag = False
            self.show_popup("Please upload an image!")
            # if self.frame.pixmap() is None or


        if flag:
            # Create a temporary folder if it doesn't exist
            temp_folder = 'temp'
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            # Create a file in the temporary folder to store the data
            data_file = os.path.join(temp_folder, 'temp_data.txt')
            with open(data_file, 'w') as file:
                file.write(f'{self.input_case_no.text()}\n')
                file.write(f'{self.input_ps.text()}\n')
                file.write(f'{self.input_exm_name.text()}\n')
                file.write(f'{self.input_exm_bp.text()}\n')
                file.write(f'{self.input_remarks.text()}\n')

            self.path_folder = os.path.abspath('temp')

            img = Image.open(self.path_name)
            img = img.convert('RGB')
            img.save(self.path_folder+"/image.jpeg")

        return flag

    def resize_image(self, img,im):
        savefile = img
        file_size = os.path.getsize(img)
        # Convert bytes to megabytes
        file_size_mb = file_size / 10**6
        if file_size_mb > 5:
            qlt = 100 - math.ceil(file_size_mb - 5)
            savefile = "compressed_img.jpeg"
            im.save(savefile, quality=qlt, optimize=True)
        return savefile

    def upload_photo(self, event):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
         'c:\\',"Image files (*.jpeg *.gif *.ico *.png *.bmp *.gif *.tif *.tiff)")



        if fname[0] != '':
            extn = fname[0].split('.')
            if extn[-1] == "gif":
                im = Image.open(fname[0])
                try:
                    im.seek(0)
                    fname = "gif_frame.png"
                    im.save(fname)
                    fname = self.resize_image(fname,im)
                    self.frame.setPixmap(QPixmap(fname))
                except Exception as e:
                    print(e)
                    self.show_popup("The gif is corrupt!")
            else:
                try:
                    im = Image.open(fname[0])
                    fname = self.resize_image(fname[0],im)
                    self.frame.setPixmap(QPixmap(fname))
                    self.path_name = fname
                    self.img_upload = True
                    # print(self.path_name)
                except:
                    self.show_popup("The image is corrupt!")


    def clear_text(self):
        self.input_case_no.clear()
        self.input_ps.clear()
        self.input_exm_name.clear()
        self.input_exm_bp.clear()
        self.input_remarks.clear()
        self.frame.clear()
        fname = os.path.abspath("images/Group 68.png")
        im = Image.open(fname)
        fname = self.resize_image(fname, im)
        self.frame.setPixmap(QPixmap(fname))




