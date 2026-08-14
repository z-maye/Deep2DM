import shutil

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QComboBox, \
    QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import os
from detect import main

class Stats:

    state = False
    result = None
    model = None
    file_name = None
    goods = None
    model_dic = {'Boron Nitride': 'bn_mask_rcnn_tdm_120.h5', 'Graphene': 'graphene_mask_rcnn_tdm_0120.h5', 'Mos2': 'mos2_mask_rcnn_tdm_0120.h5', 'Wte2': 'wte2_mask_rcnn_tdm_0071.h5'}
    def __init__(self):
        # Load UI definition from file
        self.ui = uic.loadUi("./qt/Deep2DM.ui")
        self.ui.comboBox.currentIndexChanged.connect(self.choose_model)
        self.ui.Button_1.clicked.connect(self.choose_image)
        self.ui.Button_2.clicked.connect(self.opt)
        self.ui.Button_4.clicked.connect(self.save_image_locally)
        self.ui.Button_5.clicked.connect(self.out)
    def choose_model(self, index):
        selected_item = self.ui.comboBox.itemText(index)
        if selected_item == "Select Detection Material":
            self.model = None
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please select the item to be detected")
            msg.setWindowTitle("Prompt")
            msg.exec_()
        else:
            self.goods = selected_item
            self.model = self.model_dic[selected_item]

    def choose_image(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self.ui, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)",
                                                  options=options)
        if filePath:
            image = QImage(filePath)
            if not image.isNull():
                fileName = os.path.basename(filePath)
                savePath = os.path.join("./img/input", fileName)
                self.file_name = fileName
                image.save(savePath)
                pixmap = QPixmap(savePath)
                label_size = self.ui.label_1.size()
                pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio)
                label_1 = self.ui.label_1
                label_1.setScaledContents(True)
                self.ui.label_1.setPixmap(pixmap)
    def opt(self):
        if self.model == None or self.file_name == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please select the item or image to be detected")
            msg.setWindowTitle("Prompt")
            msg.exec_()
            self.state = False
        else:
            self.result = main(model_file=self.model, img_file=self.file_name)
            if self.result == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("No such material exists in the image, please try again")
                msg.setWindowTitle("Prompt")
                msg.exec_()
                self.state = False
                self.ui.label_5.setText(self.model)
                self.ui.label_11.setText(self.goods)
                self.ui.label_12.setText('0')
                self.ui.label_14.setText('0')
                self.ui.label_13.setText('0')
            else:
                outputpath = './img/output/' + self.file_name
                pixmap = QPixmap(outputpath)
                label_size = self.ui.label_2.size()
                pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio)
                label_2 = self.ui.label_2
                label_2.setScaledContents(True)
                self.ui.label_2.setPixmap(pixmap)
                self.ui.label_5.setText(self.model)
                self.ui.label_11.setText(self.goods)
                self.ui.label_12.setText(str(self.result["Mono"]))
                self.ui.label_14.setText(str(self.result['Few']))
                self.ui.label_13.setText(str(self.result['Thick']))
                self.state = True

    def save_image_locally(self):
        if self.state == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Failed to save the result image, please perform detection first")
            msg.setWindowTitle("Prompt")
            msg.exec_()
        else:
            options = QFileDialog.Options()
            folder_path = QFileDialog.getExistingDirectory(None, "Select Save Location", options=options)
            if folder_path:
                image_path = './img/output/' + self.file_name
                image_name = self.file_name
                destination_path = os.path.join(folder_path, image_name)
                shutil.copy(image_path, destination_path)

    def out(self):
        sys.exit()
if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()