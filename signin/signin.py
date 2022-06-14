'''
Sign in screen
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        super().__init__(**kwargs)

    def validate_user(self):
        '''
        Validates if the user exists or not
        '''
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
        '''
        Build the app
        '''
        return SigninWindow()


if __name__ == "__main__":
    '''
    Run the app
    '''
    SigninApp().run()