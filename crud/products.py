
from sqlalchemy.orm import Session


from storage.schemas import product as p

from storage.database import tables


def get_product_by_name(db: Session, name: str):
    return db.query(tables.Product).filter(tables.Product.name == name).first()


def get_prods(db: Session):
    return db.query(tables.Product).all()


def add_new_product(db: Session, product: p.Product):
    db_product = tables.Product(name=product.name, quan=product.quan)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product: p.Product, quan,add:bool):
    prod = product
    if add == True:

        prod.quan += quan
    else:
        prod.quan-=quan
    db.add(prod)
    db.commit()
    db.refresh(prod)

    return prod





