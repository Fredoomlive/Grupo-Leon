from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.forms import CitaForm, LoginForm
from app.models import db, Cita, Abogado
from datetime import date
from .forms import ClienteLoginForm
from app.models import Cliente


main = Blueprint('main', __name__)


@main.route('/')
def inicio():
    return render_template('inicio.html')


@main.route('/home')
def home():
    # Recuperamos el ID del cliente desde la sesión
    cliente_id = session.get('cliente_id')
    if cliente_id:
        # Obtenemos el cliente de la base de datos
        cliente = Cliente.query.get(cliente_id)
        if cliente:
            return render_template('home.html', nombre=cliente.nombre, apellido=cliente.apellido)
    # Si no hay cliente en sesión, redirigimos a login
    return redirect(url_for('main.cliente_login'))


@main.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if 'cliente_id' not in session:
        flash('Debe iniciar sesión como cliente para agendar una cita.', 'warning')
        return redirect(url_for('main.cliente_login'))

    form = CitaForm()

    # Cargar abogados dinámicamente desde la base de datos
    abogados = Abogado.query.all()
    form.abogado.choices = [(ab.id, ab.nombre) for ab in abogados]

    if form.validate_on_submit():
        if form.fecha.data <= date.today():
            flash('La fecha debe ser a partir de mañana.', 'danger')
            return render_template('agendar.html', form=form)

        nueva_cita = Cita(
            tipo_asunto=form.tipo_asunto.data,
            abogado_id=form.abogado.data,
            cliente_id=session.get('cliente_id'),
            fecha=form.fecha.data,
            asunto=form.asunto.data
        )
        db.session.add(nueva_cita)
        db.session.commit()

        return redirect(url_for('main.confirmacion', cita_id=nueva_cita.id))

    return render_template('agendar.html', form=form)


@main.route('/confirmacion/<int:cita_id>')
def confirmacion(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    return render_template('confirmacion.html', cita=cita)


@main.route('/historial')
def historial():
    if 'cliente_id' not in session:
        flash('Debe iniciar sesión para ver su historial de citas.')
        return redirect(url_for('main.cliente_login'))

    cliente_id = session['cliente_id']
    citas = Cita.query.filter_by(
        cliente_id=cliente_id).order_by(Cita.fecha.desc()).all()

    if not citas:
        return render_template('no_citas.html')

    return render_template('historial.html', citas=citas)


@main.route('/editar/<int:cita_id>', methods=['GET', 'POST'])
def editar_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    form = CitaForm(obj=cita)

    if form.validate_on_submit():
        form.populate_obj(cita)
        db.session.commit()
        flash('Cita actualizada exitosamente.', 'success')
        return redirect(url_for('main.historial'))

    return render_template('editar.html', form=form, cita=cita)


@main.route('/eliminar/<int:cita_id>', methods=['POST'])
def eliminar_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    db.session.delete(cita)
    db.session.commit()
    flash('Cita eliminada exitosamente.', 'success')
    return redirect(url_for('main.historial'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        abogado = Abogado.query.filter_by(email=form.email.data).first()
        if abogado and abogado.check_password(form.password.data):
            session['abogado_id'] = abogado.id
            session['abogado_nombre'] = abogado.nombre

            return redirect(url_for('main.panel_abogado'))
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html', form=form)


@main.route('/panel_abogado')
def panel_abogado():
    if 'abogado_id' not in session:
        flash('Debe iniciar sesión como abogado para acceder.')
        return redirect(url_for('main.abogado_login'))

    abogado_id = session['abogado_id']
    abogado = Abogado.query.get(abogado_id)

    citas = Cita.query.filter_by(
        abogado_id=abogado_id).order_by(Cita.fecha).all()

    return render_template('panel_abogado.html', abogado=abogado, citas=citas)


@main.route('/cliente/login', methods=['GET', 'POST'])
def cliente_login():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(email=form.email.data).first()
        if cliente and cliente.check_password(form.password.data):
            session['cliente_id'] = cliente.id
            flash('Cliente autenticado correctamente.')
            # Asegúrate de tener esta ruta
            return redirect(url_for('main.home'))
        else:
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('main.cliente_login'))

    return render_template('cliente_login.html', form=form)
