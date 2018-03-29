from application.base_model import Base, db
from sqlalchemy.orm import backref

# many to many relationship between users and teams
team_members = db.Table(
	'team_members',
	db.Column('user_id', db.Integer, db.ForeignKey('User.id'), nullable=False),
	db.Column('team_id', db.Integer, db.ForeignKey('Team.id'), nullable=False))


class Team(Base):
	"""
	Model for team to access a collection of requests
	"""
	__tablename__ = 'Team'
	__table_args__ = {'extend_existing': True}
	name = db.Column(db.String(128), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
	collections = db.relationship('Collection', backref='team', lazy='select')
	
	def __str__(self):
		return self.name


class Collection(Base):
	"""
	Model for Collection to group particular requests together
	"""
	__tablename__ = 'Collection'
	__table_args__ = {'extend_existing': True}
	
	name = db.Column(db.String(128), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
	team_id = db.Column(db.Integer, db.ForeignKey('Team.id'))
	requests = db.relationship('Request',
                    backref='collection', cascade='all, delete-orphan')
	
	def __str__(self):
		return self.name
	

class Request(Base):
	"""
	Model Request to be monitored
	"""
	__tablename__ = 'Request'
	__table_args__ = {'extend_existing': True}
	collection_id = db.Column(db.Integer, db.ForeignKey('Collection.id'))
	method = db.Column(db.String(128), nullable=False)
	body = db.Column(db.String(255))
	url = db.Column(db.String(255), nullable=False)
	headers = db.Column(db.String(255))
	

class Response(Base):
	"""
	Model for Response from the scheduled monitoring
	"""
	__tablename__ = 'Response'
	__table_args__ = {'extend_existing': True}
	request_id = db.Column(db.Integer, db.ForeignKey('Request.id'))
	status_code = db.Column(db.String(128), nullable=False)
	response_time = db.Column(db.Time)
