from NBA import create_app
from app.modelos import db, ParticipaLiga, CartaLiga, Carta, Partido, Historico
import datetime

app = create_app()

with app.app_context():
    def insertar_partido_y_estadisticas():
        print("Insertando nuevo partido y estadísticas de jugadores...")

        id_partido = int(input("ID del partido (único): "))
        fecha_str = input("Fecha del partido (YYYY-MM-DD): ")
        fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        local = input("Equipo local: ")
        visitante = input("Equipo visitante: ")
        gana_local_input = input("¿Ganó el equipo local? (s/n): ").strip().lower()
        gana_local = gana_local_input == "s"

        url = input("URL de highlights: ")

        nuevo_partido = Partido(
            id_partido=id_partido,
            fecha=fecha,
            equipo_local=local,
            equipo_visitante=visitante,
            gana_local=gana_local,
            url=url
        )
        db.session.add(nuevo_partido)

        print("\n Añadiendo jugadores al histórico...")
        while True:
            id_jugador = int(input("ID del jugador (o 0 para terminar): "))
            if id_jugador == 0:
                break
            tiempo_jugador = int(input("Minutos jugados: "))
            puntos_marcados = int(input("Puntos anotados: "))
            puntuacion = float(input("Puntuación global: "))

            registro = Historico(
                id_partido=id_partido,
                id_jugador=id_jugador,
                tiempo_jugador=tiempo_jugador,
                puntos_marcados=puntos_marcados,
                puntuacion=puntuacion
            )
            db.session.add(registro)

        db.session.commit()
        print(f"\n Partido {id_partido} y estadísticas insertadas correctamente.\n")

    def recomputar_puntos():
        print("Recomputando puntuaciones acumuladas...")
        participaciones = db.session.query(ParticipaLiga).all()

        for pl in participaciones:
            # Solo las crtas unicas
            ids_cartas = db.session.query(CartaLiga.id_jugador).filter_by(
                id_usuario=pl.id_usuario,
                id_liga=pl.id_liga
            ).distinct().all()

            ids = [id_j for (id_j,) in ids_cartas]

            puntuaciones = db.session.query(Carta.puntuacion).filter(Carta.id_jugador.in_(ids)).all()
            suma = sum(p[0] for p in puntuaciones)

            pl.puntuacion_acumulada += suma
            print(f"Usuario {pl.id_usuario} en liga {pl.id_liga}: + {suma} puntos → total: {pl.puntuacion_acumulada}")

        db.session.commit()
        print("Recómputo de puntuaciones completado.")


    print("===== PANEL DE ADMINISTRADOR =====")
    print("1 → Insertar partido + histórico")
    print("2 → Recomputar puntuaciones acumuladas")
    print("\n")
    opcion = input("Selecciona una opción (1 o 2): ").strip()

    if opcion == "1":
        insertar_partido_y_estadisticas()
    elif opcion == "2":
        recomputar_puntos()
    else:
        print("Opción inválida.")
