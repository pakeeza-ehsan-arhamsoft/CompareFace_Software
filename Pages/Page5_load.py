from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import images
import os
import math
from PIL import Image
import random


class Start_Page5(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = uic.loadUi("UI_Designs/Page_5.ui", self)
        self.pg5_btn1 = self.findChild(QPushButton, "pushButton_5")
        self.pg5_btn2 = self.findChild(QPushButton, "pushButton_6")
        self.pg5_btn3 = self.findChild(QPushButton, "pushButton")

        self.case_no = self.findChild(QLabel, "case_number")
        self.examiner_no= self.findChild(QLabel, "Examiner_number")
        self.examiner_name = self.findChild(QLabel, "Examiner_name")
        self.remarks = self.findChild(QLabel, "remarks")
        self.time_generation = self.findChild(QLabel, "time_generation")
        self.probe_result = self.findChild(QLabel, "probe_result")
        self.probe_id = self.findChild(QLabel, "probe_id")
        self.sub_photo = self.findChild(QLabel, "label_8")


    def show_text(self):

        self.path_folder_pg5 = os.path.abspath('temp')


        with open(self.path_folder_pg5 + "/temp_data.txt", "r") as file:
            data = file.readlines()
            self.case_no.setText(data[0].strip())
            self.examiner_no.setText(data[3].strip())
            self.examiner_name.setText(data[2].strip())
            self.remarks.setText(data[4].strip())

        # Generate a random 9-digit number
        probe_id = str(random.randint(100000000, 999999999))
        self.probe_id.setText(probe_id)

         # Get the current date and time
        current_datetime = QDateTime.currentDateTime()

        # Format the date and time to the desired format
        time_generation = current_datetime.toString("dd/MM/yyyy hh:mm AP")

        # Set the formatted date and time as the text for the label
        self.time_generation.setText(time_generation)


        path = self.path_folder_pg5 + "/image.jpeg"
        im = Image.open(path)
        path = self.resize_image(path, im)
        self.sub_photo.setPixmap(QPixmap(path))


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
