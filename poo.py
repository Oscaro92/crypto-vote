import uuid

##--------------------------UTILISATEURS-----------------------------##
class User:
  def __init__(self, lname, fname, email):
    self.lname = lname
    self.fname = fname
    self.email = email

  def print(self):
    print("Utilisateur:", self.fname, self.lname, self.email)
##-------------------------------------------------------------------##
class Voter(User):
  def __init__(self, *args):
    ### Création d'un électeur depuis un utilisateur
    if type(args[0]) is User:
      self.__dict__ = args[0].__dict__.copy()
    else:
      super(Voter, self).__init__(*args[:2])
    self.uuid = uuid.uuid4()

  def from_user(self, user):
    return self(user.lname, user.fname, user.email)

  def print(self):
    print("Électeur:", self.fname, self.lname, self.email, self.uuid)
##-------------------------------------------------------------------##
class Admin(User):
  def __init__(self, lname, fname, email):
    User.__init__(self, lname, fname, email)

  def from_user(self, user):
    return self(user.fname, user.lname, user.email)

  def print(self):
    print("Administrateur:", self.fname, self.lname, self.email, self.uuid)
##-------------------------------------------------------------------##
class Authority(User):
  def __init__(self, lname, fname, email):
    User.__init__(self, lname, fname, email)

  def from_user(self, user):
    return self(user.fname, user.lname, user.email)

  def print(self):
    print("Autorité:", self.fname, self.lname, self.email, self.uuid)

##--------------------------ELECTION---------------------------------##
class Election:
  class_counter = 0 #Compteur d'élection pour en gérer plusieurs
  def __init__(self, questions, answers, authorities, voters):
    self.id = self.class_counter
    self.questions = questions
    self.answers = answers
    self.authorities = authorities
    self.voters = voters
    self.class_counter += 1





#TESTS
user = User("Moisset", "Oscar", "oscar.moisset@utt.fr")
v2 = Voter(user)

user.print()
v2.print()