from sqlalchemy import select

from modelos import CategoriaModel, EtiquetaModel, ProductoModel


def test_relacion_uno_a_muchos_categoria_productos(db_session):
    cat_tech = CategoriaModel(nombre="Tecnología")

    ProductoModel(nombre="Laptop", precio=2500.0, categoria=cat_tech)
    ProductoModel(nombre="Mouse", precio=50.0, categoria=cat_tech)

    db_session.add(cat_tech)
    db_session.commit()

    categoria_db = db_session.scalars(
        select(CategoriaModel).filter_by(nombre="Tecnología")
    ).first()

    assert categoria_db is not None
    assert len(categoria_db.productos) == 2


def test_relacion_muchos_a_muchos_producto_etiquetas(db_session):
    cat_hogar = CategoriaModel(nombre="Hogar")
    tag_oferta = EtiquetaModel(nombre="Oferta")
    tag_nuevo = EtiquetaModel(nombre="Nuevo")

    prod = ProductoModel(
        nombre="Cafetera",
        precio=150.0,
        categoria=cat_hogar,
        etiquetas=[tag_oferta, tag_nuevo],
    )

    db_session.add_all([cat_hogar, prod])
    db_session.commit()

    prod_db = db_session.scalars(
        select(ProductoModel).filter_by(nombre="Cafetera")
    ).first()

    assert prod_db is not None
    assert len(prod_db.etiquetas) == 2

    tag_db = db_session.scalars(
        select(EtiquetaModel).filter_by(nombre="Oferta")
    ).first()

    assert tag_db is not None
    assert tag_db.productos[0].nombre == "Cafetera"


def test_eliminar_categoria_elimina_sus_productos(db_session):
    cat_ropa = CategoriaModel(nombre="Ropa")
    ProductoModel(nombre="Casaca", precio=120.0, categoria=cat_ropa)

    db_session.add(cat_ropa)
    db_session.commit()

    db_session.delete(cat_ropa)
    db_session.commit()

    prod_db = db_session.scalars(
        select(ProductoModel).filter_by(nombre="Casaca")
    ).first()

    assert prod_db is None