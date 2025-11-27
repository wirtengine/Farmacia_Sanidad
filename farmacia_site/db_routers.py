class UsersRouter:
    """
    Router para dirigir todas las operaciones del modelo Usuario a la base de datos Users.db
    """

    app_label = 'usuarios'   # app donde está tu modelo Usuario

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'users_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'users_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # permitir relaciones internas dentro de la app usuarios
        if (
            obj1._meta.app_label == self.app_label or
            obj2._meta.app_label == self.app_label
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # migraciones de usuarios -> Users.db
        if app_label == self.app_label:
            return db == 'users_db'

        # impedir que usuarios migre a Farmacia.db
        if db == 'users_db' and app_label != self.app_label:
            return False

        return None
