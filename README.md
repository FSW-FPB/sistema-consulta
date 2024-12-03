
# API de consulta CIDs (Classificação Internacional de Doenças)

Esta API fornece endpoints para consulta e busca de códigos CID e suas respectivas descrições. Utiliza o framework Flask para criar endpoints HTTP que permitem a recuperação eficiente de informações sobre CIDs, com suporte a 2 (dois) modos de buscas: flexíveis e regulares.

## Tecnologias Utilizadas
- **Flask**: Framework web para criação da API.
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **thefuzz**: Biblioteca para comparação aproximada de 2 strings.
- **JSON**: Armazenamento dos dados CID.
- **Flask-CORS**: Gerenciamento de CORS para permitir requisições de diferentes origens.

## Configuração Inicial

1. Configure as variáveis de ambiente em um arquivo .env:
   ```
   JSON_FILE_PATH=./arquivo_cid.json
   PORT=5000 # Ou PORT=8000, ou outra porta de sua preferência
   ```

2. Instale as dependências do projeto:
	Opção 1 - Usando requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
   Opção 2 - Instalação direta:
	```bash
   pip install flask python-dotenv thefuzz
   ```
3. Execute o servidor Flask:
   ```bash
   python app.py
   ```

A API estará disponível em: `http://localhost:5000` ou `http://localhost:8000`

## Endpoints

### `GET /cid`
- **Descriçao**: Recupera todos os CIDs disponíveis no banco de dados
- **Resposta**: 
	-Lista de objetos JSON contendo códigos CID e suas descrições
	- Status: 200 OK

### `GET /cid/<code>`
- **Descrição**: Busca um CID específico pelo seu código
- **Parâmetros**: 
	- `code`: String representando o código CID
- **Resposta**:
  - Sucesso: JSON com o código e nome do CID
  - Erro: mensagem de erro se o código não for encontrado
  - Status: 200 OK ou 404 se não encontrado.

### `GET /cid/search/<search_term>`
- **Descrição**: Busca CIDs por nome/descrição baseado na similaridade da pesquisa. 
- **Parâmetros**:
  - `search_term`: Termo a ser pesquisado no nome/descrição do CID.
  - `search_mode`: (query parameter): Modo de busca "flexible" ou "regular" (default: "flexible")
- **Modos de busca**:
	- `flexible search`: Permite uma busca mais flexível, retornando resultados que incluam variações ou aproximações das palavras, mesmo que não estejam juntas ou na mesma ordem.
	- `regular search`: Realiza uma busca rigorosa por palavras-chaves, retornando resultados que contêm todas as palavras exatas da pesquisa juntas, como em "transtorno de ansiedade".
	**Nota**: O uso do modo flexible search é recomendado, utilize regular search apenas quando os resultados de busca flexível não forem bons o suficiente.
- **Resposta**:
  - Sucesso: Lista de CIDs que correspondem ao termo de busca
  - Erro: mensagem de erro se nenhum CID for encontrado
  - Status: 200 Ok, 400 se escolher query inválido ou 404 de não encontrado.

## Exemplo de Uso

### Recuperar todos os CIDs
```bash
 http://localhost:5000/cid
```

### Buscar CID por código
```bash
 http://localhost:5000/cid/1A00
```

### Buscar CID por nome (modo flexível)
```bash
http://localhost:5000/cid/search/diabetes?search_mode=flexible 
```
or
```bash
http://localhost:5000/cid/search/diabetes
```

### Buscar CID por nome (modo regular)
```bash
http://localhost:5000/cid/search/tuberculose?search_mode=regular
```

## Nota adicionais: 

- O modo de busca flexível utiliza um threshold (limite de filtro) por padrão de 80% para filtrar por buscas melhores, mas se precisar pode diminuir o threshold para um alcance de buscas maiores com o risco de falsos positivos.
- A busca por código é case-insensitive (não diferencia maiúsculas/minúsculas)
- O modo de busca regular permite encontrar termos exatos na ordem especificada.
---

# Changelog
## Atualizações Recentes

### Versão 1.1.0 (03/12/2024)
#### `GET /cid`
- **Descrição**: Nova funcionalidade implementada de paginação no endpoint para facilitar o consumo de grandes volumes de dados.
- **Parâmetros Novos (opcionais)**:
  - `page`: Define a página a ser recuperada (Default: "1")
  - `page_size`: Define o número de itens por página (Default: "500")
- **Nova resposta:**:
  - Agora os dados retornandos são segmentados de acordo com os parâmetros de paginação fornecidos.
  - A resposta será um subconjunto da lista completa de CIDs, determinado pelos índices calculados com base na página atual e no tamanho especificado em formato JSON.
- **Exemplo de paginação**:
### Recuperar todos os CIDs
```bash
# Primeira página (padrão)
 http://localhost:5000/cid

# Especificando página e tamanho
http://localhost:5000/cid?page=2&page_size=100
```

#### Problemas Resolvidos
- **CORS**: Resolvido o problema de restrição de CORS, garantindo compatibilidade com requisições de diferentes origens.

---

### Versão 1.0.0 (Lançamento Inicial)
- Criação dos endpoints:
  - `GET /cid`: Listar todos os CIDs.
  - `GET /cid/<code>`: Buscar CID por código.
  - `GET /cid/search/<search_term>`: Buscar CID por nome/descrição com modos de busca `flexible` e `regular`.

---

Este README cobre as principais funcionalidades e exemplos de uso para a API.
