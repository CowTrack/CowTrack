class ModelGranja:

    @classmethod
    def get_by_owner(cls, db, owner_id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM granja WHERE ID_Dueño = %s", (owner_id,))
            result = cursor.fetchall()
            return result
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def create_granja(cls, db, direccion, cant_ganado, status, tatuaje, id_dueño):
        try:
            cursor = db.connection.cursor()
            cursor.execute(
                "INSERT INTO granja (Dirección, Cant_Ganado, Status, Tatuaje, ID_Dueño) VALUES (%s, %s, %s, %s, %s)",
                (direccion, cant_ganado, status, tatuaje, id_dueño)
            )
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def get_by_id(cls, db, granja_id, owner_id):
        try:
            cursor = db.connection.cursor()
            cursor.execute(
                "SELECT * FROM granja WHERE ID_Granja = %s AND ID_Dueño = %s",
                (granja_id, owner_id)
            )
            return cursor.fetchone()
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def update_granja(cls, db, granja_id, owner_id, **kwargs):
        try:
            cursor = db.connection.cursor()
            cursor.execute(
                """UPDATE granja SET 
                    Dirección = %s,
                    Cant_Ganado = %s,
                    Status = %s,
                    Tatuaje = %s
                WHERE ID_Granja = %s AND ID_Dueño = %s""",
                (
                    kwargs['direccion'],
                    kwargs['cant_ganado'],
                    kwargs['status'],
                    kwargs['tatuaje'],
                    granja_id,
                    owner_id
                )
            )
            db.connection.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def delete_granja(cls, db, granja_id, owner_id):
        try:
            cursor = db.connection.cursor()
            cursor.execute(
                "DELETE FROM granja WHERE ID_Granja = %s AND ID_Dueño = %s",
                (granja_id, owner_id)
            )
            db.connection.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()