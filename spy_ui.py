from spyder_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from spider import *
import sys


class myForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myForm, self).__init__()
        self.setupUi(self)
        self.actionClose.triggered.connect(self.close)
        self.doButton.clicked.connect(lambda: self.do_click())

    def do_click(self):
        get_url = self.urlInput.text()
        get_path = self.filePathInput.text()
        get_max_page = self.maxPageInput.text()
        get_max_deep = self.maxDeepInput.text()
        print(get_max_deep)
        get_need = self.needCheck.checkState()
        x = WebSpider(get_url, get_max_page, get_max_deep, get_need, get_path)
        x.start()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = myForm()
    win.show()
    sys.exit(app.exec_())

