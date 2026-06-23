# Consultoria - Portal da Transparência

## Pré-requisitos

- Python 3.11 ou superior
- Git
- Acesso à API do Portal da Transparência

---

## Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>
```

---

## Criar ambiente virtual

### Windows

```bash
python -m venv .venv
```

Ativar o ambiente:

```bash
.venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Instalar dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

---

## Configuração das variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto.

Exemplo:

```env
PORTAL_TRANSPARENCIA_API_KEY=SUA_CHAVE_AQUI
```

---

## Obter chave de acesso da API

A API do Portal da Transparência exige cadastro prévio.

1. Acesse:
   https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email

2. Preencha o formulário com:
   - Nome
   - E-mail
   - Instituição (opcional)
   - Finalidade de uso

3. Após o cadastro, a chave de acesso será enviada para o e-mail informado.

4. Copie a chave recebida e configure no arquivo `.env`:

```env
PORTAL_TRANSPARENCIA_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Executar o projeto

Com a `.venv` ativada:

```bash
python index.py
```

---

## Atualizar dependências

Caso novas bibliotecas sejam instaladas:

```bash
pip freeze > requirements.txt
```

---

## Estrutura recomendada

```text
.
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── index.py
└── .venv/
```

---

## Observações

- O arquivo `.env` não deve ser enviado ao Git.
- A pasta `.venv` não deve ser enviada ao Git.
- Adicione ambos ao `.gitignore`.

Exemplo:

```gitignore
.env
.venv/
.vscode/
__pycache__/
*.pyc
```