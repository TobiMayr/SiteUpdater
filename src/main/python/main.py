import requests
from PySide2.QtCore import QThreadPool
from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QGridLayout, QPushButton, QMessageBox

import sys

from worker import Worker


class SiteUpdater(QWidget):

    def __init__(self):
        super().__init__()
        self.start_button = QPushButton('Start')
        self.keywords_line = QLineEdit()
        self.url_line = QLineEdit()
        self.status_label = QLabel('nix')
        self.threadpool = QThreadPool()
        self.initUI()

    def initUI(self):
        self.start_button.clicked.connect(self.on_start_clicked)
        grid = QGridLayout()

        grid.addWidget(QLabel('Keywords:'), 0, 0)
        grid.addWidget(self.keywords_line, 0, 1)

        grid.addWidget(QLabel('URL:'), 1, 0)
        grid.addWidget(self.url_line, 1, 1)

        grid.addWidget(self.start_button, 2, 0)

        grid.addWidget(QLabel('Status:'), 3, 0)
        grid.addWidget(self.status_label, 3, 1)

        self.setLayout(grid)
        self.setMinimumWidth(500)
        self.setWindowTitle('Site Updater')

        self.show()

    def on_start_clicked(self):
        self.status_label.setText('Check Input')
        keywords_found = self.keywords_line.text()
        url = self.url_line.text()
        try:
            self.status_label.setText('Gehe auf Seite')
            request = requests.get(url=url)
        except Exception:
            self.status_label.setText('Kaputte URL du Hund')
            return
        source_code = request.text.lower()
        keywords_found = keywords_found.lower().strip()
        keywords_list = keywords_found.split(' ')
        if len(keywords_list) <= 0:
            self.status_label.setText('Keine Keywords du Bauer')
            return
        keywords_list = list(dict.fromkeys(keywords_list))
        keywords_dict = {}
        keyword_message = 'Aktuell gefunden:\n\n'
        for keyword in keywords_list:
            count = source_code.count(keyword)
            keywords_dict[keyword] = count
            keyword_message += f'{keyword}: \t{count} \n\n'
        keyword_message += 'Alert wenn sich die Anzahl ändert?'
        self.status_label.setText('Erfolgreich Seite abgerufen')

        message_box = QMessageBox.question(self, 'Solls los gehn?', keyword_message,
                                           QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if message_box == QMessageBox.Yes:
            self.status_label.setText('JETZT GEHTS LOS!!')
            worker = Worker(self.status_label, source_code, keywords_dict, url)
            self.threadpool.start(worker)
        else:
            self.status_label.setText('Heid ned')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = SiteUpdater()
    sys.exit(app.exec_())
