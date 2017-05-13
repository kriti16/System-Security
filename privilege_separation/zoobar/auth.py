from zoodb import *
from debug import *

import hashlib
import random
import bank_client
from base64 import b64encode
# Ref: Stack overflow
from os import urandom
import pbkdf2

def newtoken(db, person):
    hashinput = "%s%.10f" % (person.password, random.random())
    person.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return person.token

def login(username, password):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if not person:
        return None
    if person.password == pbkdf2.PBKDF2(password,person.salt).hexread(32):
        return newtoken(db, person)
    else:
        return None

def register(username, password):
    db = person_setup()
    person = db.query(Person).get(username)
    if person:
        return None
    newperson = Person()
    newperson.username = username
    db.add(newperson)
    db.commit()

    salt = b64encode(urandom(128)).decode('utf-8')
    new_password = pbkdf2.PBKDF2(password,salt).hexread(32)

    creddb = cred_setup()
    person = creddb.query(Cred).get(username)
    if person:
        return None
    credperson = Cred()
    credperson.username = username
    credperson.password = new_password
    credperson.salt = salt
    creddb.add(credperson)
    creddb.commit()

    bank_client.default_ten(username)
    return newtoken(creddb, credperson)

def check_token(username, token):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if person and person.token == token:
        return True
    else:
        return False

