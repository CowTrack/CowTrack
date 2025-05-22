class ModelReporte:

    @classmethod
    def get_lotes_for_export(cls, db, granja_id):
        """Get lotes data for Excel export"""
        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT * FROM lote 
                WHERE ID_Granja = %s
            """, (granja_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(f"Error getting lotes: {str(ex)}")
        finally:
            cursor.close()

    @classmethod
    def get_vacunos_for_export(cls, db, lote_ids):
        """Get vacunos data for Excel export"""
        if not lote_ids:
            return []

        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT * FROM vacuno 
                WHERE ID_Lote IN %s
            """, (tuple(lote_ids),))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(f"Error getting vacunos: {str(ex)}")
        finally:
            cursor.close()

    @classmethod
    def get_monthly_cattle_stats(cls, db, granja_id, current_year):
        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT 
                    MONTH(v.Fecha_Registro) AS Month,
                    COUNT(v.ID_Vaca) AS Total
                FROM vacuno v
                JOIN lote l ON v.ID_Lote = l.ID_Lote
                WHERE l.ID_Granja = %s 
                AND YEAR(v.Fecha_Registro) = %s
                GROUP BY Month
                ORDER BY Month
            """, (granja_id, current_year))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def get_reportes_by_granja(cls, db, granja_id):
        """Get all reports for a specific farm"""
        try:
            cursor = db.connection.cursor()
            # Join with vacuno and lote to filter by granja_id
            cursor.execute("""
                SELECT 
                    r.ID_Reporte,
                    v.ID_Arete AS etiqueta,
                    r.Fecha_Reporte,
                    r.Tipo_Reporte,
                    r.Observacion
                FROM reporte r
                JOIN vacuno v ON r.ID_Vaca = v.ID_Vaca
                JOIN lote l ON v.ID_Lote = l.ID_Lote
                WHERE l.ID_Granja = %s
                ORDER BY r.Fecha_Reporte DESC
            """, (granja_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(f"Error fetching reports: {str(ex)}")
        finally:
            cursor.close()

    @classmethod
    def create_reporte(cls, db, data, granja_id):
        """Create a new report linked to a specific farm"""
        try:
            cursor = db.connection.cursor()

            # Verify vacuno belongs to the farm
            cursor.execute("""
                SELECT v.ID_Vaca 
                FROM vacuno v
                JOIN lote l ON v.ID_Lote = l.ID_Lote
                WHERE v.ID_Arete = %s AND l.ID_Granja = %s
            """, (data['etiqueta'], granja_id))

            vacuno = cursor.fetchone()
            if not vacuno:
                raise ValueError("Etiqueta no existe en esta granja")

            # Insert report
            cursor.execute("""
                INSERT INTO reporte 
                (ID_Vaca, Fecha_Reporte, Tipo_Reporte, Observacion)
                VALUES (%s, %s, %s, %s)
            """, (
                vacuno[0],  # ID_Vaca from previous query
                data['fecha_reporte'],
                data['tipo_reporte'],
                data['observacion']
            ))

            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @classmethod
    def delete_reporte(cls, db, reporte_id, owner_id):
        """Delete a report if it belongs to the owner's farm"""
        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                DELETE r FROM reporte r
                JOIN vacuno v ON r.ID_Vaca = v.ID_Vaca
                JOIN lote l ON v.ID_Lote = l.ID_Lote
                JOIN granja g ON l.ID_Granja = g.ID_Granja
                WHERE r.ID_Reporte = %s AND g.ID_Dueño = %s
            """, (reporte_id, owner_id))

            db.connection.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @staticmethod
    def get_reportes_by_vaca(db, vaca_id):
        try:
            cursor = db.connection.cursor()
            query = """
                SELECT * FROM reporte 
                WHERE ID_Vaca = %s
                ORDER BY Fecha_Reporte DESC
            """
            cursor.execute(query, (vaca_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_razas_distribution(cls, db, granja_id):
        """Get vacunos count by raza for the farm"""
        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT raza, COUNT(*) as cantidad 
                FROM vacuno 
                WHERE ID_Lote IN (
                    SELECT ID_Lote FROM lote WHERE ID_Granja = %s
                )
                GROUP BY raza
            """, (granja_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(f"Error getting razas: {str(ex)}")
        finally:
            cursor.close()

    @classmethod
    def get_ejemplares_mensuales(cls, db, granja_id):
        """Get monthly count of vacunos"""
        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                   SELECT MONTH(fecha_nacimiento) as mes, COUNT(*) 
                   FROM vacuno 
                   WHERE ID_Lote IN (
                       SELECT ID_Lote FROM lote WHERE ID_Granja = %s
                   )
                   GROUP BY MONTH(fecha_nacimiento)
                   ORDER BY mes
               """, (granja_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(f"Error getting monthly data: {str(ex)}")
        finally:
            cursor.close()