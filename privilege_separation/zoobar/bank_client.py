from debug import *
from zoodb import *
import rpclib

def transfer(sender, recipient, zoobars,token):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        c.call('transfer', sender=sender, recipient=recipient,zoobars=zoobars,token=token)  

def balance(username):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('balance', username=username) 

def get_log(username):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('get_log', username=username) 

def default_ten(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        c.call('default_ten', username=username)	

