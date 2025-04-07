from .entities.User import User

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID_Dueno, Nombre, correo, password 
                    FROM dueño 
                    WHERE correo = %s"""  # Parameterized query
            cursor.execute(sql, (user.correo,))  # Pass parameters as tuple
            row = cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    correo=row[2],
                    password=User.check_password(row[3], user.password),
                    nombre=row[1]
                )
            return None
        except Exception as ex:
            raise Exception(f"Database error: {str(ex)}")
        finally:
            cursor.close()

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID_Dueno, Nombre, correo 
                    FROM dueño 
                    WHERE ID_Dueno = %s"""  # Parameterized query
            cursor.execute(sql, (id,))  # Pass parameters as tuple
            row = cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    correo=row[2],
                    password=None,
                    nombre=row[1]
                )
            return None
        except Exception as ex:
            raise Exception(f"Database error: {str(ex)}")
        finally:
            cursor.close()