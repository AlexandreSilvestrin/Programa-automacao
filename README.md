# XY-auto (Programa de Automação Contábil)

Um aplicativo desktop para contadores e escritórios contábeis que automatiza tarefas repetitivas de arquivos fiscais e relatórios. Ele tem interface gráfica e foi criado para facilitar a preparação de dados de notas fiscais, faturamento, geração de PRN e consulta de CNPJ.

## O que o programa faz

- Lê arquivos de notas fiscais e documentos fiscais em PDF/TXT
- Extrai e organiza dados para gerar relatórios em Excel
- Gera arquivos PRN no formato exigido por clientes e sistemas fiscais
- Consulta dados de CNPJ pela API (Receita WS)
- Exibe opções em uma interface gráfica simples e fácil de usar

## Como usar (rápido)

1. Abra `app.py` para iniciar o programa.
2. Use a janela principal para carregar o arquivo fiscal (PDF, TXT, etc.).
3. Selecione a operação desejada: gerar Excel, gerar PRN, consultar CNPJ.
4. O programa processa e salva os resultados em pastas de saída.

## Por que este projeto ajuda

- Reduz trabalho manual com planilhas e conversões
- Evita erros de digitação com processamento automático
- Torna mais rápido entregar arquivos prontos para clientes e obrigações fiscais

## Como rodar com UV

1. Instale o Python 3.12 (necessário para tabula).
2. Instale o UV globalmente no seu Python:
   ```powershell
   pip install uv
   ```
3. No diretório do projeto, inicialize o UV (vai criar `.venv` e instalar dependências):
   ```powershell
   uv sync
   ```
4. Ative o ambiente virtual criado:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
5. Execute o programa:
   ```powershell
   uv run app.py
   ```

> Se preferir, após `uv sync`, você também pode rodar diretamente com `python app.py` dentro do `.venv`.

