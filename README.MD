# Web Scraper do Google Maps

Este script Python utiliza o Selenium para extrair informações de empresas dos resultados de busca do Google Maps. Ele automatiza o processo de busca por empresas em um local específico, coletando URLs de listagens e, em seguida, visitando cada URL para extrair infos, como nome, número de telefone, site, endereço, avaliação e número de avaliações.

## Funcionalidades

*   Busca baseada em localização: Especifique um local e um termo de busca para encontrar empresas relevantes.
*   Coleta automática de URLs: O scroll e a paginação são tratados para coletar um conjunto abrangente de URLs.
*   Extração detalhada de dados: Extrai nome, telefone, site, endereço, avaliação e número de avaliações para cada listagem de empresa.
*   Saída em CSV: Salva os dados extraídos em um formato CSV claro e bem organizado.

## Instalação

1.  Instale as dependências necessárias:

    ```bash
    pip install pandas selenium
    ```

2.  Baixe o ChromeDriver

    *   Visite [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) e baixe o ChromeDriver compatível.
    *   Extraia o executável do ChromeDriver baixado e coloque-o em um diretório acessível ao seu path do sistema.

## Uso

1.  Atualize os caminhos dos arquivos:

    *   Substitua os caminhos de espaço reservado em `browser_exe_path` e `driver_exe_path` pelos locais reais do executável do seu navegador Chrome e do ChromeDriver:

    ```python
    browser_exe_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    driver_exe_path = r'C:\caminho\para\chromedriver.exe'  # Substitua pelo caminho real
    ```

2.  Defina os parâmetros de busca:

    *   Modifique a variável `search_term` (linha 168) para especificar o tipo de empresa e o local que você deseja extrair.

    *   Exemplo:

    ```python
    search_term = "restaurantes em São Paulo"
    ```

3.  Execute o script:

    *   Execute o script usando Python (`main.py`).

## Saída

O script gerará um arquivo CSV chamado `extracted_map_data.csv` contendo os dados extraídos em formato tabular.