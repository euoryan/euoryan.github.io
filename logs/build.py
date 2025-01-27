import os
import PyInstaller.__main__
import sys

# Definindo caminhos
app_path = r"C:\Users\Ryan W11\Documents\MEGA\Code\git codes\euoryan.github.io\logs\configsize.py"
icon_path = r"C:\Users\Ryan W11\Documents\MEGA\Code\git codes\euoryan.github.io\assets\images\favicon\euoryan.png"
work_path = os.path.dirname(app_path)

# Configurando argumentos do PyInstaller
PyInstaller.__main__.run([
    app_path,
    '--name=configsize',
    '--onefile',
    f'--icon={icon_path}',
    '--noconsole',
    '--clean',
    '--add-data', f'{icon_path};assets/images/favicon',
    '--workpath', os.path.join(work_path, 'build'),
    '--distpath', os.path.join(work_path, 'dist'),
    '--specpath', work_path,
])