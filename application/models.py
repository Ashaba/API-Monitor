from application.base_model import Base, db

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
	requests = db.relationship('Request', backref='collection', cascade='all, delete-orphan')
	response_summary = db.relationship(
		'ResponseSummary', backref='collection', lazy=True
	)
	schedule = db.Column(db.Time)
	
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
	assertions = db.relationship('RequestAssertion', backref='request', lazy=True)
	headers = db.relationship('Header', backref='request', lazy=True)
	responses = db.relationship('Response', backref='request', lazy=True)


class Response(Base):
	"""
	Model for Response from the scheduled monitoring
	"""
	__tablename__ = 'Response'
	__table_args__ = {'extend_existing': True}
	status_code = db.Column(db.Integer, nullable=False)
	status = db.Column(db.String(), default="failed")
	failures = db.Column(db.Integer, nullable=False)
	response_time = db.Column(db.Integer)
	data = db.Column(db.String(), nullable=False)
	headers = db.Column(db.String(), nullable=False)
	request_id = db.Column(
		db.Integer, db.ForeignKey('Request.id'), nullable=False
	)
	response_summary_id = db.Column(
		db.Integer, db.ForeignKey('ResponseSummary.id'), nullable=False
	)
	response_assertions = db.relationship('ResponseAssertion', backref='response', lazy=True)


class ResponseSummary(Base):
	"""
	Model for storing summary of a set of results run
	"""
	__tablename__ = 'ResponseSummary'
	__table_args__ = {'extend_existing': True}
	status = db.Column(db.String(), nullable=False)
	failures = db.Column(db.Integer, nullable=False)
	run_from = db.Column(db.String())
	responses = db.relationship('Response', backref='summary', lazy=True)
	collection_id = db.Column(
		db.Integer, db.ForeignKey('Collection.id'), nullable=False
	)


class Assertion(Base):
	"""
	Base model for assertions
	"""
	__abstract__ = True
	assertion_type = db.Column(db.String(), nullable=False)
	comparison = db.Column(db.String(), nullable=False)
	value = db.Column(db.Integer, nullable=False)


class RequestAssertion(Assertion):
	"""
	Model for request assertions
	"""
	__tablename__ = 'RequestAssertion'
	__table_args__ = {'extend_existing': True}
	request_id = db.Column(db.Integer, db.ForeignKey('Request.id'), nullable=False)


class ResponseAssertion(Assertion):
	"""
	Model for response assertions
	"""
	__tablename__ = 'ResponseAssertion'
	__table_args__ = {'extend_existing': True}
	status = db.Column(db.String())
	request_assertion_id = db.Column(db.Integer, db.ForeignKey('RequestAssertion.id'), nullable=False)
	request_assertion = db.relationship(
		"RequestAssertion", backref=db.backref("response_assertion", uselist=False))
	response_id = db.Column(
		db.Integer, db.ForeignKey('Response.id'), nullable=False)


class Header(Base):
	"""
	Model for request headers
	"""
	__tablename__ = 'Header'
	__table_args__ = {'extend_existing': True}
	key = db.Column(db.String(), nullable=False)
	value = db.Column(db.String(), nullable=False)
	request_id = db.Column(
		db.Integer, db.ForeignKey('Request.id'), nullable=False
	)
