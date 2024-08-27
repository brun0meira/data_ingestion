# Documentação do Projeto de Ingestão de Dados

## 1. Introdução
Este projeto foi desenvolvido com o objetivo de criar um pipeline de ingestão de dados usando uma combinação de tecnologias como Docker, MinIO, ClickHouse e APIs públicas. A aplicação é responsável por coletar dados de uma API pública, processá-los, armazená-los em MinIO e, finalmente, inseri-los em um banco de dados ClickHouse para análise posterior. Este readme descreve o fluxo de trabalho do projeto, os conceitos aprendidos, as tecnologias utilizadas, os pré-requisitos, o código-fonte, o fluxo da aplicação e o procedimento para execução.

## 2. Conceitos Aprendidos
Durante o desenvolvimento, foram explorados e aplicados diversos conceitos importantes, como:
- **Ingestão de Dados**: O processo de coleta, processamento e armazenamento de dados para análise posterior.
- **Armazenamento de Objetos com MinIO**: Uso do MinIO como um serviço de armazenamento de objetos semelhante ao Amazon S3.
- **Processamento de Dados com Pandas**: Manipulação e transformação de dados utilizando a biblioteca Pandas.
- **Uso de Bancos de Dados Colunares**: Aplicação do ClickHouse para armazenamento e consulta eficiente de grandes volumes de dados.
- **API Pública**: Integração com APIs públicas para obter dados dinâmicos.
- **Dockerização de Aplicações**: Criação de ambientes isolados e consistentes para a execução da aplicação usando Docker.

## 3. Tecnologias Utilizadas
As tecnologias e ferramentas principais utilizadas neste projeto incluem:
- **Docker**: Plataforma de containers para criar, gerenciar e implantar ambientes de forma consistente.
- **MinIO**: Serviço de armazenamento de objetos, compatível com a API S3 da AWS.
- **ClickHouse**: Banco de dados orientado a colunas, ideal para consultas analíticas de alto desempenho.
- **Flask**: Framework web minimalista para Python, utilizado para criar a API que processa e armazena os dados.
- **Poetry**: Ferramenta para gerenciamento de dependências e ambientes virtuais em Python.
- **Pandas**: Biblioteca Python para análise de dados, utilizada para manipulação de DataFrames.

## 4. Pré-requisitos
Para rodar este projeto, é necessário ter os seguintes pré-requisitos configurados:

### Variáveis de Ambiente
Certifique-se de configurar as variáveis de ambiente corretamente, criando um arquivo `.env` na raiz do projeto com as seguintes definições:

O arquivo `.env` não deve ser publicado publicamente no GitHub. No entanto, como neste caso ele é uma dependência importante para a execução do projeto, e suas definições são apenas para testes em localhost com um objetivo exclusivamente acadêmico, compartilhar o arquivo `.env` publicamente não representa um risco significativo.

```env
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=bruno
CLICKHOUSE_PASS=bruno
```

