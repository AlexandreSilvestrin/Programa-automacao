# **XY-auto v1.6.5**

Este é um projeto desenvolvido para uma empresa de contabilidade para automação e manipulação de dados, com interface gráfica amigável e suporte a várias funcionalidades, como leitura e conversão de arquivos.

---

## **Estrutura do Projeto**

A organização do projeto foi reformulada para melhorar a modularidade e a manutenção:

```plaintext
PROGRAMA_MVC/
│
├── .venv/             # Ambiente virtual do Python
├── controllers/       # Controladores que gerenciam as interações entre interface e lógica
│   ├── abas_main/
│   │   ├── aba_notas_fat.py
│   │   ├── aba_prn.py
│   │   └── aba_razao.py
│   ├── config_controller.py
│   ├── main_controller.py
│   ├── sec_controller.py
│   └── ter_controller.py
├── core/              # As funções de manipulação de arquivos
│   ├── CNPJ_API.py
│   ├── FATURAMENTO.py
│   ├── NOTAS_entrada.py
│   ├── NOTAS_pdf.py
│   ├── NOTAS_tomados.py
│   ├── NOTAS.py
│   ├── PRN_T.py
│   └── RAZAO_resumo.py
├── models/            # Modelos de dados e manipulação de banco
│   ├── banco_cnpj.py
│   └── banco_fat.py
├── resources/         # Recursos estáticos e arquivos auxiliares
│   ├── config/        # Configurações do sistema
│   │   ├── caminhos.py
│   │   ├── config.txt
│   │   ├── janela1.json
│   │   ├── janela2.json
│   │   └── janela3.json
│   ├── data/          # Bases de dados e arquivos de suporte
│   │   ├── BANCOCNPJ.xlsx
│   │   └── GUIA_NOME.xlsx
│   ├── icons/         # Ícones do programa
│   │   └── XY.ico
│   ├── layouts/       # Arquivos de layout e UI gerados
│   │   ├── configW.py
│   │   ├── mainW.py
│   │   ├── secW.py
│   │   └── tercW.py
│   └── styles/        # Arquivos de estilo (CSS)
│       ├── dark.css
│       └── light.css
├── app.py                # Arquivo principal do programa
├── README.md             # Documentação do projeto
├── requirements.txt      # Dependências do projeto
└── setup.py              # Configuração para criar o executável
```

## **Principais Funcionalidades**

- **Conversão de arquivos**: Leitura de arquivos PDF e TXT, com exportação para Excel.
- **Criação de arquivos PRN**: Geração de arquivos PRN com regras específicas.
- **Consulta de CNPJs**: Integração com a API Receita WS.
- **Interface gráfica**: Interface intuitiva desenvolvida com PyQt5.

## **Tecnologias Utilizadas**

- **Python**  
- **Bibliotecas**: Pandas, PyQt5, Tabula-py ,Regex, PyPDF2, Requests, Openpyxl, CX_Freeze

---
<br>
<br>

# **Documentação Técnica do Projeto**


## **Estrutura do Projeto**
Abaixo está uma explicação sobre as principais pastas e arquivos:

### **Diretórios**
- **`controllers/`**: Contém os controladores responsáveis por gerenciar a lógica da interface gráfica (PyQt5).  
  - **`main_controller.py`**: Controlador da janela principal.  
  - **`sec_controller.py`**: Controlador da janela de CNPJ_notas.  
  - **`ter_controller.py`**: Controlador da janela CNPJ_fat. 
- **`core/`**: Implementa as funções principais do sistema, como leitura de arquivos, geração de PRNs e integração com APIs.  
  - **Exemplo**:  
    - `NOTAS_entrada.py`: Processa notas fiscais de entrada.  
    - `CNPJ_API.py`: Consulta dados de CNPJ via API Receita WS.  
- **`models/`**: Gerencia a manipulação de dados e conexões com bases como Excel ou arquivos de configuração.  
- **`resources/`**: Contém arquivos auxiliares como configurações, estilos (CSS), ícones e layouts da interface gráfica.  
- **`app.py`**: Arquivo principal que inicializa o programa.  

---

## **Instalação**

### **Requisitos**
- Python 3.10 ou superior.  
- Instale as dependências listadas em `requirements.txt` com o comando:  
  ```bash
  pip install -r requirements.txt
