'''
Sign in screen
'''
import hashlib
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from pymongo import MongoClient
Builder.load_file('signin/signin.kv')


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        super().__init__(**kwargs)

    def validate_user(self):
        '''
        comment
        '''
        client = MongoClient()
        db = client.sim
        users = db.users
        user = self.ids.usr_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        uname = user.text
        passw = pwd.text
        user.text = ''
        passw.text = ''
        if uname == '' or passw == '':
            info.text = '[color=#FF0000]username and/or password required[/color]'
        else:
            user = users.find_one({'user_name':uname})
            if user == None:
                info.text = '[color=#FF0000]Invalid username and/or password[/color]'
            else:
                passw = hashlib.sha256(passw.encode()).hexdigest()
                if passw == user['password']:
                    des = user['designation']
                    #info.text = '[color=#00FF00]Logged In successfully!!![/color]'
                    info.text = ''
                    self.parent.parent.parent.ids.scrn_op.children[0].ids.loggedin_user.text = uname
                    if des == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = 'scrn_op'
                else:
                    info.text = '[color=#FF0000]Invalid username and/or password[/color]'


class SigninApp(App):
    def build(self):
        '''
        comment
        '''
        return SigninWindow()


if __name__ == "__main__":
    '''
    run the app
    '''
    SigninApp().run()
