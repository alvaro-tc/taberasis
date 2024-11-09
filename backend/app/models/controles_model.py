from extensions import db

class Control(db.Model):
    __tablename__ = 'controles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    descripcion = db.Column(db.String(250), nullable=True)
    estado = db.Column(db.Integer, nullable=False)
    
    tipoc_id = db.Column(db.Integer, db.ForeignKey('tipocontroles.id', ondelete='CASCADE'), nullable=False)
    tipoc = db.relationship('Tipocontrol', backref=db.backref('controles', lazy=True))

    # Constructor
    def __init__(self, estado, descripcion=None, tipoc_id=None):
        self.descripcion = descripcion
        self.estado = estado
        self.tipoc_id = tipoc_id

    # Guardar nuevo registro
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtener todos los registros
    @staticmethod
    def get_all():
        return Control.query.all()

    # Obtener un registro por ID
    @staticmethod
    def get_by_id(id):
        return Control.query.get(id)

    # Actualizar registro
    def update(self, descripcion=None, estado=None, tipoc_id=None):
        if descripcion is not None:
            self.descripcion = descripcion
        if estado is not None:
            self.estado = estado
        if tipoc_id is not None:
            self.tipoc_id = tipoc_id
        db.session.commit()

    # Eliminar registro
    def delete(self):
        db.session.delete(self)
        db.session.commit()
