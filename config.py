import os
from dotenv import load_dotenv

load_dotenv(override=True)


class ConfiguracionFlask:
    """
    Clase con todas las variables de configuraciones de Flask
    """

    # Secret key: string largo para configurar la proteccion
    # de ciertos componentes de la app
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Ponemos track modifications de sqlalchemy a False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Hacemos que se muestren las consultas que se realizan
    SQLALCHEMY_ECHO = True

    # Si ponemos el flag DEBUG a true, Flask se ejecutará en modo 'debug'.
    # En este modo, se muestra el log de los errores que se produzcan.
    # NO USAR EN PRODUCCION
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.environ.get('USER')}:{os.environ.get('PASSWORD')}" \
                              f"@{os.environ.get('HOST')}/{os.environ.get('DATABASE')}"
