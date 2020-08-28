import datetime
import mysql.connector


class DataBase:

    def __init__(self, host, user_name, password, db):
        self.host = host
        self.user_name = user_name
        self.password = password
        self.db = db
        self.cursor = None
        #self.user = None
        self.users = {}
        self.plank_types = {}
        self.plank_log = {}
        self.load(self.host, self.user_name, self.password, self.db)

    def load(self, host, user_name, password, db):
        self.db = mysql.connector.connect(
            host=host,
            user=user_name,
            passwd=password,
            database=db
        )

        self.cursor = self.db.cursor()

# THIS FUNCTION CHECKS THAT THE USER IS IN THE DATABASE BEFORE QUERYING FOR THE USER AND RETURNS -1 OTHERWISE
    def check_user(self, email):
        print("Sending check_user query.")
        query = "SELECT email FROM users;"
        self.cursor.execute(query)
        temp_users = self.cursor.fetchall()

        for user in temp_users:
            if user[0] == email:
                return email
        return -1

# THIS FUNCTION QUERIES THE DATABASE FOR THE INFORMATION ON THE USER IF THEY ARE PRESENT AND RETURNS -1 OTHERWISE
    def get_user(self, email):
        if email.strip() in self.users:
            print("Email found in self.users!")
            return self.users[email]
        else:
            print("Sending get_user() query.")
            query = "SELECT * FROM users WHERE email = '{}';"
            exists = self.check_user(email)
            if exists != -1:
                self.cursor.execute(query.format(email))
                db_id, email, password, first_name, last_name, age, sex, date_joined = self.cursor.fetchone()
                self.users[email] = (db_id, password, first_name, last_name, age, sex, date_joined)
                return self.users[email]
            else:
                return -1
# WE NEED THIS INFORMATION BECAUSE WE NEED TO DISPLAY IT TO THE USER AND ALSO ADD IT TO A QUERY WHERE WE WILL ENTER
# PLANK INFORMATION FOR THIS PARTICULAR USER INTO THE DATABASE

    def add_user(self, email, password, first_name, last_name, age, sex):
        if self.check_user(email) == -1:
            print("Sending add_user query.")
            query = "INSERT INTO users (email, password, first_name, last_name, age, sex) " \
                    "VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"
            self.cursor.execute(query.format(email, password, first_name, last_name, age, sex))
            self.db.commit()
            return 1
        else:
            print("Email already exists.")
            return -1

    def validate(self, email, password):
        print("In validate()")
        if self.get_user(email) != -1:
            return self.users[email][1] == password
        else:
            return False

    def get_user_id(self, email):
        print("In get_user_id()")
        user = self.get_user(email)
        if user != -1:
            user_id, password, first_name, last_name, age, sex, date_joined = user
            return user_id
        else:
            return -1

    def get_all_plank_types(self):
        print("Submitting plank_types query.")
        query = "SELECT id, type FROM plank_types;"
        self.cursor.execute(query)
        self.plank_types = self.cursor.fetchall()
        print("Now I can see the types!")
        return self.plank_types

    def get_all_plank_names(self):
        print("In get_all_plank_names().")
        self.get_all_plank_types()
        plank_names = [str(t[1]) for t in self.plank_types]
        return plank_names

    def get_plank_id(self, plank_type):
        print("In get_plank_id()")
        print(plank_type)
        for t in self.plank_types:
            print(t[1])
            if t[1] == plank_type:
                return t[0]
        return -1

    def get_duration(self, minute, second):
        if minute == '':
            min = 0
        else:
            try:
                min = int(minute)
            except ValueError:
                min = "error"

        if second == '':
            sec = 0
        else:
            try:
                sec = int(second)
            except ValueError:
                sec = "error"

        if sec == "error" or min == "error":
            return -1
        elif sec > 0 and min > 0:
            return (min*60) + sec
        elif sec == 0 and min > 0:
            return min*60
        elif min == 0 and sec > 0:
            return sec
        else: # Both minute and second are 0, or are negative
            return -2

    def create_print_dur(self, minute, second):

        if minute == '':
            min = 0
        else:
            try:
                min = int(minute)
            except ValueError:
                min = "error"

        if second == '':
            sec = 0
        else:
            try:
                sec = int(second)
            except ValueError:
                sec = "error"

        s = "seconds" if sec > 1 else "second"
        m = "minutes" if min > 1 else "minute"

        if sec == "error" or min == "error":
            return -1
        elif sec > 0 and min > 0:
            phrase = "{} {} & {} {}"
            return phrase.format(minute, m, second, s)
        elif sec == 0 and min > 0:
            phrase = "{} {}"
            return phrase.format(minute, m)
        elif min == 0 and sec > 0:
            phrase = "{} {}"
            return phrase.format(second, s)
        else: # Both are equal to zero or are negative
            return -2

        

    def add_plank_instance(self, user_id, date, plank_id, duration, plank_type):
        query = "INSERT INTO plank_log (user_id, date, plank_type_id, duration)" \
               "VALUES ('{}', '{}', '{}', '{}')"
        self.cursor.execute(query.format(user_id, date, plank_id, duration))
        self.db.commit()
        #self.plank_log[user_id].add(date, plank_type, duration)
        #return self.plank_log[user_id]


    @staticmethod
    def get_date():
        print("In get_date()")
        return str(datetime.datetime.now()).split(" ")[0]


