import uuid

#
##--------------------------UTILISATEURS-----------------------------##
class User:
    def __init__(self, lname, fname, email):
        self.lname = lname
        self.fname = fname
        self.email = email

    def to_print(self):
        return str(self.fname) + str(self.lname) + str(self.email) + "\n"

    # Permet l'itération de l'élément
    def __iter__(self):
      yield self


##--------------------------ELECTEURS--------------------------------##
class Voter(User):
    def __init__(self, *args):
        ### Création d'un électeur depuis un utilisateur
        if type(args[0]) is User:
            self.__dict__ = args[0].__dict__.copy()
        else:
            super(Voter, self).__init__(*args)
        self.uuid = uuid.uuid4()

    def to_print(self):
        return str(self.fname) + " " + str(self.lname) + " " + str(self.email) + " " + str(self.uuid) + "\n"

    def __iter__(self):
      yield self


##-------------------------------------------------------------------##
class Admin(User):
    def __init__(self, *args):
        if type(args[0]) is User:
            self.__dict__ = args[0].__dict__.copy()
        else:
            super(Admin, self).__init__(*args)

    def to_print(self):
        return str(self.fname) + " " + str(self.lname) + " " + str(self.email) + "\n"

    def __iter__(self):
      yield self


##-------------------------------------------------------------------##
class Authority(User):
    def __init__(self, *args):
        if type(args[0]) is User:
            self.__dict__ = args[0].__dict__.copy()
        else:
            super(Authority, self).__init__(*args)

    def to_print(self):
        return str(self.fname) + " " + str(self.lname) + " " + str(self.email) + "\n"

    def __iter__(self):
      yield self

##--------------------------ELECTION---------------------------------##
class Question:
    class_counter = 1  # Compteur de questions

    def __init__(self, title):
        self.id = self.class_counter
        self.class_counter += 1
        self.title = title
        self.answers = []

    def add_answer(self, answer):
        self.answers.append(answer)

    def to_print(self):
        to_print = "Question " + str(self.id) + ": " + str(self.title) + "\n\t\t"
        i = 1
        for a in self.answers:
            to_print += str(i) + ": " + str(a) + "\n\t\t"
            i += 1
        return to_print

    def __iter__(self):
        yield self

##-------------------------------------------------------------------##
class Election:
    class_counter = 1  # Compteur d'élection pour en gérer plusieurs

    def __init__(self, admin, questions, authorities, voters):
        self.id = self.class_counter
        self.admin = admin
        self.questions = questions
        self.authorities = authorities
        self.voters = voters
        self.class_counter += 1

    def to_print_questions(self):
        to_print = ""
        for q in self.questions:
            to_print += q.to_print()
        return to_print + "\n"

    def to_print_authorities(self):
        to_print = ""
        for a in self.authorities:
          to_print += a.to_print()
        return to_print + "\n"

    def to_print_voters(self):
        to_print = ""
        for v in self.voters:
          to_print += v.to_print()
        return to_print + "\n"

    def to_print(self):
        return "Élection " + str(self.id) + "\nAdmin:\n\t" + self.admin.to_print() + "Question(s):\n\t" + self.to_print_questions() + "Dépouilleur(s):\n\t" + self.to_print_authorities() + "Électeurs:\n\t" + self.to_print_voters() + "\n"


# TESTS
user = User("Moisset", "Oscar", "oscar.moisset@utt.fr")
v = Voter(user)
a = Admin(user)
d = Authority("KUHN", "Valentin", "valentin.kuhn@utt.fr")

q = Question("Qui?")
q.add_answer("Oui")
q.add_answer("Non")

e = Election(a, q, d, v)

print(e.to_print())
