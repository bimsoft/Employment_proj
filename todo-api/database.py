from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
						'mysql+pymysql://root:root@localhost/employee?charset=utf8',
						connect_args = {'port':3306},
						echo = 'debug',
						echo_pool = True
						)

db_session = scoped_session(
		sessionmaker(
			bind = engine,
			autocommit = False,
			autoflush = False
			)
		)

Base = declarative_base() 

def init_db():
	import models
	from models import employee_detail
	from models import project_detail

	Base.metadata.create_all(engine)
	db_session.add_all([
		# 	employee_detail(Name='Bim', Title='Sharma', Company='NC', DOB='12-JAN'),
		])

	db_session.commit()
	print ("DB REady to Use")