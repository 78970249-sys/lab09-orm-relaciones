from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base declarativa para todas las entidades ORM."""


# Tabla asociativa para la relación N:M entre productos y etiquetas.
producto_etiqueta = Table(
    "producto_etiqueta",
    Base.metadata,
    Column(
        "producto_id",
        ForeignKey("productos.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "etiqueta_id",
        ForeignKey("etiquetas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class CategoriaModel(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    # Relación 1:N: una categoría tiene varios productos.
    # Al eliminar la categoría, se eliminan sus productos.
    productos: Mapped[list["ProductoModel"]] = relationship(
        "ProductoModel",
        back_populates="categoria",
        cascade="all, delete-orphan",
    )


class ProductoModel(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    precio: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    categoria_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categorias.id"),
        nullable=False,
    )

    # Cada producto pertenece a una categoría.
    categoria: Mapped["CategoriaModel"] = relationship(
        "CategoriaModel",
        back_populates="productos",
    )

    # Un producto puede tener varias etiquetas.
    etiquetas: Mapped[list["EtiquetaModel"]] = relationship(
        "EtiquetaModel",
        secondary=producto_etiqueta,
        back_populates="productos",
    )


class EtiquetaModel(Base):
    __tablename__ = "etiquetas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    nombre: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )

    # Una etiqueta puede estar asociada a varios productos.
    productos: Mapped[list["ProductoModel"]] = relationship(
        "ProductoModel",
        secondary=producto_etiqueta,
        back_populates="etiquetas",
    )