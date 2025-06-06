import sys
import random
import string
import git
import os
import datetime
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QWidget, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu,
                           QFileDialog, QMessageBox, QSpinBox, QCheckBox, QFrame)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QIcon

class GitWorker(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self, repo_path, file_path, pull_first=True):
        super().__init__()
        self.repo_path = repo_path
        self.file_path = file_path
        self.pull_first = pull_first
        
    def run(self):
        try:
            repo = git.Repo(self.repo_path)
            
            if self.pull_first:
                try:
                    origin = repo.remote(name='origin')
                    origin.pull()
                    time.sleep(1)
                except:
                    pass
            
            repo.git.add(self.file_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            repo.index.commit(f"Token {timestamp}")
            
            origin = repo.remote(name='origin')
            origin.push()
            
            self.finished.emit(True, "Success")
        except Exception as e:
            self.finished.emit(False, str(e))

class TokenGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo_path = None
        self.batch_running = False
        self.current_token = 0
        self.total_tokens = 0
        self.wait_time = 15
        self.git_worker = None
        self.batch_timer = QTimer()
        self.batch_timer.setSingleShot(True)
        self.batch_timer.timeout.connect(self.process_next_token)
        self.initUI()
        self.setupTrayIcon()
        
    def initUI(self):
        self.setWindowTitle('euoryan // token gen')
        self.setFixedSize(480, 320)
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d2d, stop:1 #1e1e1e);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a4a4a, stop:1 #3a3a3a);
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 10px;
                min-height: 24px;
                max-height: 28px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a5a5a, stop:1 #4a4a4a);
                border-color: #777;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a3a, stop:1 #2a2a2a);
            }
            QPushButton:disabled {
                background: #2a2a2a;
                color: #666;
                border-color: #333;
            }
            QSpinBox {
                background: #2a2a2a;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
                font-size: 10px;
                min-height: 20px;
            }
            QSpinBox:focus {
                border-color: #0078d4;
            }
            QLabel {
                color: #ffffff;
                font-size: 10px;
            }
            QCheckBox {
                color: #ffffff;
                spacing: 6px;
                font-size: 10px;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #555;
                border-radius: 2px;
                background: #2a2a2a;
            }
            QCheckBox::indicator:checked {
                background: #0078d4;
                border-color: #0078d4;
            }
            QFrame {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 8px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)
        
        title_label = QLabel("euoryan // token gen")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0078d4; margin-bottom: 8px; font-size: 14px;")
        main_layout.addWidget(title_label)
        
        controls_frame = QFrame()
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(12)
        controls_layout.setContentsMargins(12, 12, 12, 12)
        
        self.path_button = QPushButton("📁 SELECIONAR REPOSITÓRIO")
        self.path_button.clicked.connect(self.select_directory)
        controls_layout.addWidget(self.path_button)
        
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(10)
        
        settings_layout.addWidget(QLabel("Tokens:"))
        self.token_count = QSpinBox()
        self.token_count.setRange(1, 10000)
        self.token_count.setValue(100)
        self.token_count.setFixedWidth(70)
        settings_layout.addWidget(self.token_count)
        
        settings_layout.addWidget(QLabel("Intervalo:"))
        self.wait_time_input = QSpinBox()
        self.wait_time_input.setRange(5, 300)
        self.wait_time_input.setValue(5)
        self.wait_time_input.setSuffix("s")
        self.wait_time_input.setFixedWidth(70)
        self.wait_time_input.valueChanged.connect(self.update_wait_time)
        settings_layout.addWidget(self.wait_time_input)
        
        settings_layout.addStretch()
        controls_layout.addLayout(settings_layout)
        
        self.pull_checkbox = QCheckBox("Pull antes do Push")
        self.pull_checkbox.setChecked(True)
        controls_layout.addWidget(self.pull_checkbox)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        self.start_button = QPushButton("INICIAR")
        self.start_button.clicked.connect(self.start_batch)
        self.start_button.setEnabled(False)
        buttons_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("PARAR")
        self.stop_button.clicked.connect(self.stop_batch)
        self.stop_button.setEnabled(False)
        buttons_layout.addWidget(self.stop_button)
        
        controls_layout.addLayout(buttons_layout)
        main_layout.addWidget(controls_frame)
        
        self.status_label = QLabel("Selecione um repositório para começar")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #00ff88; font-weight: 500; margin-top: 8px; font-size: 10px;")
        main_layout.addWidget(self.status_label)
        
        main_layout.addStretch()
        
    def update_wait_time(self, value):
        if value < 5:
            self.wait_time_input.setValue(5)
            self.wait_time = 5
        else:
            self.wait_time = value
        
    def setupTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        
        tray_menu = QMenu()
        
        self.tray_status = tray_menu.addAction("Status: Pronto")
        self.tray_status.setEnabled(False)
        tray_menu.addSeparator()
        
        show_action = tray_menu.addAction("Mostrar")
        show_action.triggered.connect(self.show)
        
        quit_action = tray_menu.addAction("Sair")
        quit_action.triggered.connect(self.close_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecionar Repositório Git")
        if directory and os.path.exists(os.path.join(directory, '.git')):
            self.repo_path = directory
            folder_name = os.path.basename(directory)
            if len(folder_name) > 20:
                folder_name = folder_name[:17] + "..."
            self.path_button.setText(f"📁 {folder_name}")
            self.start_button.setEnabled(True)
            self.status_label.setText("Repositório selecionado ✓")
        elif directory:
            QMessageBox.warning(self, "Erro", "Diretório selecionado não é um repositório Git!")
            
    def generate_token(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(200))
        
    def start_batch(self):
        if not self.repo_path:
            return
            
        self.batch_running = True
        self.current_token = 0
        self.total_tokens = self.token_count.value()
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.token_count.setEnabled(False)
        self.wait_time_input.setEnabled(False)
        self.path_button.setEnabled(False)
        
        self.process_next_token()
        
    def process_next_token(self):
        if not self.batch_running or self.current_token >= self.total_tokens:
            self.finish_batch()
            return
            
        try:
            token = self.generate_token()
            
            logs_path = os.path.join(self.repo_path, 'logs')
            os.makedirs(logs_path, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"token_{timestamp}.txt"
            filepath = os.path.join(logs_path, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"{token}\n")
            
            relative_path = os.path.join('logs', filename)
            
            self.git_worker = GitWorker(self.repo_path, relative_path, self.pull_checkbox.isChecked())
            self.git_worker.finished.connect(self.on_git_finished)
            self.git_worker.start()
            
        except Exception as e:
            self.status_label.setText(f"Erro: {str(e)}")
            self.finish_batch()
            
    def on_git_finished(self, success, message):
        if success:
            self.current_token += 1
            progress = f"Token {self.current_token}/{self.total_tokens}"
            self.status_label.setText(f"✓ {progress}")
            self.tray_status.setText(f"Status: {progress}")
            
            if self.batch_running and self.current_token < self.total_tokens:
                self.batch_timer.start(self.wait_time * 1000)
            else:
                self.finish_batch()
        else:
            self.status_label.setText(f"Erro Git: {message}")
            self.finish_batch()
            
    def stop_batch(self):
        self.batch_running = False
        self.batch_timer.stop()
        if self.git_worker and self.git_worker.isRunning():
            self.git_worker.terminate()
        self.finish_batch()
        
    def finish_batch(self):
        self.batch_running = False
        self.batch_timer.stop()
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.token_count.setEnabled(True)
        self.wait_time_input.setEnabled(True)
        self.path_button.setEnabled(True)
        
        if self.current_token > 0:
            self.status_label.setText(f"✓ Concluído! {self.current_token} tokens gerados")
        else:
            self.status_label.setText("Geração interrompida")
            
        self.tray_status.setText("Status: Pronto")
        
    def closeEvent(self, event):
        if self.batch_running:
            reply = QMessageBox.question(self, 'Confirmar', 
                'Geração em andamento. Minimizar para bandeja?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                event.ignore()
                self.hide()
            else:
                self.close_app()
        else:
            event.ignore()
            self.hide()
            
    def close_app(self):
        self.batch_running = False
        if self.git_worker and self.git_worker.isRunning():
            self.git_worker.terminate()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = TokenGeneratorApp()
    window.show()
    sys.exit(app.exec())