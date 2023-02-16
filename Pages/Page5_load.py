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
        self.examiner_no = self.findChild(QLabel, "Examiner_number")
        self.examiner_name = self.findChild(QLabel, "Examiner_name")
        self.remarks = self.findChild(QLabel, "remarks")
        self.time_generation = self.findChild(QLabel, "time_generation")
        self.probe_result = self.findChild(QLabel, "probe_result")
        self.probe_id = self.findChild(QLabel, "probe_id")
        self.sub_photo = self.findChild(QLabel, "label_8")

        self.filter_text = self.findChild(QLineEdit, "filter_text")
        self.filter_text.setMaxLength(2)
        validator = QRegExpValidator(QRegExp("^[1-9][0-9]?$|^100$"))
        self.filter_text.setValidator(validator)

        self.filter_button = self.findChild(QPushButton, "filter_button")

        self.filter_button.clicked.connect(self.filter_images)


    def show_popup(self, txt):
        msg = QMessageBox()
        msg.setWindowTitle("Error Message!")
        msg.setText(txt)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()


    def filter_images(self):
        # convert user input into integer
        if not self.filter_text.text():
            return

        filter_number = int(self.filter_text.text())

        # get total layouts
        total_layout = self.images_grid_layout.layout().count()

        # show the error if filter number is larger than total layouts
        if filter_number > total_layout:
            self.show_popup("Value must be less than the number of matched photos")
            return

        i = filter_number
        while i < total_layout:
            if self.images_grid_layout.layout().itemAt(i):
                widget = self.images_grid_layout.layout().itemAt(i).widget()
                self.images_grid_layout.layout().removeWidget(widget)
                image_path = widget.objectName().split(":")[-1]
                os.remove(image_path)
                i -= 1
            i+=1
        print(filter_number, total_layout)


    def layout_show(self):
        # get the layout of self.images_grid_layout
        grid_layout = self.images_grid_layout.layout()

        # loop through the layouts
        for i in range(len(self.images_list)):
            # create a container widget
            container_widget = QWidget(self.images_grid_layout)

            # create a vertical layout
            vertical_layout = QVBoxLayout(container_widget)
            vertical_layout.objectName = f"vertical_layout_{i}"

            # create a picture label
            picture_label = QLabel()

            # set the maximum size of the picture label
            picture_label.setMaximumSize(QSize(320, 400))

            # set the image of the picture label and scale it to fit the maximum size of the label
            pixmap = QPixmap(f"Images Temp Folder/{self.images_list[i]}")

            scaled_pixmap = pixmap.scaled(
                picture_label.maximumSize(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            picture_label.setPixmap(scaled_pixmap)

            # create a cross button
            cross_button = QPushButton()
            cross_button.setMaximumSize(QSize(20, 20))
            cross_button.objectName = f"cross_button_{i}"

            # add a cross picture to the button
            cross_button.setIcon(QIcon("images/close-button.png"))
            cross_button.setIconSize(QSize(20, 20))

            # make the button round
            cross_button.setStyleSheet("border-radius: 10px;")

            # set the cursor to pointing hand
            cross_button.setCursor(Qt.PointingHandCursor)

            # create a horizontal layout for the cross button and picture label
            horizontal_layout = QHBoxLayout()
            horizontal_layout.addWidget(picture_label)
            horizontal_layout.addWidget(cross_button, 0, Qt.AlignTop | Qt.AlignRight)

            # create a vertical layout for the picture label and cross button layout
            vertical_layout = QVBoxLayout()
            vertical_layout.addLayout(horizontal_layout)
            vertical_layout.setAlignment(Qt.AlignTop)

            # add the vertical layout to a container widget
            container_widget = QWidget()
            container_widget.setLayout(vertical_layout)
            # container_widget.objectName = f"container_widget_{i}"
            # add the path of the image to the object name of the container widget
            container_widget.setObjectName(
                f"container_widget_{i}:Images Temp Folder/{self.images_list[i]}"
            )

            # add the container widget to the images grid layout
            self.images_grid_layout.layout().addWidget(container_widget)

            # create three text labels
            text_label1 = QLabel("Similarity score: 94.73% (Highest match)")
            text_label2 = QLabel("Case no.:")
            text_label3 = QLabel("PS:")

            text_label1.setStyleSheet("color:white; text:bold")
            text_label2.setStyleSheet("color:white;")
            text_label3.setStyleSheet("color:white;")

            # add the text labels to the vertical layout
            vertical_layout.addWidget(text_label1)
            vertical_layout.addWidget(text_label2)
            vertical_layout.addWidget(text_label3)

            # set the maximum size for the container widget
            container_widget.setMaximumSize(QSize(320, 400))

            # connect the clicked signal of the cross button to the hide_layout slot, passing in the container widget as a parameter
            cross_button.clicked.connect(self.on_button_clicked)

            # add the container widget to the grid layout
            grid_layout.addWidget(container_widget, i // 3, i % 3)

    def get_images_list(self):
        self.images_list = []
        # if os.path.isdir("Images Temp Folder"):
        self.images_list = os.listdir("Images Temp Folder")
        self.layout_show()

    def on_button_clicked(self):
        button = self.sender()
        layout = button.parent()

        # get the object name of the parent of the button
        object_name = layout.objectName()

        # get the path of the image from the object name
        path = object_name.split(":")[1]

        count = self.images_grid_layout.layout().count()
        i = 0
        while i < count:
            if self.images_grid_layout.layout().itemAt(i):
                widget = self.images_grid_layout.layout().itemAt(i).widget()
                self.images_grid_layout.layout().removeWidget(widget)
                i -= 1
            i += 1

        os.remove(path)
        self.get_images_list()

        # layout.hide()

    def show_text(self):
        self.path_folder_pg5 = os.path.abspath("temp")

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

    def resize_image(self, img, im):
        savefile = img
        file_size = os.path.getsize(img)
        # Convert bytes to megabytes
        file_size_mb = file_size / 10**6
        if file_size_mb > 5:
            qlt = 100 - math.ceil(file_size_mb - 5)
            savefile = "compressed_img.jpeg"
            im.save(savefile, quality=qlt, optimize=True)
        return savefile


# if __name__ == "__main__":
#     import sys

#     app = QApplication(sys.argv)
#     ui = Start_Page5()
#     ui.showMaximized()
#     ui.show()
#     sys.exit(app.exec_())
