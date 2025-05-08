from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, send_file
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from weasyprint import HTML
from io import BytesIO
import pandas as pd
import openpyxl

from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelGranja import ModelGranja
from models.ModelReporte import ModelReporte
from models.ModelVacuno import ModelVacuno
from models.ModelLote import ModelLote

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)

@app.template_filter('calcular_edad')
def calcular_edad(fecha_nacimiento):
    hoy = datetime.now().date()
    nacimiento = fecha_nacimiento
    edad = hoy.year - nacimiento.year
    #Revisa si el nacimiento ha ocurrido en este año
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return f"{edad} años"

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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

    breed_stats = ModelGranja.get_breed_stats(db, granja_id)

    current_year = datetime.now().year
    monthly_stats = ModelReporte.get_monthly_cattle_stats(db, granja_id, current_year)

    monthly_counts = [0] * 12
    for month, total in monthly_stats:
        monthly_counts[month - 1] = total

    owner_name = current_user.nombre
    return render_template(
        'Estadisticas.html',
        granja=granja,
        owner_name=owner_name,
        monthly_counts=monthly_counts,
        razas=breed_stats
    )

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


@app.route('/gestion_ganado')
@login_required
def gestion_ganado():
    granja_id = request.args.get('granja_id')
    granja = ModelGranja.get_by_id(db, granja_id, current_user.id)

    if not granja:
        flash("Granja no encontrada")
        return redirect(url_for('home'))

    vacunos = ModelVacuno.get_vacunos_by_granja(db, granja_id)
    lotes = ModelLote.get_active_lotes(db, granja_id)

    return render_template('GestionGanado.html',
                           vacunos=vacunos,
                           granja=granja,
                           lotes=lotes)


@app.route('/crear_vacuno', methods=['POST'])
@login_required
def crear_vacuno():
    try:
        data = request.get_json()

        # Validate lote belongs to user's farm
        lote = ModelLote.get_lote_by_id(db, data['lote'], current_user.id)
        if not lote:
            return jsonify({'success': False, 'error': 'Lote no válido'}), 400

        ModelVacuno.create_vacuno(db, {
            'lote': data['lote'],
            'etiqueta': data['etiqueta'],
            'fierro': data['fierro'],
            'sexo': data['sexo'],
            'fecha_nacimiento': data['fecha_nacimiento'],
            'raza': data['raza'],
            'proposito': data['proposito']
        })

        return jsonify({'success': True})

    except Exception as ex:
        app.logger.error(f"Error creating cattle: {str(ex)}")
        return jsonify({'success': False, 'error': str(ex)}), 500

@app.route('/actualizar_vacuno', methods=['POST'])
@login_required
def actualizar_vacuno():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['etiqueta', 'fierro', 'sexo', 'fecha_nacimiento', 'raza', 'proposito']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Faltan campos requeridos'}), 400

        # Update in database
        updated = ModelVacuno.update_vacuno(
            db=db,
            etiqueta=data['etiqueta'],
            nuevos_datos={
                'fierro': data['fierro'],
                'sexo': data['sexo'],
                'fecha_nacimiento': data['fecha_nacimiento'],
                'raza': data['raza'],
                'proposito': data['proposito']
            }
        )

        if not updated:
            return jsonify({'success': False, 'error': 'Vacuno no encontrado'}), 404

        return jsonify({'success': True})

    except Exception as ex:
        app.logger.error(f"Error updating cattle: {str(ex)}")
        return jsonify({'success': False, 'error': str(ex)}), 500


@app.route('/eliminar_vacuno', methods=['POST'])
@login_required
def eliminar_vacuno():
    try:
        data = request.get_json()
        etiqueta = data.get('etiqueta')

        if not etiqueta:
            return jsonify({'success': False, 'error': 'Falta la etiqueta del vacuno'}), 400

        deleted = ModelVacuno.delete_vacuno(
            db=db,
            etiqueta=etiqueta,
            owner_id=current_user.id
        )

        if not deleted:
            return jsonify({'success': False, 'error': 'Vacuno no encontrado o no autorizado'}), 404

        return jsonify({'success': True})

    except Exception as ex:
        app.logger.error(f"Error deleting cattle: {str(ex)}")
        return jsonify({'success': False, 'error': str(ex)}), 500


