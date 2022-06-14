from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        user = self.ids.usr_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        uname = user.text
        passw = pwd.text
        if uname == '' or passw == '':
            info.text = '[color=#FF0000]username and/or password required[/color]'
        elif uname == 'admin' and passw == 'admin':
            info.text = '[color=#00FF00]Logged In successfully!!![/color]'
        else:
            info.text = '[color=#FF0000]Invalid username and/or password[/color]'

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__ == "__main__":
    SigninApp().run()