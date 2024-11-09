from extensions import db

class Detacontrol(db.Model):
    __tablename__ = 'detacontroles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hora = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    
    control_id = db.Column(db.Integer, db.ForeignKey('controles.id', ondelete='CASCADE'), nullable=False)
    control = db.relationship('Control', backref=db.backref('detacontroles', lazy=True))
    
    participante_id = db.Column(db.Integer, db.ForeignKey('participantes.id', ondelete='CASCADE'), nullable=False)
    participante = db.relationship('Participante', backref=db.backref('detacontroles', lazy=True))

    # Constructor
    def __init__(self, estado, control_id, participante_id, hora=None):
        self.estado = estado
        self.control_id = control_id
        self.participante_id = participante_id
        if hora is not None:
            self.hora = hora

    # Guardar nuevo registro
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtener todos los registros
    @staticmethod
    def get_all():
        return Detacontrol.query.all()

    # Obtener un registro por ID
    @staticmethod
    def get_by_id(id):
        return Detacontrol.query.get(id)

    # Actualizar registro
    def update(self, estado=None, control_id=None, participante_id=None, hora=None):
        if estado is not None:
            self.estado = estado
        if control_id is not None:
            self.control_id = control_id
        if participante_id is not None:
            self.participante_id = participante_id
        if hora is not None:
            self.hora = hora
        db.session.commit()

    # Eliminar registro
    def delete(self):
        db.session.delete(self)
        db.session.commit()
