from datetime import date


class ModelLote:
    @staticmethod
    def create_lote(db, granja_id):
        try:
            cursor = db.connection.cursor()

            # Default values
            default_data = {
                'fecha_registro': date.today(),
                'cant_vacuno': 0,
                'status': 1
            }

            query = """
                INSERT INTO lote 
                (Fecha_Registro, Cant_Vacuno, Status, ID_Granja)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                default_data['fecha_registro'],
                default_data['cant_vacuno'],
                default_data['status'],
                granja_id
            ))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @staticmethod
    def get_active_lotes(db, granja_id):
        try:
            cursor = db.connection.cursor()
            query = """
                SELECT ID_Lote, Fecha_Registro 
                FROM lote 
                WHERE Status = 1 AND ID_Granja = %s
                ORDER BY Fecha_Registro DESC
            """
            cursor.execute(query, (granja_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_lote_by_id(db, lote_id, owner_id):
        try:
            cursor = db.connection.cursor()
            query = """
                SELECT l.ID_Lote 
                FROM lote l
                JOIN granja g ON l.ID_Granja = g.ID_Granja
                WHERE l.ID_Lote = %s AND g.ID_Dueño = %s
            """
            cursor.execute(query, (lote_id, owner_id))
            return cursor.fetchone()
        except Exception as ex:
            raise Exception(ex)