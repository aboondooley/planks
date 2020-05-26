## Notes:
# name = ObjectPropery(None) # name needs to match what is on the left side in the kv file
import datetime
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from database import DataBase


class CreateAccountWindow(Screen):
    firstNameKV = ObjectProperty(None)
    lastNameKV = ObjectProperty(None)
    maleSexKV = ObjectProperty(None)
    femaleSexKV = ObjectProperty(None)
    otherSexKV = ObjectProperty(None)
    ageKV = ObjectProperty(None)
    emailKV = ObjectProperty(None)
    passwordKV = ObjectProperty(None)

    def submit(self):
        if self.firstNameKV.text != "" and self.lastNameKV.text != "" and self.emailKV.text != "" and self.emailKV.text.count("@") == 1 and self.emailKV.text.count(".")>0:
            if self.passwordKV.text != "":
                sex = self.get_sex()
                result = db.add_user(self.emailKV.text, self.passwordKV.text, self.firstNameKV.text, self.lastNameKV.text, self.ageKV.text, sex)
                if result == -1:
                    userExists()
                else:
                    self.reset()
                    sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def get_sex(self):
        if self.maleSexKV.active:
            sex = "M"
        elif self.femaleSexKV.active:
            sex = "F"
        elif self.otherSexKV.active:
            sex = "O"
        else:
            sex = ""
        return sex

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
    dateKV = ObjectProperty(None)
    durMinKV = ObjectProperty(None)
    durSecKV = ObjectProperty(None)
    plank_names = ListProperty([])
    plankNameKV = ObjectProperty(None)
    current = ""

    def get_date(self):
        return str(datetime.datetime.now()).split(" ")[0]

    def backMain(self):
        self.reset()
        sm.current = "main"

    def on_enter(self):
        self.reset()
        self.plank_names = db.get_all_plank_names()

    def reset(self):
        self.dateKV.text = self.get_date()
        self.durMinKV.text = ""
        self.durSecKV.text = ""

    def submit(self):
        duration = db.get_duration(self.durMinKV.text, self.durSecKV.text)
        user_id = db.get_user_id(self.current)
        plank_id = db.get_plank_id(self.plankNameKV.text)
        session = []
        if duration > 0 and plank_id != -1 and self.dateKV.text != "":
            session = db.add_plank_instance(user_id, self.dateKV.text, plank_id, duration, self.plankNameKV.text)
        elif duration == -1:
            invalidDurationString()
        elif duration == -2:
            invalidDurationNegative()
        elif self.plankNameKV.text == "":
            print("self.plankNameKV.text == ''")
            print(self.plankNameKV.text)
            print(plank_id)
            print(user_id)
            print(duration)
            print(self.dateKV.text)
        else:
            print("In else statement")
            print(duration)
            print(plank_id)
            print(user_id)
            print(self.plankNameKV.text)
            print(self.dateKV.text)





class WindowManager(ScreenManager):
    pass


def invalidDurationNegative():
    pop = Popup(title="Invalid Duration Value",
                content=Label(text="At least one of your duration values is negative or zero. Please try again."),
                size_hint=(None, None),
                size=(400,400))
    pop.open()



def invalidDurationString():
    pop = Popup(title="Invalid Duration Value",
                content=Label(text="At least one of your duration values is not a number. Please try again."),
                size_hint=(None, None),
                size=(400,400))

def userExists():
    pop = Popup(title="Invalid New Email",
                content=Label(text="User with this email already exists in the database. Please log in."),
                size_hint=(None, None),
                size=(400, 400))
    pop.open()

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