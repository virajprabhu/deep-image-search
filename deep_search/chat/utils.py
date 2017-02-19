from channels import Group
import json

def log_to_terminal(socketid, message):
	print message
	Group(socketid).send({"text": json.dumps(message)})