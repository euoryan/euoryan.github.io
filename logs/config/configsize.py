import sys
import random
import string
import git
import os
import datetime
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QWidget, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu,
                           QFileDialog, QMessageBox, QSpinBox, QCheckBox)
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
        self.batch_running = False
        self.tokens_to_generate = 0
        self.total_tokens = 0
        self.current_token = 0
        self.batch_timer = None
        self.wait_time = 45  # Tempo padrão de espera em segundos
        self.icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'images', 'favicon', 'euoryan.png')
        self.initUI()
        self.setupTrayIcon()
        
    def initUI(self):
        self.setWindowTitle('Token Generator')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QSpinBox {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 5px;
                padding: 5px;
                min-height: 30px;
            }
            QLabel {
                color: white;
            }
            QCheckBox {
                color: white;
            }
        """)
        self.resize(800, 600)
        
        app_icon = QIcon(self.icon_path)
        self.setWindowIcon(app_icon)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        self.matrix_panel = MatrixRain()
        main_layout.addWidget(self.matrix_panel, stretch=1)
        
        # Painel de controles
        controls_panel = QWidget()
        controls_layout = QVBoxLayout(controls_panel)
        
        # Layout para botões principais
        button_panel = QWidget()
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(20, 10, 20, 10)
        
        self.path_button = ModernButton("Selecionar Pasta")
        self.path_button.clicked.connect(self.select_log_directory)
        button_layout.addWidget(self.path_button)
        
        self.generate_button = ModernButton("Gerar Token")
        self.generate_button.clicked.connect(self.generate_token)
        self.generate_button.setEnabled(False)
        button_layout.addWidget(self.generate_button)
        
        controls_layout.addWidget(button_panel)
        
        # Layout para controles de lote
        batch_panel = QWidget()
        batch_layout = QHBoxLayout(batch_panel)
        batch_layout.setContentsMargins(20, 10, 20, 10)
        
        batch_label = QLabel("Quantidade de Tokens:")
        batch_layout.addWidget(batch_label)
        
        self.token_count_input = QSpinBox()
        self.token_count_input.setRange(1, 1000)
        self.token_count_input.setValue(10)
        self.token_count_input.setFixedWidth(100)
        batch_layout.addWidget(self.token_count_input)
        
        # Adiciona controle para tempo de espera
        wait_label = QLabel("Intervalo (seg):")
        batch_layout.addWidget(wait_label)
        
        self.wait_time_input = QSpinBox()
        self.wait_time_input.setRange(1, 3600)  # Ampliar o intervalo (1s até 1h)
        self.wait_time_input.setValue(self.wait_time)
        self.wait_time_input.setFixedWidth(80)
        self.wait_time_input.setKeyboardTracking(True)  # Permitir entrada pelo teclado
        self.wait_time_input.valueChanged.connect(self.update_wait_time)
        batch_layout.addWidget(self.wait_time_input)
        
        self.batch_button = ModernButton("Iniciar Geração")
        self.batch_button.clicked.connect(self.start_batch_generation)
        self.batch_button.setEnabled(False)
        batch_layout.addWidget(self.batch_button)
        
        self.cancel_button = ModernButton("Cancelar Geração")
        self.cancel_button.clicked.connect(self.cancel_batch_generation)
        self.cancel_button.setEnabled(False)
        batch_layout.addWidget(self.cancel_button)
        
        controls_layout.addWidget(batch_panel)
        
        # Adiciona opção de pull antes do push
        options_panel = QWidget()
        options_layout = QHBoxLayout(options_panel)
        options_layout.setContentsMargins(20, 0, 20, 10)
        
        self.pull_before_push_checkbox = QCheckBox("Pull antes do Push (recomendado)")
        self.pull_before_push_checkbox.setChecked(True)
        options_layout.addWidget(self.pull_before_push_checkbox)
        
        controls_layout.addWidget(options_panel)
        
        main_layout.addWidget(controls_panel)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #00ff45; font-size: 12px;")
        main_layout.addWidget(self.status_label)
        
    def update_wait_time(self, value):
        self.wait_time = value
        
    def setupTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_path))
        
        self.tray_menu = QMenu()
        
        self.tray_status = self.tray_menu.addAction("Status: Pronto")
        self.tray_status.setEnabled(False)
        
        self.tray_menu.addSeparator()
        
        self.tray_generate = self.tray_menu.addAction("Gerar Token")
        self.tray_generate.triggered.connect(self.generate_token)
        
        self.tray_cancel = self.tray_menu.addAction("Cancelar Geração")
        self.tray_cancel.triggered.connect(self.cancel_batch_generation)
        self.tray_cancel.setEnabled(False)
        
        self.tray_menu.addSeparator()
        
        show_action = self.tray_menu.addAction("Mostrar/Esconder")
        show_action.triggered.connect(self.toggleWindow)
        
        quit_action = self.tray_menu.addAction("Sair")
        quit_action.triggered.connect(self.confirm_quit)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.trayIconActivated)

    def cancel_batch_generation(self):
        if self.batch_running:
            self.batch_running = False
            if self.batch_timer:
                self.batch_timer.stop()
            self.enable_controls(True)
            self.cancel_button.setEnabled(False)
            self.tray_cancel.setEnabled(False)
            self.status_label.setText("Geração em lote cancelada")
            self.tray_status.setText("Status: Pronto")
            self.current_token = 0
            self.total_tokens = 0

    def enable_controls(self, enabled):
        self.generate_button.setEnabled(enabled)
        self.batch_button.setEnabled(enabled)
        self.token_count_input.setEnabled(enabled)
        self.wait_time_input.setEnabled(enabled)
        self.path_button.setEnabled(enabled)
        self.pull_before_push_checkbox.setEnabled(enabled)
        self.tray_generate.setEnabled(enabled)

    def confirm_quit(self):
        if self.batch_running:
            reply = QMessageBox.question(
                self, 'Confirmar Saída',
                'Existe uma geração em lote em andamento. Deseja realmente sair?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                QApplication.quit()
        else:
            QApplication.quit()
            
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
        if self.batch_running:
            reply = QMessageBox.question(
                self, 'Confirmar',
                'Existe uma geração em lote em andamento. Deseja minimizar para a bandeja?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                event.ignore()
                self.hide()
                self.tray_icon.showMessage(
                    "Token Generator",
                    "Aplicativo continua rodando em segundo plano",
                    QIcon(self.icon_path),
                    2000
                )
            else:
                event.accept()
        else:
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
            self.batch_button.setEnabled(True)
            self.status_label.setText("Pasta selecionada com sucesso!")

    def generate_random_token(self, length=200):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        token = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        all_chars = lowercase + uppercase + digits + special
        token.extend(random.choice(all_chars) for _ in range(length - 4))
        
        random.shuffle(token)
        return ''.join(token)

    def start_batch_generation(self):
        if not self.repo_path:
            QMessageBox.warning(self, "Erro", "Selecione uma pasta primeiro!")
            return
            
        if self.batch_running:
            QMessageBox.information(self, "Info", "Já existe uma geração em lote em andamento!")
            return
            
        self.batch_running = True
        self.total_tokens = self.token_count_input.value()
        self.current_token = 0
        self.enable_controls(False)
        self.cancel_button.setEnabled(True)
        self.tray_cancel.setEnabled(True)
        self.generate_token(is_batch=True)

    def generate_token(self, is_batch=False):
        if not is_batch and not self.can_generate:
            return
            
        if not self.repo_path:
            QMessageBox.warning(self, "Erro", "Selecione uma pasta primeiro!")
            return
        
        try:
            token = self.generate_random_token()
            
            # Criar pasta logs se não existir
            logs_path = os.path.join(self.repo_path, 'logs')
            os.makedirs(logs_path, exist_ok=True)
            
            # Gerar nome de arquivo único com timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            log_filename = f"token_{timestamp}.txt"
            log_path = os.path.join(logs_path, log_filename)
            
            # Salvar token em arquivo individual
            with open(log_path, 'w') as f:
                f.write(f"{token}\n")
            
            try:
                repo = git.Repo(self.repo_path)
                
                # Pull antes de fazer push se a opção estiver ativada
                if self.pull_before_push_checkbox.isChecked():
                    try:
                        origin = repo.remote(name='origin')
                        origin.pull()
                    except Exception as pull_error:
                        print(f"Pull error (não crítico): {pull_error}")
                        # Continua mesmo se o pull falhar
                
                # Adiciona, commita e faz push de um único arquivo
                relative_path = os.path.join('logs', log_filename)
                repo.git.add(relative_path)
                commit_msg = f"Add token {timestamp}"
                repo.index.commit(commit_msg)
                
                origin = repo.remote(name='origin')
                # Push com retry em caso de falha
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        origin.push()
                        break
                    except Exception as push_error:
                        if attempt < max_retries - 1:
                            time.sleep(2)  # Espera antes de tentar novamente
                        else:
                            raise push_error
                
                if is_batch:
                    self.current_token += 1
                    progress_msg = f"Token {self.current_token}/{self.total_tokens} gerado"
                    self.status_label.setText(progress_msg)
                    self.tray_status.setText(f"Status: {progress_msg}")
                    
                    if self.current_token < self.total_tokens and self.batch_running:
                        # Agendar próxima geração com o intervalo configurado
                        self.batch_timer = QTimer()
                        self.batch_timer.setSingleShot(True)
                        self.batch_timer.timeout.connect(lambda: self.generate_token(True))
                        self.batch_timer.start(self.wait_time * 1000)
                    else:
                        if self.batch_running:  # Se não foi cancelado
                            self.status_label.setText("✓ Geração em lote concluída!")
                            self.tray_status.setText("Status: Geração concluída")
                        self.batch_running = False
                        self.enable_controls(True)
                        self.cancel_button.setEnabled(False)
                        self.tray_cancel.setEnabled(False)
                else:
                    self.status_label.setText("✓ Token gerado e sincronizado")
                    self.start_cooldown()
                
            except Exception as git_error:
                print(f"Git error: {git_error}")
                self.status_label.setText(f"Erro Git: {git_error}")
                self.tray_status.setText(f"Status: Erro Git")
                if is_batch:
                    self.batch_running = False
                    self.enable_controls(True)
                    self.cancel_button.setEnabled(False)
                    self.tray_cancel.setEnabled(False)
            
        except Exception as e:
            print(f"Error: {e}")
            self.status_label.setText(f"Erro: {e}")
            self.tray_status.setText(f"Status: Erro")
            if is_batch:
                self.batch_running = False
                self.enable_controls(True)
                self.cancel_button.setEnabled(False)
                self.tray_cancel.setEnabled(False)

    def start_cooldown(self):
        self.can_generate = False
        self.generate_button.setEnabled(False)
        self.remaining_time = self.wait_time
        
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)
        
    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            countdown_msg = f"Próximo token em: {self.remaining_time} segundos"
            self.status_label.setText(countdown_msg)
            self.tray_status.setText(f"Status: {countdown_msg}")
        else:
            self.countdown_timer.stop()
            self.can_generate = True
            self.generate_button.setEnabled(True)
            self.status_label.setText("Pronto para gerar novo token")
            self.tray_status.setText("Status: Pronto")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'assets', 'images', 'favicon', 'euoryan.png')))
    ex = TokenGeneratorApp()
    ex.show()
    sys.exit(app.exec_())