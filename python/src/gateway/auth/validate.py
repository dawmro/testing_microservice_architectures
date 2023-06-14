import os, requests

# function to validate the token
def token(request):
	# check for authorization header in request
	if not "Authorization" in request.headers:
		return None, ("missing credentials", 401)
	
	token = request.headers["Authorization"]
	# check if token exists
	if not token:
		return None, ("missing credentials", 401)
	
	# if all good send post request via http to auth service
	response = requests.post(
		f"http;//{os.environ.get('AUTH_SVC_ADRESS')}/login",
		headers = {"Authorization": token},
	)
	# check repsonse
	if response.status_code == 200:
		return response.txt, None
	else: 
		return None, (response.txt, response.status_code)
	
