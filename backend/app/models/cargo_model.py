from extensions import db

class Cargo(db.Model):
    __tablename__ = 'cargos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255), nullable=False)

    # Constructor
    def __init__(self, descripcion):
        self.descripcion = descripcion

    # Guardar nuevo registro
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtener todos los registros
    @staticmethod
    def get_all():
        return Cargo.query.all()

    # Obtener un registro por ID
    @staticmethod
    def get_by_id(id):
        return Cargo.query.get(id)

    # Actualizar registro
    def update(self, descripcion=None):
        if descripcion is not None:
            self.descripcion = descripcion
        db.session.commit()

    # Eliminar registro
    def delete(self):
        db.session.delete(self)
        db.session.commit()
