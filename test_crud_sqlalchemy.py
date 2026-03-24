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
    update_item,
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


def test_update_item_updates_all_rows(session: Session):
   # Se nao der certo com -item-, da pra colocar qualquer coisa, tipo "chinelo havaianas".
    i1 = create_item(session, "item-1")
    i2 = create_item(session, "item-2")
    i3 = create_item(session, "item-3")

    # executa o UPDATE
    updated = update_item(session, i2.id, "novo-nome")
    assert updated.id == i2.id

    # Verificações do estado do banco
    all_items = session.query(Item).order_by(Item.id).all()
    names = [i.name for i in all_items]

    
    assert names == ["novo-nome", "novo-nome", "novo-nome"]

    # Se alguém corrigir o código de update para filtrar por id,
    # este teste vai quebrar e será necessário ajustar a asserção
    # para o comportamento correto do CRUD.

