## Notes:
# name = ObjectPropery(None) # name needs to match what is on the left side in the kv file

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase


class CreateAccountWindow(Screen):
    firstNameKV = ObjectProperty(None)
    lastNameKV = ObjectProperty(None)
    sexKV = ObjectProperty(None)
    ageKV = ObjectProperty(None)
    emailKV = ObjectProperty(None)
    passwordKV = ObjectProperty(None)

    def submit(self):
        if self.firstNameKV.text != "" and self.lastNameKV.text != "" and self.emailKV.text != "" and self.emailKV.text.count("@") == 1 and self.emailKV.text.count(".")>0:
            if self.passwordKV.text != "":
                result = db.add_user(self.emailKV.text, self.passwordKV.text, self.nameKV.text)
                if result == -1:
                    userExists()
                else:
                    self.reset()
                    sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.firstNameKV.text = ""
        self.lastNameKV.text = ""
        self.sexKV.text = ""
        self.ageKV.text = ""
        self.emailKV.text = ""
        self.passwordKV.text = ""


class LoginWindow(Screen):
    emailKV = ObjectProperty(None)
    passwordKV = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.emailKV.text, self.passwordKV.text):
            MainWindow.current = self.emailKV.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.emailKV.text = ""
        self.passwordKV.text = ""


class MainWindow(Screen):
    nameKV = ObjectProperty(None)
    createdKV = ObjectProperty(None)
    emailKV = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def addPlankBtn(self):
        EnterPlankWindow.current = self.current
        sm.current = "plank"

    def on_enter(self, *args):
        db_id, user_name, first_name, last_name, age, sex, date_joined = db.get_user(self.current)
        self.nameKV.text = "Account Name: " + first_name + " " + last_name
        self.emailKV.text = "Email: " + self.current
        self.createdKV.text = "Created On: " + date_joined.strftime("%m/%d/%Y")


class EnterPlankWindow(Screen):
    nameKV = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        db_id, user_name, first_name, last_name, age, sex, date_joined = db.get_user(self.current)
        self.nameKV.text = "Account Name: " + first_name + " " + last_name


class WindowManager(ScreenManager):
    pass

def userExists():
    pop = Popup(title="Invalid New User",
                content=Label(text="User already exists in the database. Please log in."),
                size_hint=(None, None),
                size=(400, 400))

def invalidLogin():
    pop = Popup(title="Invalid Login",
                content=Label(text="Invalid username or password."),
                size_hint=(None, None),
                size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title="Invalid Form",
                content=Label(text="Please fill all inputs with valid information."),
                size_hint=(None, None),
                size=(400, 400))
    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase(host="alieboonvm.lan", user_name="admin", password="plankdb", db="plankdb")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"), EnterPlankWindow(name="plank")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

#row_nums = NumericProperty(0.1)

class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()