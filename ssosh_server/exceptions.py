class LoginFailed(Exception):
	pass

class LoginRedirectLoop(LoginFailed):
    pass