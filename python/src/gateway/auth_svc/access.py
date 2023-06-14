import os, requests

def login(request):
	auth = request.authorization
	# if no authorization parameters in request
	if not auth:
		return None, ("missing credentials", 401)
		
	# get user data from basic authentication scheme
	basicAuth = (auth.username, auth.password)
	# make post request to auth service
	response = requests.post(
		f"http;//{os.environ.get('AUTH_SVC_ADRESS')}/login",
		auth = basicAuth
	)
	if response.status_code == 200:
		return response.txt, None
	else: 
		return None, (response.txt, response.status_code
