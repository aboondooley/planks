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
    nameKV = ObjectProperty(None)
    emailKV = ObjectProperty(None)
    passwordKV = ObjectProperty(None)

    def submit(self):
        if self.nameKV.text != "" and self.emailKV.text != "" and self.emailKV.text.count("@") == 1 and self.emailKV.text.count(".")>0:
            if self.passwordKV.text != "":
                db.add_user(self.emailKV.text, self.passwordKV.text, self.nameKV.text)

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
        self.emailKV.text = ""
        self.passwordKV.text = ""
        self.nameKV.text = ""


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

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.nameKV.text = "Account Name: " + name
        self.emailKV.text = "Email: " + self.current
        self.createdKV.text = "Created On: " + created


class EnterPlankWindow(Screen):
    nameKV = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self):
        #password, name, created = db.get_user(self.current)
        self.nameKV.text = "Account Name: " + self.current



class WindowManager(ScreenManager):
    pass


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
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"), EnterPlankWindow(name="plank")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()