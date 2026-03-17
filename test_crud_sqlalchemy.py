import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from crud_sqlalchemy import (
    Base,
    Item,
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item_buggy,
)


@pytest.fixture()
def session() -> Session:
    """
    Cria um banco SQLite em memória para cada teste.
    """
    engine = create_engine(
        "sqlite://",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_and_get_item(session: Session):
    created = create_item(session, "primeiro")
    assert created.id == 1
    assert created.name == "primeiro"

    fetched = get_item(session, created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "primeiro"


def test_list_items(session: Session):
    create_item(session, "a")
    create_item(session, "b")
    create_item(session, "c")

    items = list_items(session)
    assert [i.name for i in items] == ["a", "b", "c"]


def test_delete_item(session: Session):
    created = create_item(session, "para deletar")
    assert get_item(session, created.id) is not None

    delete_item(session, created.id)
    assert get_item(session, created.id) is None


def test_update_item_buggy_updates_all_rows(session: Session):
    """
    Este teste mostra explicitamente o BUG no UPDATE.

    Esperado (correto em um CRUD): apenas o item com id=2 deveria
    ter o nome alterado para "novo-nome".

    Mas a implementação atual de update_item_buggy faz um update
    em massa e muda o nome de TODOS os registros.
    """
    i1 = create_item(session, "item-1")
    i2 = create_item(session, "item-2")
    i3 = create_item(session, "item-3")

    # Executa o UPDATE com bug
    updated = update_item_buggy(session, i2.id, "novo-nome")
    assert updated.id == i2.id

    # Verificações do estado do banco
    all_items = session.query(Item).order_by(Item.id).all()
    names = [i.name for i in all_items]

    # O que seria CORRETO:
    #   ["item-1", "novo-nome", "item-3"]
    #
    # Porém, devido ao bug, o teste EXPECTA que todos tenham sido alterados,
    # para evidenciar o comportamento incorreto.
    assert names == ["novo-nome", "novo-nome", "novo-nome"]

    # Se alguém corrigir o código de update para filtrar por id,
    # este teste vai quebrar e será necessário ajustar a asserção
    # para o comportamento correto do CRUD.

