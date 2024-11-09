from extensions import db

class Participante(db.Model):
    __tablename__ = 'participantes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellidos = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    codigo = b.Column(db.Text, nullable=True)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos.id', ondelete='CASCADE'), nullable=False)
    tipo = db.relationship('Tipo', backref=db.backref('participantes', lazy=True))
    
    iglesia_id = db.Column(db.Integer, db.ForeignKey('iglesias.id', ondelete='CASCADE'), nullable=False)
    iglesia = db.relationship('Iglesia', backref=db.backref('participantes', lazy=True))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Iglesia', backref=db.backref('users', lazy=True)) 

    def __init__(self, nombre, apellidos, email=None, telefono=None, tipo_id=None, iglesia_id=None):
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.tipo_id = tipo_id
        self.iglesia_id = iglesia_id
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Participante.query.all()

    @staticmethod
    def get_by_id(id):
        return Participante.query.get(id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
