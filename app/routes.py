from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import CitaForm
from app.models import db, Cita
from datetime import date

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/agendar', methods=['GET', 'POST'])
def agendar():
    form = CitaForm()

    if form.validate_on_submit():
        # Validación: fecha debe ser después de hoy
        if form.fecha.data <= date.today():
            flash('La fecha debe ser a partir de mañana.', 'danger')
            return render_template('agendar.html', form=form)

        # Crear la nueva cita
        nueva_cita = Cita(
            nombre_cliente=form.nombre_cliente.data,
            email_cliente=form.email_cliente.data,
            telefono_cliente=form.telefono_cliente.data,
            tipo_asunto=form.tipo_asunto.data,
            abogado=form.abogado.data,
            fecha=form.fecha.data,
            asunto=form.asunto.data
        )
        db.session.add(nueva_cita)
        db.session.commit()

        # Redireccionar a pantalla de confirmación
        return redirect(url_for('main.confirmacion', cita_id=nueva_cita.id))

    return render_template('agendar.html', form=form)


@main.route('/confirmacion/<int:cita_id>')
def confirmacion(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    return render_template('confirmacion.html', cita=cita)


@main.route('/historial')
def historial():
    citas = Cita.query.all()
    if not citas:
        return render_template('no_citas.html')
    return render_template('historial.html', citas=citas)
