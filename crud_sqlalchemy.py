from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


def get_engine(url: str = "sqlite:///./crud_example.db"):
    """
    Cria um engine do SQLAlchemy.

    Por padrão usa um arquivo SQLite local (crud_example.db).
    Os testes podem passar um URL diferente (por exemplo, SQLite em memória).
    """
    return create_engine(url, future=True)


def get_session_factory(url: str = "sqlite:///./crud_example.db"):
    engine = get_engine(url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)


@dataclass
class ItemDTO:
    id: int
    name: str


def _to_dto(item: Item) -> ItemDTO:
    return ItemDTO(id=item.id, name=item.name)


# CREATE
def create_item(session: Session, name: str) -> ItemDTO:
    if not name or not name.strip():
        raise ValueError("name must not be empty")

    item = Item(name=name.strip())
    session.add(item)
    session.commit()
    session.refresh(item)
    return _to_dto(item)


# READ (get by id)
def get_item(session: Session, item_id: int) -> Optional[ItemDTO]:
    item = session.get(Item, item_id)
    return _to_dto(item) if item else None


# READ (list all)
def list_items(session: Session) -> List[ItemDTO]:
    items = session.query(Item).order_by(Item.id).all()
    return [_to_dto(i) for i in items]


# UPDATE - IMPLEMENTAÇÃO COM BUG PROPOSITAL
def update_item_buggy(session: Session, item_id: int, new_name: str) -> ItemDTO:
   
    if not new_name or not new_name.strip():
        raise ValueError("new_name must not be empty")

    # Verifica se o item existe
    item = session.get(Item, item_id)
    if not item:
        raise ValueError(f"item with id={item_id} not found")

 
    session.query(Item).update({"name": new_name.strip()})
    session.commit()

    # Recarrega o item "individual" (que agora tem o mesmo nome que todos)
    session.refresh(item)
    return _to_dto(item)

# DELETE
def delete_item(session: Session, item_id: int) -> None:
    item = session.get(Item, item_id)
    if not item:
        raise ValueError(f"item with id={item_id} not found")
    session.delete(item)
    session.commit()

__all__ = [
    "Base",
    "Item",
    "ItemDTO",
    "get_engine",
    "get_session_factory",
    "create_item",
    "get_item",
    "list_items",
    "update_item_buggy",
    "delete_item",
]

