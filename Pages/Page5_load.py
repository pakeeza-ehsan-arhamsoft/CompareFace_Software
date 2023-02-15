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

        # get the layout of self.images_grid_layout
        grid_layout = self.images_grid_layout.layout()

        images_list = os.listdir("Images Temp Folder")

        # get the number of layouts you want to add

        # loop through the layouts
        for i in range(len(images_list)):
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
            pixmap = QPixmap(f"Images Temp Folder/{images_list[i]}")
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
            container_widget.objectName = f"container_widget_{i}"

            # add the container widget to the images grid layout
            self.images_grid_layout.layout().addWidget(container_widget)

            # create three text labels
            text_label1 = QLabel("Text Label 1")
            text_label2 = QLabel("Text Label 2")
            text_label3 = QLabel("Text Label 3")

            # add the text labels to the vertical layout
            vertical_layout.addWidget(text_label1)
            vertical_layout.addWidget(text_label2)
            vertical_layout.addWidget(text_label3)

            # set the maximum size for the container widget
            container_widget.setMaximumSize(QSize(320, 400))

            # connect the clicked signal of the cross button to the hide_layout slot, passing in the container widget as a parameter
            cross_button.clicked.connect(self.hide_layout)

            # add the container widget to the grid layout
            grid_layout.addWidget(container_widget, i // 3, i % 3)

    @pyqtSlot()
    def hide_layout(self):
        # Get the sender object (the button that was clicked)
        button = self.sender()

        # Get the object name (the unique ID we assigned)
        button_parent = button.parent()

        # Remove the widget from the layout and delete it
        # print(self.images_grid_layout.layout().indexOf(button_parent))
        index = self.images_grid_layout.layout().indexOf(button_parent)
        print(index)
        self.images_grid_layout.layout().itemAt(index).widget().setParent(None)
        # self.images_grid_layout.layout().itemAt(index).widget().deleteLater()

        # Rearrange the remaining widgets in the layout
        count = self.images_grid_layout.layout().count()
        print(count)
        for i in range(count):
            widget = self.images_grid_layout.layout().itemAt(i).widget()
            row = i // 3
            column = i % 3
            self.images_grid_layout.layout().addWidget(widget, row, column)

        # Hide the layout
        # button_parent.hide()

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


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Start_Page5()
    ui.showMaximized()
    ui.show()
    sys.exit(app.exec_())
