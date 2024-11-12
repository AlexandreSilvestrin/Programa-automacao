from cx_Freeze import setup, Executable
import sys
import os

# Adiciona o caminho dos arquivos adicionais
base = "Win32GUI"

executables = [
    Executable("app.py", base=base, icon="icon/XY.ico")
]

build_exe_options = {
    "packages": ["os", "pandas", "sys", "numpy", "requests", "unidecode"],
    "include_files": ["interface/", "icon/","BANCOCNPJ.xlsx", "GUIA NOME.xlsx"]  # Inclui pastas necessárias
}

setup(
    name="XY-auto",
    version="1.5.8",
    description="Seu Aplicativo Python compilado.",
    options={"build_exe": build_exe_options},
    executables=executables
)