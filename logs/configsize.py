import sys
import random
from datetime import datetime
import git
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QWidget, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu,
                           QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon

class MatrixRain(QWidget):
    def __init__(self):
        super().__init__()
        self.drops = []
        for _ in range(50):
            self.drops.append({
                'x': random.randint(0, 300),
                'y': random.randint(0, 600),
                'speed': random.randint(1, 3),
                'char': random.choice('01')
            })
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_drops)
        self.timer.start(50)
        
        self.setStyleSheet("background-color: #000000;")
        
    def update_drops(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] > self.height():
                drop['y'] = 0
                drop['x'] = random.randint(0, self.width())
                drop['char'] = random.choice('01')
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        font = QFont('Consolas', 14)
        painter.setFont(font)
        
        for drop in self.drops:
            color = QColor(0, 255, 70, random.randint(100, 255))
            painter.setPen(color)
            painter.drawText(drop['x'], drop['y'], drop['char'])

class ModernButton(QPushButton):
    def __init__(self, text, parent=None, active_color=None):
        super().__init__(text, parent)
        self.setMinimumSize(200, 40)
        self.setFont(QFont('Segoe UI', 10))
        self.setCursor(Qt.PointingHandCursor)
        
        default_style = """
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 5px;
            }
            QPushButton:hover {
                border-color: rgba(255,255,255,0.5);
            }
            QPushButton:pressed {
                border-color: rgba(255,255,255,0.7);
            }
            QPushButton:disabled {
                color: #666;
                border-color: rgba(255,255,255,0.1);
            }
        """
        
        if active_color:
            active_style = f"""
                QPushButton {{
                    background-color: {active_color};
                    color: #ffffff;
                    border: 1px solid rgba(255,255,255,0.5);
                }}
            """
            self.active_style = default_style + active_style
        else:
            self.active_style = default_style
        
        self.setStyleSheet(default_style)
        self.is_active = False
    
    def toggle_active(self):
        self.is_active = not self.is_active
        self.setStyleSheet(self.active_style if self.is_active else self.styleSheet())
        return self.is_active

class LogGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo_path = None
        self.auto_generate_timer = None
        self.countdown_timer = None
        self.log_count = 0
        self.remaining_time = 0
        self.icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'images', 'favicon', 'euoryan.png')
        self.initUI()
        self.setupTrayIcon()
        
    def initUI(self):
        self.setWindowTitle('Matrix Log Generator')
        self.setStyleSheet("background-color: #1a1a1a;")
        self.resize(1000, 600)
        
        app_icon = QIcon(self.icon_path)
        self.setWindowIcon(app_icon)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        self.matrix_panel = MatrixRain()
        main_layout.addWidget(self.matrix_panel, stretch=1)
        
        bottom_panel = QWidget()
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(20, 10, 20, 10)
        
        self.path_button = ModernButton("Selecionar Pasta")
        self.path_button.clicked.connect(self.select_log_directory)
        bottom_layout.addWidget(self.path_button)
        
        self.log_button = ModernButton("Gerar Log")
        self.log_button.clicked.connect(self.generate_log)
        self.log_button.setEnabled(False)
        bottom_layout.addWidget(self.log_button)
        
        self.auto_log_button = ModernButton("Iniciar Log Automático", active_color="#4CAF50")
        self.auto_log_button.clicked.connect(self.toggle_auto_generate)
        self.auto_log_button.setEnabled(False)
        bottom_layout.addWidget(self.auto_log_button)
        
        main_layout.addWidget(bottom_panel)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #00ff45; font-size: 12px;")
        main_layout.addWidget(self.status_label)
        
    def setupTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_path))
        
        tray_menu = QMenu()
        
        generate_action = tray_menu.addAction("Gerar Log")
        generate_action.triggered.connect(self.generate_log)
        
        tray_menu.addSeparator()
        
        show_action = tray_menu.addAction("Mostrar/Esconder")
        show_action.triggered.connect(self.toggleWindow)
        
        quit_action = tray_menu.addAction("Sair")
        quit_action.triggered.connect(app.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.trayIconActivated)
        
    def toggleWindow(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
    
    def trayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggleWindow()
            
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Matrix Log Generator",
            "Aplicativo minimizado para a bandeja do sistema",
            QIcon(self.icon_path),
            2000
        )
        
    def select_log_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, 
                                                     "Selecionar Diretório de Logs", 
                                                     "", 
                                                     options=options)
        if directory:
            self.repo_path = directory
            self.path_button.setText(f"Pasta: {os.path.basename(directory)}")
            self.log_button.setEnabled(True)
            self.auto_log_button.setEnabled(True)
            self.status_label.setText("Pasta selecionada com sucesso!")
    
    def generate_log(self, is_auto=False):
        if not self.repo_path:
            QMessageBox.warning(self, "Erro", "Selecione uma pasta primeiro!")
            return False
        
        try:
            logs_path = os.path.join(self.repo_path, 'logs')
            os.makedirs(logs_path, exist_ok=True)
            
            log_path = os.path.join(logs_path, 'login_log.txt')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(log_path, 'a') as f:
                f.write(f"Log registrado em: {timestamp}\n")
            
            try:
                repo = git.Repo(self.repo_path)
                repo.git.add('logs/login_log.txt')
                repo.index.commit(f"Log entry: {timestamp}")
                
                origin = repo.remote(name='origin')
                origin.push()
                
                if is_auto:
                    self.log_count += 1
                    sync_status = f"✓ Log gerado e sincronizado (Total: {self.log_count})"
                else:
                    sync_status = "✓ Log gerado e sincronizado"
                
                self.status_label.setText(sync_status)
                return True
            
            except Exception as git_error:
                print(f"Git error: {git_error}")
                self.status_label.setText(f"Erro Git: {git_error}")
                return False
        
        except Exception as e:
            print(f"Log generation error: {e}")
            self.status_label.setText(f"Erro: {e}")
            return False

    def toggle_auto_generate(self):
        is_active = self.auto_log_button.toggle_active()
        
        if is_active:
            # Set up 5-minute (300 seconds) timer
            self.remaining_time = 300
            
            # Auto generate log timer
            self.auto_generate_timer = QTimer()
            self.auto_generate_timer.timeout.connect(lambda: self.generate_log(is_auto=True))
            self.auto_generate_timer.start(300000)  # 5 minutes
            
            # Countdown timer to update status
            self.countdown_timer = QTimer()
            self.countdown_timer.timeout.connect(self.update_countdown)
            self.countdown_timer.start(1000)  # Update every second
            
            self.status_label.setText("Geração automática de logs iniciada")
        else:
            # Stop timers
            if self.auto_generate_timer:
                self.auto_generate_timer.stop()
            if self.countdown_timer:
                self.countdown_timer.stop()
            
            self.log_count = 0
            self.status_label.setText("Geração automática de logs parada")
    
    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes, seconds = divmod(self.remaining_time, 60)
            countdown_text = f"Próximo log em: {minutes:02d}:{seconds:02d}"
            
            # Append log count to status
            if self.log_count > 0:
                countdown_text += f" (Total: {self.log_count})"
            
            self.status_label.setText(countdown_text)
        else:
            # Reset countdown
            self.remaining_time = 300

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'assets', 'images', 'favicon', 'euoryan.png')))
    ex = LogGeneratorApp()
    ex.show()
    sys.exit(app.exec_())