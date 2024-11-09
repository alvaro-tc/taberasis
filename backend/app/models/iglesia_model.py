from extensions import db
from sqlalchemy.orm import validates

class Iglesia(db.Model):
    __tablename__ = 'iglesias'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.Text, nullable=True)

    # Constructor
    def __init__(self, nombre, area, ciudad=None, direccion=None):
        self.nombre = nombre
        self.area = area
        self.ciudad = ciudad
        self.direccion = direccion

    # Validación para el campo "area"
    @validates('area')
    def validate_area(self, key, value):
        if value.lower() not in ['URBANO', 'RURAL']:
            raise ValueError("El área debe ser URBANO o RURAL")
        return value.lower()

    # Guardar nuevo registro
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtener todos los registros
    @staticmethod
    def get_all():
        return Iglesia.query.all()

    # Obtener un registro por ID
    @staticmethod
    def get_by_id(id):
        return Iglesia.query.get(id)

    # Actualizar registro
    def update(self, nombre=None, area=None, ciudad=None, direccion=None):
        if nombre is not None:
            self.nombre = nombre
        if area is not None:
            self.area = self.validate_area('area', area)
        if ciudad is not None:
            self.ciudad = ciudad
        if direccion is not None:
            self.direccion = direccion
        db.session.commit()

    # Eliminar registro
    def delete(self):
        db.session.delete(self)
        db.session.commit()
