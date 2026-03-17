# CRUD simples com SQLAlchemy

Este projeto é um exemplo de CRUD em Python usando **SQLAlchemy** e testes com **pytest**.

## Estrutura

- `crud_sqlalchemy.py` – implementação do CRUD usando SQLAlchemy.
- `test_crud_sqlalchemy.py` – testes automatizados com pytest.
- `requirements.txt` – dependências do projeto.

## Como instalar

1. Crie e ative um ambiente virtual (opcional, mas recomendado).
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Como rodar os testes

Na pasta do projeto, execute:

```bash
pytest -v
```

## Como usar o CRUD no Python

Abaixo alguns exemplos básicos de uso em um script Python ou em um REPL (por exemplo, `python` ou `ipython`).

### Criando uma sessão

```python
from crud_sqlalchemy import get_session_factory

SessionLocal = get_session_factory()  # usa SQLite em arquivo local
session = SessionLocal()
```

### CREATE – criar um item

```python
from crud_sqlalchemy import create_item

item = create_item(session, "meu primeiro item")
print(item.id, item.name)
```

### READ – buscar um item por ID

```python
from crud_sqlalchemy import get_item

encontrado = get_item(session, item.id)
if encontrado is not None:
    print(encontrado.id, encontrado.name)
```

### READ – listar todos os itens

```python
from crud_sqlalchemy import list_items

itens = list_items(session)
for it in itens:
    print(it.id, it.name)
```

### UPDATE – atualizar o nome de um item

```python
from crud_sqlalchemy import update_item_buggy

atualizado = update_item_buggy(session, item.id, "novo nome")
print(atualizado.id, atualizado.name)
```

### DELETE – deletar um item

```python
from crud_sqlalchemy import delete_item, get_item

delete_item(session, item.id)
print(get_item(session, item.id))  # deve retornar None
```

