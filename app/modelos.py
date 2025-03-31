from typing import List
import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from sqlalchemy import Numeric, Date


class Jugador(db.Model):
    """
    Jugadores de la NBA
    """

    id_jugador: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    nombre: Mapped[str] = mapped_column(String, nullable=False)
    nombre_equipo: Mapped[str] = mapped_column(String, nullable=True)
    posicion: Mapped[str] = mapped_column(String(20), nullable=False)
    altura: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False)
    peso: Mapped[float] = mapped_column(Numeric(4, 1), nullable=True)
    fecha_nacimiento: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    pais: Mapped[str] = mapped_column(String(30), nullable=False)
    url_imagen: Mapped[str] = mapped_column(String, nullable=False)

    historicos: Mapped[List["Historico"]] = relationship(back_populates="jugador")
    cartas: Mapped[List["Carta"]] = relationship(back_populates="jugador")
    cartas_liga: Mapped[List["CartaLiga"]] = relationship(back_populates="jugador")


class Partido(db.Model):

    id_partido: Mapped[int] = mapped_column(Integer, primary_key=True)

    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    equipo_local: Mapped[str] = mapped_column(String(30), nullable=False)
    equipo_visitante: Mapped[str] = mapped_column(String(30), nullable=False)
    gana_local: Mapped[bool] = mapped_column(Boolean, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    historicos: Mapped[List["Historico"]] = relationship(back_populates="partido")


class Historico(db.Model):
    """
    Historico de un Jugador
    """

    id_jugador: Mapped[int] = mapped_column(Integer, ForeignKey(Jugador.id_jugador), primary_key=True)
    id_partido: Mapped[int] = mapped_column(Integer, ForeignKey(Partido.id_partido), primary_key=True)

    tiempo_jugador: Mapped[int] = mapped_column(Integer, nullable=False)
    puntos_marcados: Mapped[int] = mapped_column(Integer, nullable=True)
    puntuacion: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)

    jugador: Mapped["Jugador"] = relationship(back_populates="historicos")
    partido: Mapped["Partido"] = relationship(back_populates="historicos")


class Usuario(db.Model, UserMixin):
    """
    Usuarios de la aplicacion
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    cumple: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    ultima_tirada: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    cartas_liga: Mapped[List["CartaLiga"]] = relationship(back_populates="usuario")
    participa_ligas: Mapped[List["ParticipaLiga"]] = relationship(back_populates="usuario")

    # Con property, especificamos que password se puede acceder como un atributo,
    # de la forma usuario.password. Es un getter encubierto
    @property
    def password(self):
        raise AttributeError('No se puede leer el atributo password')

    # Especificando `nombre_propiedad.setter`, definimos la función setter. Esta función
    # se invoca siempre que asignemos al atributo un nuevo valor. En este caso, cuando hagamos usuario.password
    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Carta(db.Model):
    id_jugador: Mapped[int] = mapped_column(Integer, ForeignKey(Jugador.id_jugador), primary_key=True)

    puntuacion: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False, default=0)
    rareza: Mapped[str] = mapped_column(String(15), nullable=False)

    jugador: Mapped["Jugador"] = relationship(back_populates="cartas")



class Liga(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    numero_participantes_maximo: Mapped[int] = mapped_column(Integer, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)

    participa_ligas: Mapped[List["ParticipaLiga"]] = relationship(back_populates="liga")
    cartas_liga: Mapped[List["CartaLiga"]] = relationship(back_populates="liga")

    @property
    def password(self):
        raise AttributeError('No se puede leer el atributo password de la liga')

    @password.setter
    def password(self, password: str) -> None:
        if password:
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = None

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return True
        return check_password_hash(self.password_hash, password)


class ParticipaLiga(db.Model):
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey(Usuario.id), primary_key=True)
    id_liga: Mapped[int] = mapped_column(Integer, ForeignKey(Liga.id), primary_key=True)

    puntuacion_acumulada: Mapped[float] = mapped_column(Numeric, nullable=False, default=0)

    usuario: Mapped["Usuario"] = relationship(back_populates="participa_ligas")
    liga: Mapped["Liga"] = relationship(back_populates="participa_ligas")


class CartaLiga(db.Model):
    id_liga: Mapped[int] = mapped_column(Integer, ForeignKey(Liga.id), primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey(Usuario.id), primary_key=True)
    id_jugador: Mapped[int] = mapped_column(Integer, ForeignKey(Jugador.id_jugador), primary_key=True)

    numero_copias: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    usuario: Mapped["Usuario"] = relationship(back_populates="cartas_liga")
    liga: Mapped["Liga"] = relationship(back_populates="cartas_liga")
    jugador: Mapped["Jugador"] = relationship(back_populates="cartas_liga")