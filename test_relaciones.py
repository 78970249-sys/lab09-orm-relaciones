from sqlalchemy import select

from modelos import CategoriaModel, ProductoModel


def test_relacion_uno_a_muchos_categoria_productos(db_session):
    cat_tech = CategoriaModel(nombre="Tecnología")

    ProductoModel(nombre="Laptop", precio=2500.0, categoria=cat_tech)
    ProductoModel(nombre="Mouse", precio=50.0, categoria=cat_tech)

    db_session.add(cat_tech)
    db_session.commit()

    stmt = select(CategoriaModel).filter_by(nombre="Tecnología")
    categoria_db = db_session.scalars(stmt).first()

    assert categoria_db is not None
    assert len(categoria_db.productos) == 2