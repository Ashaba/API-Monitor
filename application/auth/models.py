from application.base_model import Base, db


class User(Base):
	"""
	User model
	"""
	__tablename__ = 'User'
	__table_args__ = {'extend_existing': True}
	
	name = db.Column(db.String(250), nullable=False)
	email = db.Column(db.String(250), unique=True)
	image_url = db.Column(db.String(), nullable=False)
	collections = db.relationship(
		'Collection', backref='owner', lazy='dynamic'
	)
