from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import date


class CitaForm(FlaskForm):

    tipo_asunto = SelectField('Tipo de asunto', choices=[
        ('Penal', 'Penal'),
        ('Civil', 'Civil'),
        ('Laboral', 'Laboral'),
        ('Familiar', 'Familiar'),
        ('Empresarial', 'Empresarial')
    ], validators=[DataRequired()])

    abogado = SelectField('Selecciona un abogado',
                          coerce=int, validators=[DataRequired()])
    fecha = DateField('Fecha de la cita', validators=[DataRequired()])
    asunto = TextAreaField('Motivo de la cita', validators=[DataRequired()])
    submit = SubmitField('Agendar Cita')

    def validate_fecha(self, field):
        if field.data <= date.today():
            raise ValidationError(
                'Debes agendar citas desde el día de mañana en adelante.')


class LoginForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')


class ClienteLoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[
                        DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')
