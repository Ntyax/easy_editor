from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QTableWidget, QListWidget, QListWidgetItem,
        QLineEdit, QFormLayout,
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel, QSpinBox, QTextEdit, QMessageBox, QFileDialog)

from PyQt5.QtGui import QPixmap

from PIL import Image, ImageFilter

import os

app = QApplication([])


win = QWidget()
win.resize(700, 500)
win.setWindowTitle("Easy Editor")

#віджети вікна
img_list = QListWidget()
note_title = QLineEdit()


open_folder_btn = QPushButton("Відкрити папку")


image_lb = QLabel("Картинка")

left_btn = QPushButton("Вліво")
right_btn = QPushButton("Вправо")
mirror_btn = QPushButton("Дзеркало")
sharpen_btn = QPushButton("Різкість")
black_btn = QPushButton("Ч/Б")


#напрямні лінії
main_line = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

row1 = QHBoxLayout()

row1.addWidget(left_btn)
row1.addWidget(right_btn)
row1.addWidget(mirror_btn)
row1.addWidget(sharpen_btn)
row1.addWidget(black_btn)


col1.addWidget(open_folder_btn)
col1.addWidget(img_list)

col2.addWidget(image_lb)

col2.addLayout(row1)


main_line.addLayout(col1, stretch=1)
main_line.addLayout(col2, stretch=2)

win.setLayout(main_line)

workdir = ""

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    workimage.dir = workdir

def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result



def openFolder():
    try:
        chooseWorkDir()
        filenames = os.listdir(workdir)
        extensions = [".jpg", ".gif", ".bmp", ".png", ".jpeg"]
        images = filter(filenames, extensions)

        img_list.clear()
        img_list.addItems(images)
    except:
        print("Папку не вибрано!")



class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        self.filename = filename
        full_name = os.path.join(self.dir, self.filename)
        self.image = Image.open(full_name)

    def showImage(self, path):
        image_lb.hide()
        pixmapimage = QPixmap(path)
        w, h = image_lb.width(), image_lb.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        image_lb.setPixmap(pixmapimage)
        image_lb.show()


    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path)):
            os.mkdir(path)

        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        full_path = os.path.join(self.dir, self.save_dir, self.filename)
        workimage.showImage(full_path)




def chooseImage():
    if img_list.currentRow() >= 0:
        name = img_list.currentItem().text()
        workimage.loadImage(name)
        full_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(full_path)


workimage = ImageProcessor()


open_folder_btn.clicked.connect(openFolder)
img_list.currentRowChanged.connect(chooseImage)

black_btn.clicked.connect(workimage.do_bw)

win.show()
app.exec_()