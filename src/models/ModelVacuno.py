class ModelVacuno:
    @staticmethod
    def get_vacunos_by_granja(db, granja_id):
        try:
            cursor = db.connection.cursor()
            query = """
                SELECT v.ID_Arete, v.ID_Fierro, v.Genero, 
                       v.Fecha_Nacimiento, v.Raza, v.Proposito
                FROM vacuno v
                JOIN lote l ON v.ID_Lote = l.ID_Lote
                WHERE l.ID_Granja = %s
            """
            cursor.execute(query, (granja_id,))
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def update_vacuno(db, etiqueta, nuevos_datos):
        try:
            cursor = db.connection.cursor()
            query = """
                UPDATE vacuno
                SET ID_Fierro = %s,
                    Genero = %s,
                    Fecha_Nacimiento = %s,
                    Raza = %s,
                    Proposito = %s
                WHERE ID_Arete = %s
            """
            params = (
                nuevos_datos['fierro'],
                nuevos_datos['sexo'],
                nuevos_datos['fecha_nacimiento'],
                nuevos_datos['raza'],
                nuevos_datos['proposito'],
                etiqueta
            )
            cursor.execute(query, params)
            db.connection.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @staticmethod
    def delete_vacuno(db, etiqueta, owner_id):
        try:
            cursor = db.connection.cursor()
            query = """
                DELETE v FROM vacuno v
                JOIN lote l ON v.ID_Lote = l.ID_Lote
                JOIN granja g ON l.ID_Granja = g.ID_Granja
                WHERE v.ID_Arete = %s AND g.ID_Dueño = %s
            """
            cursor.execute(query, (etiqueta, owner_id))
            db.connection.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @staticmethod
    def create_vacuno(db, data):
        try:
            cursor = db.connection.cursor()

            query = """
                    INSERT INTO vacuno (
                        ID_Lote, ID_Arete, ID_Fierro, Genero,
                        Fecha_Nacimiento, Fecha_Registro, Raza,
                        Estado_Salud, Proposito
                    ) VALUES (%s, %s, %s, %s, %s, CURDATE(), %s, 'Sano', %s)
                """
            params = (
                data['lote'],
                data['etiqueta'],
                data['fierro'],
                data['sexo'],
                data['fecha_nacimiento'],
                data['raza'],
                data['proposito']
            )

            cursor.execute(query, params)

            # Update lote count
            cursor.execute("""
                    UPDATE lote 
                    SET Cant_Vacuno = Cant_Vacuno + 1 
                    WHERE ID_Lote = %s
                """, (data['lote'],))

            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @staticmethod
    def get_vacuno_by_etiqueta(db, etiqueta, owner_id):
        try:
            cursor = db.connection.cursor()
            query = """
                SELECT 
                    v.*, 
                    l.Nombre AS lote_nombre,
                    g.Dirección AS granja_nombre,
                    g.ID_Granja
                FROM vacuno v
                JOIN lote l ON v.ID_Lote = l.ID_Lote
                JOIN granja g ON l.ID_Granja = g.ID_Granja
                WHERE v.ID_Arete = %s 
                AND g.ID_Dueño = %s
            """
            cursor.execute(query, (etiqueta, owner_id))
            return cursor.fetchone()
        except Exception as ex:
            raise Exception(f"Database error: {str(ex)}")