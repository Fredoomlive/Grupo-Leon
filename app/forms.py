from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import date


class CitaForm(FlaskForm):
    nombre_cliente = StringField(
        'Nombre completo', validators=[DataRequired()])
    email_cliente = StringField('Correo electrónico', validators=[
                                DataRequired(), Email()])
    telefono_cliente = StringField(
        'Teléfono de contacto', validators=[DataRequired()])

    tipo_asunto = SelectField('Tipo de asunto', choices=[
        ('Penal', 'Penal'),
        ('Civil', 'Civil'),
        ('Laboral', 'Laboral'),
        ('Familiar', 'Familiar'),
        ('Empresarial', 'Empresarial')
    ], validators=[DataRequired()])

    abogado = SelectField('Selecciona un abogado', choices=[
        ('Dr. Juan Pérez', 'Dr. Juan Pérez'),
        ('Dra. Ana Gómez', 'Dra. Ana Gómez'),
        ('Dr. Luis Martínez', 'Dr. Luis Martínez'),
        ('Dra. María Torres', 'Dra. María Torres'),
        ('Dr. Ricardo Silva', 'Dr. Ricardo Silva')
    ], validators=[DataRequired()])

    fecha = DateField('Fecha de la cita', validators=[DataRequired()])
    asunto = TextAreaField('Motivo de la cita', validators=[DataRequired()])
    submit = SubmitField('Agendar Cita')

    def validate_fecha(self, field):
        if field.data <= date.today():
            raise ValidationError(
                'Debes agendar citas desde el día de mañana en adelante.')
