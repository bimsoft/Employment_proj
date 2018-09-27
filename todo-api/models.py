from sqlalchemy import String, Integer, Column
from database import Base


class employee_detail(Base):
	__tablename__ = "basic_details"

	id = Column(String(36), primary_key=True)
	Name = Column(String(20))
	Title = Column(String(30))
	Company = Column(String(30))
	DOB = Column(String(15))

	def __init__(self, id=0, Name=None, Title=None, Company=None, DOB=None):
		self.id = id
		self.Name = Name
		self.Title = Title
		self.Company = Company
		self.DOB = DOB

	def __repr__(self):
		return  "<employee_detail(id='%s', Name='%s', Title='%s', Company='%s', DOB='%s')>" % (self.id, self.Name, self.Title, self.Company, self.DOB)

	def convert_to_dict(self):
		return {
				'id': self.id,
				'Name': self.Name,
				'Title': self.Title,
				'Company': self.Company,
				'DOB': self.DOB
		}


class project_detail(Base):
	__tablename__ = "project_details"

	
	id = Column(String(36), primary_key=True)
	uname = Column(String(20))
	company = Column(String(20))
	bu_name = Column(String(15))
	client = Column(String(25))
	project = Column(String(25))
	duration = Column(String(3))
	location = Column(String(25))

	def __init__(self, id=0, uname=None, company=None, bu_name=None, client=None, project=None, duration=None, location=None):
		self.id = id
		self.uname = uname
		self.company = company
		self.bu_name = bu_name
		self.client = client
		self.project = project
		self.duration = duration
		self.location = location
		
	def __repr__(self):
		return  "<project_detail(id='%s', uname='%s', company='%s', bu_name='%s', client='%s', project='%s', duration='%s', location='%s')>" % (self.id, self.uname, self.company, self.bu_name, self.client, self.project, self.duration, self.location)

	def convert_to_dict(self):
		return {
				'id': self.id,
				'uname': self.uname,
				'company': self.company,
				'bu_name': self.bu_name,
				'client': self.client,
				'project': self.project,
				'duration': self.duration,
				'location': self.location
		}
