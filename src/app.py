from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, send_file
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from weasyprint import HTML
from io import BytesIO
import pandas as pd

from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelGranja import ModelGranja
from models.ModelReporte import ModelReporte

# Entities:
from models.entities.User import User


app = Flask(__name__)

csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['email'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta...")
                return render_template('login.html')
        else:
            flash("El usuario no existe...")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    try:
        granjas = ModelGranja.get_by_owner(db, current_user.id)
        return render_template('InicioAdministrador.html', granjas=granjas)
    except Exception as ex:
        flash(f"Error loading farms: {str(ex)}")
        return redirect(url_for('login'))

@app.route('/recPassword')
def recPassword():
    return render_template('RecuperarContraseña.html')

@app.route('/estadisticas')
@login_required
def estadisticas():
    granja_id = request.args.get('granja_id')
    granja = ModelGranja.get_by_id(db, granja_id, current_user.id)
    if not granja:
        flash("Granja no encontrada")
        return redirect(url_for('home'))
    owner_name = current_user.nombre
    return render_template('Estadisticas.html', granja=granja, owner_name=owner_name)

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/get_granjas')
@login_required
def get_granjas():
    try:
        granjas = ModelGranja.get_by_owner(db, current_user.id)
        return jsonify([{'id': g[0], 'direccion': g[1]} for g in granjas])
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/add_granja', methods=['POST'])
@login_required
def add_granja():
    try:
        data = request.json
        ModelGranja.create_granja(
            db=db,
            direccion=data['direccion'],
            cant_ganado=int(data['cant_ganado']),
            status=int(data['status']),
            tatuaje=data['tatuaje'],
            id_dueño=current_user.id
        )
        return jsonify({'success': True})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as ex:
        app.logger.error(f"Error adding farm: {str(ex)}")
        return jsonify({'error': "Server error"}), 500

@app.route('/get_granja/<int:granja_id>')
@login_required
def get_granja(granja_id):
    try:
        granja = ModelGranja.get_by_id(db, granja_id, current_user.id)
        if not granja:
            return jsonify({'error': 'Granja no encontrada'}), 404

        return jsonify({
            'id': granja[0],
            'direccion': granja[1],
            'cant_ganado': granja[2],
            'status': granja[3],
            'tatuaje': granja[4]
        })
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/update_granja/<int:granja_id>', methods=['PUT'])
@login_required
def update_granja(granja_id):
    try:
        data = request.get_json()
        success = ModelGranja.update_granja(
            db=db,
            granja_id=granja_id,
            owner_id=current_user.id,
            direccion=data['direccion'],
            cant_ganado=data['cant_ganado'],
            status=data['status'],
            tatuaje=data['tatuaje']
        )

        if not success:
            return jsonify({'error': 'Granja no encontrada o no autorizada'}), 404

        return jsonify({'success': True})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/delete_granja/<int:granja_id>', methods=['DELETE'])
@login_required
def delete_granja(granja_id):
    try:
        success = ModelGranja.delete_granja(db, granja_id, current_user.id)
        if not success:
            return jsonify({'error': 'Granja no encontrada o no autorizada'}), 404
        return jsonify({'success': True})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


@app.route('/exportar_pdf')
@login_required
def exportar_pdf():
    # Fetch farm data
    granja_id = request.args.get('granja_id')
    granja = ModelGranja.get_by_id(db, granja_id, current_user.id)

    if not granja:
        flash("Granja no encontrada")
        return redirect(url_for('home'))

    # Fetch owner name from current_user
    owner_name = current_user.nombre

    # Render HTML template with farm data
    html = render_template(
        'pdf_template.html',
        granja=granja,
        owner_name=owner_name,
        # Add other dynamic data here (e.g., charts)
    )

    # Generate PDF
    pdf = HTML(string=html, base_url=request.host_url).write_pdf()

    # Create response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=reporte_granja_{granja_id}.pdf'

    return response


@app.route('/exportar_excel')
@login_required
def exportar_excel():
    granja_id = request.args.get('granja_id')
    granja = ModelGranja.get_by_id(db, granja_id, current_user.id)

    if not granja:
        flash("Granja no encontrada")
        return redirect(url_for('home'))

    try:
        # Get data through model classes
        lotes = ModelReporte.get_lotes_for_export(db, granja_id)
        lote_ids = [lote[0] for lote in lotes]
        vacunos = ModelReporte.get_vacunos_for_export(db, lote_ids)

        # Create DataFrames (keep transformation logic here)
        df_granja = pd.DataFrame([{
            'ID': granja[0],
            'Dirección': granja[1],
            'Cantidad Ganado': granja[2],
            'Estado': 'Activo' if granja[3] else 'Inactivo',
            'Tatuaje': granja[4]
        }])

        df_lotes = pd.DataFrame([{
            'ID Lote': lote[0],
            'Fecha Registro': lote[1],
            'Herraje': lote[2],
            'Cantidad Vacunos': lote[3],
            'Estado': 'Activo' if lote[4] else 'Inactivo'
        } for lote in lotes])

        df_vacunos = pd.DataFrame([{
            'ID Vaca': vaca[0],
            'ID Lote': vaca[1],
            'ID Arete': vaca[2],
            'Género': vaca[3],
            'Fecha Nacimiento': vaca[4],
            'Raza': vaca[5],
            'Estado Salud': vaca[6],
            'Observaciones': vaca[7]
        } for vaca in vacunos])

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_granja.to_excel(writer, sheet_name='Granja', index=False)
            df_lotes.to_excel(writer, sheet_name='Lotes', index=False)
            df_vacunos.to_excel(writer, sheet_name='Vacunos', index=False)

        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            download_name=f"reporte_granja_{granja_id}.xlsx",
            as_attachment=True
        )

    except Exception as ex:
        app.logger.error(f"Error generating Excel: {str(ex)}")
        flash("Error al generar el reporte")
        return redirect(url_for('estadisticas', granja_id=granja_id))

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()