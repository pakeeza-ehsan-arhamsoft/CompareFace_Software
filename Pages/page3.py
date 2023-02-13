import os
import math
import images
from os import listdir
from os.path import isfile, join
from PIL import Image
from PyQt5 import uic, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QPixmap, QImage


class Start_Page3(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        path = "/home/nouman/Desktop/Nouman Akram/qt5_design/CompareFace_Software/UI_Designs"
        self.window = uic.loadUi(f"{path}/Page_3.ui", self)
        x = QRegExpValidator(QRegExp(r"[ \x{0020} -  \x{007E}]"))

        self.frame = self.findChild(QtWidgets.QLabel, "image_label")

        self.single_photo_radio = self.findChild(
            QtWidgets.QRadioButton, "single_photo_radioButton"
        )
        self.multiple_photo_radio = self.findChild(
            QtWidgets.QRadioButton, "multiple_photo_radioButton"
        )
        self.entire_folder_radio = self.findChild(
            QtWidgets.QRadioButton, "entire_folder_radioButton"
        )
        self.old_case_photo_radio = self.findChild(
            QtWidgets.QRadioButton, "old_case_photo_radioButton"
        )

        self.stack_widget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")

        self.single_photo_radio.pressed.connect(self.show_single_image_label)
        self.multiple_photo_radio.pressed.connect(self.show_multiple_image_label)
        self.entire_folder_radio.pressed.connect(self.show_folder_label)
        self.old_case_photo_radio.pressed.connect(self.show_old_case_photo_label)

        self.upload_images_list = []

        ###################### Single Upload Widget ###################################

        self.upload_button.clicked.connect(self.single_upload_photo)
        self.upload_button = self.findChild(QtWidgets.QPushButton, "upload_button")

        ###################### Multiple Upload Widget ###################################

        self.images_scroll_area = self.findChild(
            QtWidgets.QScrollArea, "multiple_images_scroll_area"
        )

        self.target_photos_widget = self.findChild(
            QtWidgets.QWidget, "target_photos_widget"
        )

        self.multiple_photos_label = self.findChild(
            QtWidgets.QLabel, "multiple_photos_label"
        )

        self.upload_image_label = self.findChild(QtWidgets.QLabel, "upload_image_label")

        self.photos_upload_button = self.findChild(
            QtWidgets.QPushButton, "photos_upload_button"
        )

        self.photos_upload_button.clicked.connect(self.multiple_upload_photo)

        ###################### Upload Folder Widget ###################################

        self.folder_images_scroll_area = self.findChild(
            QtWidgets.QScrollArea, "folder_images_scroll_area"
        )

        self.target_folder_widget = self.findChild(
            QtWidgets.QWidget, "target_folder_widget"
        )

        self.folder_images_label = self.findChild(
            QtWidgets.QLabel, "folder_images_label"
        )

        self.upload_folder_logo_label = self.findChild(
            QtWidgets.QLabel, "upload_folder_logo_label"
        )

        self.folder_upload_button = self.findChild(
            QtWidgets.QPushButton, "folder_upload_button"
        )

        self.folder_upload_button.clicked.connect(self.folder_upload)

        ###################### Start Prob ###################################

        self.start_prob_button = self.findChild(
            QtWidgets.QPushButton, "start_prob_button"
        )

        self.start_prob_button.clicked.connect(self.save_images)

    def show_single_image_label(self):
        self.upload_button.show()
        fname = os.path.abspath("../images/Group70.png")
        im = Image.open(fname)
        fname = self.resize_image(fname, im)
        self.frame.setPixmap(QPixmap(fname))
        self.stack_widget.setCurrentIndex(0)

    def show_multiple_image_label(self):
        self.upload_images_list.clear()
        self.multiple_photos_label.clear()
        self.images_scroll_area.hide()
        self.target_photos_widget.show()
        self.upload_image_label.show()
        self.frame.clear()
        self.stack_widget.setCurrentIndex(1)

    def show_folder_label(self):
        self.upload_images_list.clear()
        self.folder_images_label.clear()
        self.target_folder_widget.show()
        self.upload_folder_logo_label.show()
        self.folder_images_scroll_area.hide()
        self.stack_widget.setCurrentIndex(2)

    def show_old_case_photo_label(self):
        self.stack_widget.setCurrentIndex(3)

    def show_popup(self, txt):
        msg = QMessageBox()
        msg.setWindowTitle("Error Message!")
        msg.setText(txt)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def send_data(self):
        flag = True
        if self.input_case_no.text() == "":
            flag = False
            self.show_popup("Please enter case number!")
        if self.input_ps.text() == "":
            flag = False
            self.show_popup("Please enter PS!")
        if self.input_exm_name.text() == "":
            flag = False
            self.show_popup("Please enter Examiner's name!")
        if self.input_exm_bp.text() == "":
            flag = False
            self.show_popup("Please enter Examiner's BP number!")
        if self.input_remarks.text() == "":
            flag = False
            self.show_popup("Please enter Remarks!")
        if flag:
            pass

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

    def single_upload_photo(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "Image files (*.jpeg *.gif *.ico *.png *.bmp *.gif *.tif *.tiff)",
        )

        if fname[0] != "":
            self.upload_button.hide()
            self.upload_images_list.clear()
            try:
                fname = self.images_resize_and_gif_handler(fname[0])
                self.frame.setPixmap(QPixmap(fname))
                self.upload_images_list.append(fname)
            except Exception as e:
                self.show_popup("The gif or image is corrupt!")

    def multiple_upload_photo(self):
        self.images_scroll_area.show()
        self.target_photos_widget.hide()
        self.upload_image_label.hide()
        self.upload_images_list.clear()

        fname = QFileDialog.getOpenFileNames(
            self,
            "Open files",
            "",
            "Image files (*.jpeg *.gif *.ico *.png *.bmp *.gif *.tif *.tiff)",
        )

        if not fname[0]:
            self.upload_images_list.clear()
            self.multiple_photos_label.clear()
            self.images_scroll_area.hide()
            self.target_photos_widget.show()
            self.upload_image_label.show()
            return None

        self.multiple_photos_label.setText(
            "\n".join([file.split("/")[-1] for file in fname[0]])
        )

        i = 0
        for images_path in fname[0]:
            image = QImage(images_path)
            if not image.isNull():
                i += 1
                resize_image_path = self.images_resize_and_gif_handler(
                    images_path, gif_index=i
                )
                self.upload_images_list.append(resize_image_path)

        if not self.upload_images_list:
            self.show_popup("The Images is corrupt!")

    def folder_upload(self):
        self.upload_images_list.clear()
        fname = QFileDialog.getExistingDirectory(self)
        if fname:
            images = self.get_images(fname)

            self.folder_images_label.clear()
            self.upload_images_list.clear()
            self.target_folder_widget.hide()
            self.upload_folder_logo_label.hide()
            self.folder_images_scroll_area.show()

            i = 0
            for images_path in images:
                image = QImage(images_path)

                if not image.isNull():
                    i += 1
                    resize_image_path = self.images_resize_and_gif_handler(
                        images_path, gif_index=i
                    )
                    self.upload_images_list.append(resize_image_path)

            self.folder_images_label.setText(
                "\n".join([image.split("/")[-1] for image in images])
            )

    def get_images(self, root_folder):
        images = []
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if (
                    file.endswith(".jpg")
                    or file.endswith(".jpeg")
                    or file.endswith(".png")
                    or file.endswith(".gif")
                    or file.endswith(".ico")
                    or file.endswith("bmp")
                    or file.endswith("tif")
                    or file.endswith("tiff")
                ):
                    images.append(join(root, file))

        return images

    def images_resize_and_gif_handler(self, image, gif_index=0):
        if image.endswith(".gif"):
            im = Image.open(image)
            im.seek(0)
            fname = f"gif_frame{gif_index}.png"
            im.save(fname)
            fname = self.resize_image(fname, im)
        else:
            im = Image.open(image)
            fname = self.resize_image(image, im)

        return fname

    def save_images(self):
        if self.upload_images_list:
            for image in self.upload_images_list:
                image_name = image.split("/")[-1]
                temp_folder = "FaceAI Media"
                if not os.path.exists(temp_folder):
                    os.makedirs(temp_folder)

                # Create a file in the temporary folder to store the data
                self.path_folder = os.path.abspath("FaceAI Media")

                img = Image.open(image)
                img = img.convert("RGB")
                img.save(self.path_folder + f"/{image_name}")
        else:
            self.show_popup("No valid supported image file is selected.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Start_Page3()
    ui.showMaximized()
    ui.show()
    sys.exit(app.exec_())
