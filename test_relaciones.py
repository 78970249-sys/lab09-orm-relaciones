# Línea de importación actualizada (parte superior del archivo)
from modelos import CategoriaModel, EtiquetaModel, ProductoModel
 
 
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
    assert len(prod_db.etiquetas) == 2
 
    tag_db = db_session.scalars(
        select(EtiquetaModel).filter_by(nombre="Oferta")
    ).first()
    assert tag_db.productos[0].nombre == "Cafetera"
