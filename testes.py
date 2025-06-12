from core.NOTAS import Notas

base_directory = r'C:/Users/Alexandre/Downloads/drive-download-20250610T175842Z-1-001/PLANSERVI'
saida = "C:/Users/Alexandre/Desktop/Nova pasta (2)"
mes = '05'
ano = '2025'

notas = Notas(base_directory,  saida, mes, ano)
notas.gerarNotas()