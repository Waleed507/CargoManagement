import flask
from flask import jsonify
from flask import request
from sql import create_connection
from sql import execute_read_query
from datetime import datetime
import creds

app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbname)
cursor = conn.cursor(dictionary=True)

authorizedusers = [
  {
    #default user
    'username': 'username',
    'password': 'password',
    'role': 'Admin',
    'token': '0',
    'admininfo': None
  },
]

@app.route('/login', methods = ['GET'])
def app_login():
    username = request.headers['username'] #get header parameter
    pw = request.headers['password']
    for au in authorizedusers: 
        if au['username'] == username and au['password'] == pw: #found an auth user
          sessiontoken = au['token']
          admininfo = au['admininfo']
          returninfo = []
          returninfo.append(au['role'])
          return jsonify(returninfo)
    return 'SECURITY ERROR'

spaceship_list = []
cargo_list = []
captain_list = []

# Get all spaceships
@app.route('/spaceship', methods=['GET'])
def get_spaceship():
    sql = 'SELECT * from spaceship'
    get_spaceship = execute_read_query(conn, sql)
    spaceship_list.append(get_spaceship)
    return jsonify(spaceship_list)

# Add Spaceship
@app.route('/spaceship', methods=['POST'])
def add_spaceship():          
  request_data = request.get_json()   
  add_weight = request_data['maxweight']    
  add_captainid = request_data['captainid']
  sql_captainid = "Select * from captain where id = %s" 
  val1 = (add_captainid,)
  cursor.execute(sql_captainid,val1)
  result = cursor.fetchone() 
  if result is None: # If the id is not found
     return 'Captain Does not exist'
  sql = "INSERT INTO spaceship(maxweight, captainid) VALUES (%s, %s)"   #SQL Insert command
  val = (add_weight, add_captainid)                
  cursor.execute(sql, val)
  conn.commit()
  return 'Add request successful'
      
# Update Spaceship
@app.route('/spaceship/<id>', methods=['PUT']) #Id must be in the url
def update_spaceship(id):
  request_data = request.get_json()   
  update_weight = request_data['maxweight']    
  update_captainid = request_data['captainid']

  sql_spaceshipid = "Select * from spaceship where id = %s"
  val_spaceship = (id, )
  cursor.execute(sql_spaceshipid, val_spaceship)
  result_spaceship = cursor.fetchone()
  if result_spaceship is None: # If id is not found
     return 'Spaceship Does not exist'

  sql_captainid = "Select * from captain where id = %s"
  val1 = (update_captainid,)
  cursor.execute(sql_captainid,val1)
  result = cursor.fetchone()
  if result is None:
     return 'Captain Does not exist' 
        
  sql = "UPDATE spaceship SET maxweight = %s, captainid = %s Where id = %s" #SQL Command to Update
  val = (update_weight, update_captainid, id)                

  cursor.execute(sql, val)
  conn.commit() #To make sure changes are made in databse
  return 'Update request successful'

# Delete spaceship
@app.route('/spaceship/<id>', methods=['DELETE']) #Id must be in the url
def delete_spaceship(id):
  sql = "DELETE FROM spaceship WHERE id = %s" #SQl command for delete
  val = (id,)
  cursor.execute(sql, val)
  conn.commit()
  return 'Delete request successful'


# View All Cargo
@app.route('/cargo', methods=['GET'])
def get_cargo():
    sql = 'SELECT * from cargo'
    get_cargo = execute_read_query(conn, sql)
    cargo_list.append(get_cargo)
    return jsonify(cargo_list) #Returns in JSON Format

# Add Cargo
@app.route('/cargo', methods=['POST'])
def add_cargo():          
    request_data = request.get_json()   
    add_weight = request_data['weight']    
    add_cargotype = request_data['cargotype']
    add_cargoid = request_data['shipid']  
    
    # Check if the spaceship exists
    sql_spaceship = "SELECT * FROM spaceship WHERE id = %s"
    val_spaceship = (add_cargoid,)
    cursor.execute(sql_spaceship, val_spaceship)
    spaceship_result = cursor.fetchone()
    if spaceship_result is None:
        return 'Spaceship does not exist'
    
    # Check if there is enough room in the spaceship for the cargo
    max_weight = spaceship_result['maxweight']
    if add_weight > max_weight:
        return 'Not enough room for the cargo'
      
    # Insert the cargo record into the database
    sql_cargo = "INSERT INTO cargo(weight, cargotype, shipid) VALUES (%s, %s, %s)"
    val_cargo = (add_weight, add_cargotype, add_cargoid)                
    cursor.execute(sql_cargo, val_cargo)
    conn.commit()
    
    return 'Add request successful'

