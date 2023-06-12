import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL


# create server as a Flask object
server = Flask(__name__)

# config for mysql connection
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# connect Flask to MySQL database
mysql = MySQL(server)


# create and return json web token 
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "admin": authz,
        },
        secret,
        algorithm="HS256"
    )


# create login route
@server.route("/login", methods =["POST"])
def login():
    # get user data from basic authentication scheme
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    # check database for login and password where email matches username that came in a request   
    cur = mysql.connection.cursor()
    res = cur.execute( 
        "SELECT email, password FROM user WHERE email=%s, (auth.username,)"
    )
    
    # if user exists in database
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        # check if username and password match the ones from request 
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            # return JWT using username and secret from virtual env
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    # if such user does not exists, then credentials are invalid
    else:
        return "invalid credentials", 401


# validate jwt route
@server.route("/validate", method=["POST"])
def validate():
    # get encoded jwt from request
    encoded_jwt = request.headers["Autorization"]
    
    # return error if no jwt in request
    if not encoded_jwt:
        return "missing credentials", 401

    # get token 
    encoded_jwt = encoded_jwt.split(" ")[1]
    
    # decode token
    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"])
    except:
        return "not authorized", 403
    return decoded, 200

if __name__ == "__main__":
    # run flask server
    server.run(host="0.0.0.0", port=5000)
    
   
