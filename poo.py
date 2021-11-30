import uuid

class Voter:
  def __init__(self, lname, fname, email, uuid):
    self.lname = lname
    self.fname = fname
    self.email = email
    self.uuid = uuid

v1 = Voter("Moisset", "Oscar", "oscar.moisset@utt.fr", str(uuid.uuid4()))

print(v1.email)