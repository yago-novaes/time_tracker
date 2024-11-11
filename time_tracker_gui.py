# time_tracker_gui.py

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import QTimer
from time_tracker import TimeTracker 
import cmath

class TimeTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tracker = TimeTracker()
        self.initUI()
        self.check_existing_timer()

    def initUI(self):
        self.setWindowTitle('Time Tracker')
        self.setGeometry(100, 100, 600, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        ticket_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        ticket_label = QLabel('ID do Ticket:')
        self.ticket_entry = QLineEdit()

        ticket_layout.addWidget(ticket_label)
        ticket_layout.addWidget(self.ticket_entry)

        self.start_button = QPushButton('Iniciar Timer')
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton('Encerrar Timer')
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setEnabled(False)

        self.status_button = QPushButton('Status')
        self.status_button.clicked.connect(self.show_status)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.status_button)

        status_label = QLabel('Status:')
        self.status_area = QTextEdit()
        self.status_area.setReadOnly(True)

        main_layout.addLayout(ticket_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(status_label)
        main_layout.addWidget(self.status_area)

        self.central_widget.setLayout(main_layout)

    def start_timer(self):
        ticket = self.ticket_entry.text().strip()
        if not ticket:
            QMessageBox.warning(self, 'Entrada Inválida', 'Por favor, insira o ID do ticket.')
            return
        success, message = self.tracker.iniciar_timer(ticket)
        if success:
            self.log_status(message)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            QMessageBox.critical(self, 'Erro ao Iniciar Timer', message)

    def stop_timer(self):
        success, message = self.tracker.encerrar_timer()
        if success:
            self.log_status(message)
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
        else:
            QMessageBox.critical(self, 'Erro ao Encerrar Timer', message)

    def show_status(self):
        status = self.tracker.exibir_status()
        self.log_status(status)

    def log_status(self, message):
        self.status_area.append(message + "\n")

    def check_existing_timer(self):
        state_file = self.tracker.get_state_filename()
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                content = f.read().strip()
                if content:
                    try:
                        ticket, start_time = content.split(',')
                        ticket = ticket.strip()
                        message = f"Timer ativo para o ticket {ticket}."
                        self.log_status(message)
                        self.start_button.setEnabled(False)
                        self.stop_button.setEnabled(True)
                    except ValueError:
                        pass

def main():
    app = QApplication(sys.argv)
    window = TimeTrackerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
