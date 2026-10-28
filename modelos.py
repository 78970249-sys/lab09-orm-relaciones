from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base declarativa para todas las entidades ORM."""


class CategoriaModel(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    nombre: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )

    productos: Mapped[list["ProductoModel"]] = relationship(
        "ProductoModel", back_populates="categoria"
    )


class ProductoModel(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)

    categoria_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categorias.id"), nullable=False
    )

    categoria: Mapped["CategoriaModel"] = relationship(
        "CategoriaModel", back_populates="productos"
    )