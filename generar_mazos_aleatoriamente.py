




                POR HACER

















"""
Modulo que genera mazos aleatoriamente con cartas seleccionadas
también aleatoriamente y los introduce en la base de datos
"""
from typing import List
import random
from app import db, create_app
from app.modelos import CartaEnMazo, Mazo, Carta, Usuario
from sqlalchemy import select


def insertar_cartas_en_mazo_aleatorio(ids_cartas_disponibles: List[int], id_mazo: int,
                                      n_cartas: int) -> None:
    """
    Funcion que inserta cartas aleatoriamente
    """
    # Seleccionamos un numero de cartas igual a n_cartas, sin repeticiones
    id_cartas_aleatorias = random.sample(ids_cartas_disponibles, n_cartas)
    for id_carta_aleatoria in id_cartas_aleatorias:
        en_banquillo = random.choice([True, False])
        numero_copias = random.randint(1, 4)
        # Incluyo las cartas aleatoriamente
        db.session.add(CartaEnMazo(id_carta=id_carta_aleatoria, id_mazo=id_mazo,
                                   numero_copias=numero_copias, banquillo=en_banquillo))
    db.session.commit()


def generar_mazo_aleatorio(id_creador: int, nombre_mazo: str, ids_cartas_disponibles: List[int]):
    mazo = Mazo(nombre=nombre_mazo, id_creador=id_creador)
    db.session.add(mazo)
    db.session.commit()
    # Despues del commit, si accedo al id lo cargo
    insertar_cartas_en_mazo_aleatorio(ids_cartas_disponibles, mazo.id, 40)


def seleccionar_usuarios_mazos_aleatorios(ids_cartas_disponibles: List[int], ids_usuarios_disponibles: List[int],
                                          n_mazos: int):
    usuarios_con_mazo = random.choices(ids_usuarios_disponibles, k=n_mazos)
    for i, id_usuario_aleatorio in enumerate(usuarios_con_mazo):
        generar_mazo_aleatorio(id_usuario_aleatorio, f"mazo_{i}",
                               ids_cartas_disponibles)


def crear_datos_aleatorios():
    # Creo una instancia de la aplicacion para inicializar la base de datos
    flask_app = create_app()

    # Para ejecutar codigo en el contexto de la aplicacion, debemos utilizar
    # esta sentencia
    with flask_app.app_context():

        # Selecciono los usuarios y las cartas disponibles
        usuarios = db.session.scalars(select(Usuario.id)).fetchall()
        cartas = db.session.scalars(select(Carta.id)).fetchall()
        seleccionar_usuarios_mazos_aleatorios(cartas, usuarios, 200)


if __name__ == "__main__":
    crear_datos_aleatorios()