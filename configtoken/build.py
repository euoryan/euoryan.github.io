import os
import PyInstaller.__main__
import sys
from PIL import Image
import tempfile

def convert_png_to_ico(png_path):
    """Converte PNG para ICO"""
    ico_path = os.path.join(tempfile.gettempdir(), 'temp_icon.ico')
    img = Image.open(png_path)
    # Converter para tamanhos padrão de ícone
    icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128)]
    img.save(ico_path, format='ICO', sizes=icon_sizes)
    return ico_path

# Definindo caminhos
app_path = r"C:\Users\Ryan\Documents\MEGA\Code\git codes\euoryan.github.io\logs\config\configsize.py"
png_icon_path = r"C:\Users\Ryan\Documents\MEGA\Code\git codes\euoryan.github.io\assets\images\favicon\euoryan.png"
work_path = os.path.dirname(app_path)

# Converter PNG para ICO
ico_path = convert_png_to_ico(png_icon_path)

# Configurando argumentos do PyInstaller
PyInstaller.__main__.run([
    app_path,
    '--name=configsize',
    '--onefile',
    f'--icon={ico_path}',
    '--noconsole',
    '--clean',
    '--add-data', f'{png_icon_path};assets/images/favicon',
    '--workpath', os.path.join(work_path, 'build'),
    '--distpath', os.path.join(work_path, 'dist'),
    '--specpath', work_path,
])