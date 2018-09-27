from flask import Flask, jsonify, abort
from flask import make_response
from flask import request, url_for
from database import init_db, db_session
from models import employee_detail, project_detail
import uuid
from flask import Flask, render_template, redirect, url_for, request



from flask_httpauth import HTTPBasicAuth


init_db()
app = Flask(__name__)
auth = HTTPBasicAuth()

employees = [
				{
					'id' : 1,
					'Name' : 'Bimlesh',
					'title' : 'Sharma',
					'Company' : 'NC',
					'Dob' : "12-Jan-1980"
				},
				{
					'id' : 2,
					'Name' : 'Manoj',
					'title' : 'Verma',
					'Company' : 'VC',
					'Dob' : "10-Jan-1982"
				},
				{
					'id' : 3,
					'Name' : 'Mahesh',
					'title' : 'Kumar',
					'Company' : 'DC',
					'Dob' : "11-Jan-1981"
				}
]

# Common methods

def add_url_for_employee(emp):
	if emp['id']:
		emp['url'] = url_for('get_employeeById', employeeId=emp['id'], _external=True)
	return emp


# Services
@app.teardown_appcontext
def shutdown_dbsession(exception=None):
	db_session.remove()

@app.route('/')
def index():
	all_employees = db_session.query(employee_detail).all()
	return jsonify({'employee': [ al_emp.convert_to_dict() for al_emp in all_employees ] })


@app.route('/todo/api/v1/employees', methods=['GET'])
@auth.login_required
def get_allEmployees():
	all_employees = db_session.query(employee_detail).all()
	return jsonify({'employee' : [ emp.convert_to_dict() for emp in all_employees ] })

@app.route('/todo/api/v1/employees/<string:employeeId>', methods=['GET'])
def get_employeeById(employeeId):
	employee = db_session.query(employee_detail).filter_by(id=employeeId)
	if  employee is None:
		abort (404)
	return jsonify({'task' : employee[0].convert_to_dict()})


'''
Adding new data:
curl -i -H "content-Type:application/json" -X POST -d "{\"Name\":\"NEW1 Bimlesh\",\"title\":\"Sharma\",\"Company\":\"BNC\",\"Dob\":\"12-Jan-1988\"}" http://192.168.160.20:5000/todo/api/v1/employees
'''

@app.route('/todo/api/v1/employees', methods=['POST'])
def add_employee():
	if not request.json or not 'Name' in request.json:
		abort(404)

	ID = uuid.uuid4().hex
	Name = request.json['Name']
	Title = request.json['title']
	Company = request.json['Company']
	Dob = 	request.json['Dob']

	new_emp = employee_detail(id=ID, Name=Name, Title=Title, Company=Company, DOB=Dob)
	db_session.add(new_emp)
	db_session.commit()


	return jsonify({'task' : new_emp.convert_to_dict()}), 201

'''
Updating data
curl -i -H "content-Type: application/json" -X PUT -d "{\"Name\":\"Update Bimlesh\"}" http://192.168.160.20:5000/todo/api/v1/employees/38cd2e2c0a924e5b882b1071ff30a23d
'''

@app.route('/todo/api/v1/employees/<string:employeeId>', methods=['PUT'])
def update_employee(employeeId):

	searched_employee = db_session.query(employee_detail).get(employeeId)

	if not request.json:
		abort(400)
	if 'Name' in request.json and type(request.json['Name']) !=  str:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != str:
		abort(400)
	if 'Company' in request.json and type(request.json['Company']) is not str:
		abort(400)
	if 'Dob' in request.json and type(request.json['Dob']) is not bool:
		abort(400)
	if searched_employee is None:
		abort(400)
	
	searched_employee.Name = request.json.get('Name', searched_employee.Name)
	searched_employee.Title = request.json.get('title', searched_employee.Title)
	searched_employee.Company = request.json.get('Company', searched_employee.Company)
	searched_employee.DOB = request.json.get('Dob', searched_employee.DOB)
	db_session.commit()

	return jsonify({'Employee' : searched_employee.Name})

'''
Delete data

'''
@app.route('/todo/api/v1/employees/<string:employeeId>', methods=['DELETE'])
def remove_empl(employeeId):
	emp_to_delete = db_session.query(employee_detail).get(employeeId)

	if emp_to_delete is None:
		abort(400)
	db_session.delete(emp_to_delete)
	db_session.commit()
	return jsonify({'result' : True})

'''
home
'''
@app.route('/home', methods=['GET'])
def home():
	return render_template('employeedetails.html')


''' Project Details page'''
@app.route('/submitproj', methods=['POST'])
def submit_project():
	# if not request.json:
	# 	abort(400)

	# if  not 'username' in request.jsonify:
	# 	abort(404)
	error = 'None'
	ID = uuid.uuid4().hex
	uname = request.json["username"]
	company = request.json['company']
	bu_name = request.json['bu']
	client = 	request.json['client']
	project = request.json['project']
	duration = 	request.json['duration']
	location = request.json['location']

	new_project = project_detail(id=ID, uname=uname, company=company, bu_name=bu_name, client=client, project=project, duration=duration, location=location)
	db_session.add(new_project)
	db_session.commit()

	return render_template('thank.html', error=error)

'''
Login Page
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = 'None'
	if request.method == 'POST':
		if request.form['uname'] != 'bimlesh' and request.form['psw'] != 'bimlesh':
			error = "Invalid creential,  please try again"
		else:
			return redirect(url_for('home'))
	return render_template('relogin.html', error=error)


'''
HTTP authentication on every request
'''

@auth.get_password
def get_password(username):
	if username == 'bimlesh':
		return username
	return None


# Errors handling

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error' : 'Something wrong with request'}), 400)

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error' : 'unauthorized access'}))


# Main calling

if __name__ == '__main__':

	app.run(host='bimlesh3146322', debug=True)

