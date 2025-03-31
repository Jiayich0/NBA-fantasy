"""
Modulo en el que definimos los formularios de nuestra aplicacion
"""
from typing import List
import datetime
from dateutil import relativedelta
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, ValidationError, NumberRange, Optional
from flask_wtf import FlaskForm


class SignupForm(FlaskForm):
    """Formulario para el registro de usuarios"""
    email = StringField(
        'Email',
        [
            Email(message='No es un email válido.'),
            DataRequired(message="Este campo es obligatorio.")
        ]
    )
    password = PasswordField(
        'Contraseña',
        [
            DataRequired(message="Introduzca una contraseña."),
            Length(8, message="La contraseña debe tener al menos 8 caracteres.")
        ]
    )
    confirmPassword = PasswordField(
        'Repite Contraseña',
        [
            DataRequired(message="Por favor, repite la contraseña."),
            EqualTo('password', message='Las contraseñas deben coincidir.')
        ]
    )
    cumple = DateField('Fecha de nacimiento', validators=[DataRequired("Introduce tu fecha de nacimiento.")])

    submit = SubmitField('Registrarse')

class SignInForm(FlaskForm):
    """Formulario para hacer login"""
    email = StringField(
        'Email',
        [
            Email(message='No es un email válido.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Contraseña',
        [
            DataRequired(message="Introduzca una contraseña."),
        ]
    )

    submit = SubmitField('Submit')

class UnirseLigaForm(FlaskForm):
    """Formulario para unirse a una liga privada"""
    password = PasswordField('Contraseña', validators=[DataRequired(message="Introduce la contraseña.")])

    submit = SubmitField('Unirse')

class CrearLigaForm(FlaskForm):
    """Formulario para crear una liga"""
    nombre = StringField('Nombre', validators=[DataRequired("Introduce un nombre.")])
    numero_participantes_maximo = IntegerField(
        'Número máximo de participantes',
        validators=[DataRequired("Este campo es obligatorio.")]
    )
    password = PasswordField('Contraseña (opcional)', validators=[Optional()])

    submit = SubmitField('Crear')