# Update Cargo 
@app.route('/cargo/<cargoid>', methods = ['PUT'])
def update_cargo(cargoid):
   request_data = request.get_json()
   update_weight = request_data['weight']    
   update_cargotype = request_data['cargotype']
   update_departure = request_data['departure']
   update_arrival = request_data['arrival']
   update_shipid = request_data['shipid']
   
   #To Check if Cargo exisits
   sql_cargo = "SELECT * FROM cargo WHERE id = %s"
   val_check = (cargoid,)
   cursor.execute(sql_cargo, val_check)
   result = cursor.fetchone()
 
   if result is None:
      return 'Cargo does not exist'
   
   # To Check if Spaceship exists
   sql_spaceship = "Select * from spaceship where id = %s"
   val = (update_shipid,)
   cursor.execute(sql_spaceship,val)
   spaceship_result = cursor.fetchone()

   if spaceship_result is None:
      return 'Spaceship does not exist'

   if update_weight > spaceship_result['maxweight']:
      return 'Not enough room for the cargo'

   sql_update = "Update cargo set weight = %s, cargotype = %s, departure = %s, arrival = %s, shipid = %s WHERE id = %s" #SQL Update Command

   val_update = (update_weight,update_cargotype, str(update_departure), str(update_arrival), update_shipid, cargoid)
   cursor.execute(sql_update, val_update)
   conn.commit()

   return 'Update Request Successful'

# Delete Cargo
@app.route('/cargo/<cargoid>', methods=['DELETE']) #Id must be in the url
def delete_cargo(cargoid):
  sql = "DELETE FROM cargo WHERE id = %s" #SQl command for delete
  val = (cargoid,)
  cursor.execute(sql, val)
  conn.commit()
  return 'Delete request successful' 

# Get all captain
@app.route('/captain', methods=['GET'])
def get_captain():
    sql = 'SELECT * from captain'
    get_captain = execute_read_query(conn, sql)
    captain_list.append(get_captain)
    return jsonify(captain_list)

@app.route('/captain', methods=['POST'])
def add_captain():          
  request_data = request.get_json()   
  add_firstname = request_data['firstname'] #The inputs from postman
  add_lastname = request_data['lastname']
  add_rank = request_data['captain_rank']
  add_homeplanet = request_data['homeplanet']       
  sql = "INSERT INTO captain(firstname, lastname, captain_rank, homeplanet) VALUES (%s, %s, %s, %s)"   #
  val = (add_firstname, add_lastname, add_rank, add_homeplanet) 

  cursor.execute(sql, val)
  conn.commit()
  return 'Add request successful'

@app.route('/captain/<id>', methods=['PUT']) #Id must be in the url
def update_captain(id):
  request_data = request.get_json()  
  update_firstname = request_data['firstname']
  update_lastname = request_data['lastname']
  update_rank = request_data['captain_rank']
  update_homeplanet = request_data['homeplanet']       
  sql = "UPDATE captain SET firstname = %s, lastname = %s, captain_rank = %s, homeplanet = %s WHERE id = %s"#SQL Command to Update
  val = (update_firstname, update_lastname, update_rank, update_homeplanet, id)                

  cursor.execute(sql, val)
  conn.commit() #To make sure changes are made in databse
  return 'Update request successful'  

@app.route('/captain/<id>', methods=['DELETE']) #Id must be in the url
def delete_captain(id):
  sql = "DELETE FROM captain WHERE id = %s" #SQl command for delete
  val = (id,)
  cursor.execute(sql, val)
  conn.commit()
  return 'Delete request successful' 
      
app.run()
    
