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

    # def get_all_users(self):
    #     query = "SELECT * FROM users;"
    #
    #     for line in self.file:
    #         email, password, name, created = line.strip().split(";")
    #         self.users[email] = (password, name, created)

# THIS FUNCTION CHECKS THAT THE USER IS IN THE DATABASE BEFORE QUERYING FOR THE USER AND RETURNS -1 OTHERWISE
    def check_user(self, email):
        query = "SELECT email FROM users;"
        self.cursor.execute(query)
        temp_users = self.cursor.fetchall()

        for user in temp_users:
            if user[0] == email:
                return email
        return -1

# THIS FUNCTION QUERIES THE DATABASE FOR THE INFORMATION ON THE USER IF THEY ARE PRESENT AND RETURNS -1 OTHERWISE
    def get_user(self, email):
        # if email in self.users:
        #     return self.users[email]
        #else:
        query = "SELECT * FROM users WHERE email = '{}';"
        #print(query)
        exists = self.check_user(email)
        if exists != -1:
            self.cursor.execute(query.format(email))
            db_id, email, user_name, first_name, last_name, age, sex, date_joined = self.cursor.fetchone()
            self.users[email] = (db_id, user_name, first_name, last_name, age, sex, date_joined)
            return self.users[email]
        else:
            return -1
# WE NEED THIS INFORMATION BECAUSE WE NEED TO DISPLAY IT TO THE USER AND ALSO ADD IT TO A QUERY WHERE WE WILL ENTER
# PLANK INFORMATION FOR THIS PARTICULAR USER INTO THE DATABASE

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email already exists.")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][1] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";"  + self.users[user][1] + ";" + self.users[user][2] + "\n")


    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


