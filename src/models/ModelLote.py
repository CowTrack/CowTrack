from datetime import date


class ModelLote:
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

    @staticmethod
    def get_lotes_by_granja(db, granja_id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT l.ID_Lote, l.Nombre, l.Fecha_Registro, 
                             l.Cant_Vacuno, l.Status 
                      FROM lote l 
                      WHERE l.ID_Granja = %s 
                      ORDER BY l.Fecha_Registro DESC"""
            cursor.execute(sql, (granja_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def create_lote(db, nombre, granja_id):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO lote (Nombre, Fecha_Registro, Cant_Vacuno, Status, ID_Granja) 
                     VALUES (%s, CURDATE(), 0, 1, %s)"""
            cursor.execute(sql, (nombre, granja_id))
            db.connection.commit()
            return cursor.lastrowid
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @staticmethod
    def delete_lote(db, lote_id, owner_id):
        try:
            cursor = db.connection.cursor()
            # Verify ownership through farm
            sql = """DELETE l FROM lote l
                     INNER JOIN granja g ON l.ID_Granja = g.ID_Granja
                     WHERE l.ID_Lote = %s AND g.ID_Dueño = %s"""
            cursor.execute(sql, (lote_id, owner_id))
            db.connection.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @staticmethod
    def toggle_status(db, lote_id, owner_id):
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE lote l
                     INNER JOIN granja g ON l.ID_Granja = g.ID_Granja
                     SET l.Status = NOT l.Status
                     WHERE l.ID_Lote = %s AND g.ID_Dueño = %s"""
            cursor.execute(sql, (lote_id, owner_id))
            db.connection.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)