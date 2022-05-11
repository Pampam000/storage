from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
    Query
)



from sqlalchemy.orm import Session
from typing import List

from storage.crud import products, users

from storage.schemas import product as p
from storage.schemas import user as u
from storage.schemas import token as t

from storage.database.database import (
    engine,
    get_db
)
from storage.database import tables

tables.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/prod'
)


@router.post('/')
def add_product(
        name: str,
        product: p.Product,
        current_user: u.User = Depends(users.get_current_user),
        db: Session = Depends(get_db),
        quan: int = Query(..., ge=1)
):
    if not current_user.is_seller:
        raise HTTPException(status_code=403, detail='YOU ARE NOT ALLOWED TO ADD')
    product.name = name
    product.quan = quan
    db_product = products.get_product_by_name(db, name=name)

    if db_product:

        return products.update_product(
            db,
            db_product,
            quan,
            True
        )

    return products.add_new_product(db=db, product=product)


@router.get('/', response_model=List[p.Product])
def get_products(db: Session = Depends(get_db)):
    prods = products.get_prods(db)
    return prods


@router.put('/{name}')
def buy_product(
        name: str,
        quan: int = Query(..., ge=1),
        db: Session = Depends(get_db),
        current_user: u.User = Depends(users.get_current_user)
):
    if current_user.is_seller:
        raise HTTPException(status_code=403, detail='YOU ARE NOT ALLOWED TO BUY')
    prod = products.get_product_by_name(db, name)
    if not prod:
        raise HTTPException(status_code=404, detail="NO PRODUCT:(")
    if prod.quan < quan:
        raise HTTPException(status_code=405, detail=f"NOT AVAILABLE QUANTITY, TRY {prod.quan} OR LESS")

    prod = products.update_product(db, prod, quan,False)

    return prod