### Python e Poetry
- **Python**: Versão 10 ou superior.
- **Poetry**: Ferramenta de gerenciamento de dependências. Instale o Poetry seguindo a [documentação oficial](https://python-poetry.org/docs/).

## 5. Descrição dos Códigos Desenvolvidos

### 5.1 Código Principal (`app.py`)
Este é o código principal da aplicação Flask. Ele define uma rota `/data` que coleta dados de uma API pública, processa-os, armazena-os em MinIO e insere-os no ClickHouse para análises futuras.

- **Rota `/data`**: Esta rota, quando acessada via POST, inicia o processo de coleta de dados da API Rick and Morty, processa os dados, salva-os em um arquivo Parquet no MinIO, faz o download deste arquivo, prepara os dados e os insere na tabela `working_data` do ClickHouse. Por fim, um `View` é criado para facilitar consultas futuras.

### 5.2 MinIO Client (`data_pipeline/minio_client.py`)
Este módulo é responsável pela integração com o MinIO para criar buckets, fazer upload e download de arquivos.

- **`create_bucket_if_not_exists`**: Cria um bucket no MinIO se ele não existir.
- **`upload_file`**: Faz o upload de um arquivo para um bucket específico.
- **`download_file`**: Faz o download de um arquivo de um bucket para um local especificado.

### 5.3 API Client (`data_pipeline/api.py`)
Este módulo lida com a comunicação com a API pública de Rick and Morty.

- **`get_all_characters`**: Faz uma requisição HTTP GET para a API e retorna todos os personagens. Em caso de erro, captura e exibe mensagens de erro específicas.

### 5.4 Processamento de Dados (`data_pipeline/data_processing.py`)
Este módulo é responsável por processar os dados coletados e prepará-los para inserção no banco de dados.

- **`process_data`**: Cria um DataFrame com os dados coletados e salva em um arquivo Parquet.
- **`prepare_dataframe_for_insert`**: Adiciona colunas adicionais ao DataFrame e o prepara para inserção no ClickHouse.

### 5.5 ClickHouse Client (`data_pipeline/clickhouse_client.py`)
Este módulo integra a aplicação com o banco de dados ClickHouse.

- **`get_client`**: Cria e retorna uma conexão com o ClickHouse.
- **`execute_sql_script`**: Executa um script SQL no ClickHouse.
- **`insert_dataframe`**: Insere um DataFrame em uma tabela no ClickHouse.

### 5.6 Makefile (`Makefile`)
O Makefile facilita a execução de comandos comuns, como subir containers Docker, instalar dependências e rodar a aplicação.

- **`up`**: Sobe os serviços definidos no `docker-compose.yml`.
- **`install`**: Instala as dependências do projeto utilizando Poetry.
- **`run`**: Executa o arquivo principal `app.py` utilizando Poetry.
- **`curl`**: Faz uma requisição POST para a API de ingestão de dados.
- **`test`**: Executa testes automatizados.
- **`down`**: Derruba os serviços Docker.

### 5.7 Docker Compose (`docker-compose.yml`)
Este arquivo define os serviços Docker para MinIO e ClickHouse.

- **MinIO**: Serviço de armazenamento de objetos.
- **ClickHouse**: Banco de dados colunar para análises de dados.

### 5.8 Configurações adicionais ClickHouse (`users.xml`)
Arquivo de configuração personalizado para usuários e perfis no ClickHouse.

O ideal é que o arquivo `users.xml` presente neste repositório não seja publicado publicamente no GitHub. Porém, neste caso específico, como foi apresentado como parte de um desafio de configuração adicional do Clickhouse, e o projeto é destinado a testes em localhost com um propósito puramente acadêmico, compartilhar esse arquivo publicamente não representa riscos significativos, especialmente porque, sem ele, não seria possível acessar as senhas do banco e os usuários definidos.

- **`bruno`**: Usuário configurado com permissões e quota padrão.
- **`max_memory_usage`**: Limite de uso de memória configurado para 10GB.

## 6. Fluxo da Aplicação

1. **Recepção de Dados**: A aplicação coleta dados de personagens da API Rick and Morty.
2. **Processamento Inicial**: Os dados são processados, transformados em um DataFrame, e salvos em um arquivo Parquet.
3. **Armazenamento Temporário**: O arquivo Parquet é enviado ao MinIO.
4. **Recuperação e Preparação**: O arquivo é baixado do MinIO, os dados são preparados para inserção e enriquecidos com metadados.
5. **Inserção no Banco de Dados**: O DataFrame preparado é inserido em uma tabela no ClickHouse.
6. **Criação de Views**: Uma `View` é criada no ClickHouse para facilitar a análise dos dados inseridos.

## 7. Testes Implementados

### 7.1 Testes de `api_test`
Os testes da `api_test` cobrem as funcionalidades relacionadas à integração com a API do Rick and Morty. A seguir, uma descrição dos testes implementados:

- **`test_get_all_characters_success`**: Testa a função `get_all_characters` simulando uma resposta bem-sucedida da API, verificando se a função retorna os dados corretamente.

- **`test_get_all_characters_http_error`**: Simula um erro HTTP (por exemplo, 404 Not Found) e verifica se a função `get_all_characters` lança a exceção correta.

- **`test_get_all_characters_connection_error`**: Simula um erro de conexão e verifica se a função `get_all_characters` lança a exceção `ConnectionError`.

- **`test_get_all_characters_timeout_error`**: Simula um erro de timeout e verifica se a função `get_all_characters` lança a exceção `Timeout`.

- **`test_get_all_characters_request_exception`**: Simula um erro de solicitação genérico e verifica se a função `get_all_characters` lança a exceção `RequestException`.

### 7.2 Testes de `clickhouse_client_test`
Os testes de `clickhouse_client_test` validam as operações de interação com o banco de dados ClickHouse. A seguir, uma descrição dos testes:

- **`test_get_client`**: Verifica se a função `get_client` retorna corretamente o cliente configurado.

- **`test_execute_sql_script`**: Testa a execução de um script SQL, simulando a leitura de um arquivo e verificando se o comando SQL é executado corretamente.

- **`test_insert_dataframe`**: Verifica se a função `insert_dataframe` insere corretamente um DataFrame no banco de dados.

- **`test_get_client_error`**: Simula um erro na conexão com o ClickHouse e verifica se a exceção correta é lançada.

- **`test_execute_sql_script_error`**: Simula um erro durante a execução de um script SQL e verifica se a exceção correta é lançada.

- **`test_insert_dataframe_error`**: Simula um erro durante a inserção de dados e verifica se a exceção correta é lançada.

### 7.3 Testes de `data_processing_test`
Os testes de `data_processing_test` garantem que as funções de processamento de dados funcionem conforme esperado. A seguir, uma descrição dos testes:

- **`test_process_data_success`**: Testa o processamento de dados e a geração do arquivo Parquet com sucesso, verificando se o nome do arquivo gerado está correto.

- **`test_process_data_error`**: Simula um erro durante o processamento de dados e verifica se a exceção correta é lançada.

- **`test_prepare_dataframe_for_insert_success`**: Verifica se a função `prepare_dataframe_for_insert` adiciona corretamente as colunas esperadas ao DataFrame.

### 7.4 Testes de `minio_client_test`
Os testes de `minio_client_test` verificam as operações de interação com o serviço MinIO. A seguir, uma descrição dos testes:

- **`test_create_bucket_if_not_exists_success`**: Verifica se o bucket é criado corretamente quando ele não existe.

- **`test_create_bucket_if_not_exists_already_exists`**: Verifica se a função não tenta recriar um bucket que já existe.

- **`test_create_bucket_if_not_exists_error`**: Simula um erro durante a criação do bucket e verifica se a exceção correta é lançada.

- **`test_upload_file_success`**: Testa o upload de um arquivo para o bucket do MinIO, verificando se a operação é realizada corretamente.

- **`test_upload_file_error`**: Simula um erro durante o upload de um arquivo e verifica se a exceção correta é lançada.

- **`test_download_file_success`**: Verifica se o download de um arquivo do bucket do MinIO é realizado corretamente.

- **`test_download_file_error`**: Simula um erro durante o download de um arquivo e verifica se a exceção correta é lançada.

## 8. Como Rodar a Aplicação
Para rodar a aplicação, siga os passos abaixo:

### 8.1 Clonar o Repositório
Clone o repositório do projeto em sua máquina local.

### 8.2 Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e adicione as variáveis de ambiente conforme descrito anteriormente.

### 8.3 Subir os Serviços Docker
Utilize o comando abaixo para subir os serviços MinIO e ClickHouse:
```bash
make up
```

### 8.4 Instalar Dependências
Instale as dependências do projeto utilizando o Poetry:
```bash
make install
```

### 8.5 Executar a Aplicação
Execute a aplicação Flask:
```bash
make run
```

### 8.6 Enviar Dados para a API
Envie uma requisição POST para a API de ingestão de dados:
```bash
make curl
```

### 8.7 Rodar os Testes

Execute os testes para garantir que tudo está funcionando corretamente:

```bash
make test
```

### 8.8 Derrubar os Serviços
Para encerrar os serviços Docker, utilize o comando:
```bash
make down
```

Com isso, a aplicação de ingestão de dados estará em pleno funcionamento, pronta para coletar, processar e armazenar dados de forma eficiente.

Obs: Para simplificar, você pode usar o comando abaixo sem parâmetros adicionais:

```bash
make
```

Esse comando irá iniciar os serviços Docker, instalar as dependências e executar a aplicação Flask. Se preferir, após isso você pode usar os comandos `make curl` e `make down` individualmente para realizar as ações separadamente.