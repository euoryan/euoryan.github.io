import sys
import random
import string
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
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(200, 40)
        self.setFont(QFont('Segoe UI', 10))
        self.setCursor(Qt.PointingHandCursor)
        
        self.setStyleSheet("""
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
        """)

class TokenGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo_path = None
        self.remaining_time = 0
        self.can_generate = True
        self.icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'images', 'favicon', 'euoryan.png')
        self.initUI()
        self.setupTrayIcon()
        
    def initUI(self):
        self.setWindowTitle('Token Generator')
        self.setStyleSheet("background-color: #1a1a1a;")
        self.resize(800, 600)
        
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
        
        self.generate_button = ModernButton("Gerar Token")
        self.generate_button.clicked.connect(self.generate_token)
        self.generate_button.setEnabled(False)
        bottom_layout.addWidget(self.generate_button)
        
        main_layout.addWidget(bottom_panel)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #00ff45; font-size: 12px;")
        main_layout.addWidget(self.status_label)
        
    def setupTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_path))
        
        tray_menu = QMenu()
        
        generate_action = tray_menu.addAction("Gerar Token")
        generate_action.triggered.connect(self.generate_token)
        
        tray_menu.addSeparator()
        
        show_action = tray_menu.addAction("Mostrar/Esconder")
        show_action.triggered.connect(self.toggleWindow)
        
        quit_action = tray_menu.addAction("Sair")
        quit_action.triggered.connect(QApplication.quit)
        
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
            "Token Generator",
            "Aplicativo continua rodando em segundo plano",
            QIcon(self.icon_path),
            2000
        )
        
    def select_log_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, 
                                                   "Selecionar Diretório", 
                                                   "", 
                                                   options=options)
        if directory:
            self.repo_path = directory
            self.path_button.setText(f"Pasta: {os.path.basename(directory)}")
            self.generate_button.setEnabled(True)
            self.status_label.setText("Pasta selecionada com sucesso!")

    def generate_random_token(self, length=200):
        # Definindo os caracteres possíveis
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Garantindo pelo menos um de cada tipo
        token = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Preenchendo o resto do token
        all_chars = lowercase + uppercase + digits + special
        token.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Embaralhando o token final
        random.shuffle(token)
        return ''.join(token)

    def generate_token(self):
        if not self.can_generate:
            return
            
        if not self.repo_path:
            QMessageBox.warning(self, "Erro", "Selecione uma pasta primeiro!")
            return
        
        try:
            # Gerar token
            token = self.generate_random_token()
            
            # Criar arquivo
            logs_path = os.path.join(self.repo_path, 'logs')
            os.makedirs(logs_path, exist_ok=True)
            
            log_path = os.path.join(logs_path, 'token_log.txt')
            with open(log_path, 'a') as f:
                f.write(f"{token}\n")
            
            try:
                # Commit e push
                repo = git.Repo(self.repo_path)
                repo.git.add('logs/token_log.txt')
                repo.index.commit(f"New token generated")
                
                origin = repo.remote(name='origin')
                origin.push()
                
                self.status_label.setText("✓ Token gerado e sincronizado")
                self.start_cooldown()
                
            except Exception as git_error:
                print(f"Git error: {git_error}")
                self.status_label.setText(f"Erro Git: {git_error}")
            
        except Exception as e:
            print(f"Error: {e}")
            self.status_label.setText(f"Erro: {e}")

    def start_cooldown(self):
        self.can_generate = False
        self.generate_button.setEnabled(False)
        self.remaining_time = 60
        
        # Criar timer para atualizar o contador
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Atualiza a cada segundo
        
    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.status_label.setText(f"Próximo token em: {self.remaining_time} segundos")
        else:
            self.countdown_timer.stop()
            self.can_generate = True
            self.generate_button.setEnabled(True)
            self.status_label.setText("Pronto para gerar novo token")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'assets', 'images', 'favicon', 'euoryan.png')))
    ex = TokenGeneratorApp()
    ex.show()
    sys.exit(app.exec_())