@app.route('/crear_lote', methods=['POST'])
@login_required
def crear_lote():
    try:
        granja_id = request.args.get('granja_id')

        # Verify farm ownership
        granja = ModelGranja.get_by_id(db, granja_id, current_user.id)
        if not granja:
            return jsonify({'success': False, 'error': 'Granja no encontrada'}), 404

        # Create new lote
        ModelLote.create_lote(db, granja_id)

        return jsonify({'success': True})

    except Exception as ex:
        app.logger.error(f"Error creating lote: {str(ex)}")
        return jsonify({'success': False, 'error': str(ex)}), 500

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
            'Proposito': vaca[7]
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


@app.route('/importar_vacunos', methods=['POST'])
@login_required
def importar_vacunos():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        if not file.filename.endswith('.xlsx'):
            return jsonify({'success': False, 'error': 'Solo se aceptan archivos XLSX'}), 400

        # Read Excel file
        df = pd.read_excel(file, dtype=str)
        required_columns = ['Etiqueta', 'Fierro', 'Sexo', 'Fecha_Nacimiento', 'Raza', 'Proposito', 'Lote_ID']

        # Validate columns
        if not all(col in df.columns for col in required_columns):
            return jsonify({
                'success': False,
                'error': f'El archivo debe contener estas columnas: {", ".join(required_columns)}'
            }), 400

        success_count = 0
        errors = []

        for index, row in df.iterrows():
            try:
                # Validate lote ownership
                lote = ModelLote.get_lote_by_id(db, row['Lote_ID'], current_user.id)
                if not lote:
                    errors.append(f"Fila {index + 2}: Lote ID {row['Lote_ID']} no válido")
                    continue

                # Prepare cattle data
                cattle_data = {
                    'lote': row['Lote_ID'],
                    'etiqueta': row['Etiqueta'],
                    'fierro': row['Fierro'],
                    'sexo': row['Sexo'],
                    'fecha_nacimiento': row['Fecha_Nacimiento'],
                    'raza': row['Raza'],
                    'proposito': row['Proposito']
                }

                # Insert into database
                ModelVacuno.create_vacuno(db, cattle_data)
                success_count += 1

            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
                continue

        return jsonify({
            'success': True,
            'imported': success_count,
            'errors': errors
        })

    except Exception as ex:
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(ex)}'
        }), 500


@app.route('/gestion_reportes')
@login_required
def gestion_reportes():
    granja_id = request.args.get('granja_id')
    granja = ModelGranja.get_by_id(db, granja_id, current_user.id)

    if not granja:
        flash("Granja no encontrada")
        return redirect(url_for('home'))

    reportes = ModelReporte.get_reportes_by_granja(db, granja_id)
    return render_template('GestionReportes.html', granja=granja, reportes=reportes)


@app.route('/crear_reporte', methods=['POST'])
@login_required
def crear_reporte():
    try:
        data = request.get_json()
        granja_id = data.get('granja_id')

        # Validate farm ownership
        granja = ModelGranja.get_by_id(db, granja_id, current_user.id)
        if not granja:
            return jsonify({'success': False, 'error': 'Granja no válida'}), 400

        ModelReporte.create_reporte(db, {
            'etiqueta': data['etiqueta'],
            'fecha_reporte': data['fecha_reporte'],
            'tipo_reporte': data['tipo_reporte'],
            'observacion': data['observacion']
        }, granja_id)

        return jsonify({'success': True})

    except Exception as ex:
        return jsonify({'success': False, 'error': str(ex)}), 500


@app.route('/eliminar_reporte', methods=['POST'])
@login_required
def eliminar_reporte():
    try:
        data = request.get_json()
        reporte_id = data.get('reporte_id')

        if not reporte_id:
            return jsonify({'success': False, 'error': 'Falta el ID del reporte'}), 400

        deleted = ModelReporte.delete_reporte(
            db=db,
            reporte_id=reporte_id,
            owner_id=current_user.id
        )

        if not deleted:
            return jsonify({'success': False, 'error': 'Reporte no encontrado o no autorizado'}), 404

        return jsonify({'success': True})

    except Exception as ex:
        return jsonify({'success': False, 'error': str(ex)}), 500

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