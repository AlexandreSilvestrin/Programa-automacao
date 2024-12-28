from cx_Freeze import setup, Executable
import sys
import os

# Adiciona o caminho dos arquivos adicionais
base = "Win32GUI"

executables = [
    Executable("app.py", base=base, icon=r"resources\icons\XY.ico")
]

build_exe_options = {
    "packages": ["os", "pandas", "sys", "numpy", "requests", "unidecode", "json"],
    "include_files": ["resources/"]  # Inclui pastas necessárias
}

setup(
    name="XY-auto",
    version="1.6.2",
    description="Programa de automacao // 11961594515 // https://github.com/AlexandreSilvestrin",
    options={"build_exe": build_exe_options},
    executables=executables
)