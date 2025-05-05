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