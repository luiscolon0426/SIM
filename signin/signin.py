"""
Sign in page:
Can log in as an Operator or as an Administrator
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from pymongo import MongoClient
import hashlib
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
Builder.load_file('signin/signin.kv')


class SigninWindow(BoxLayout):
    '''Sign in window'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        '''Validates the user in the db'''
        client = MongoClient("mongodb+srv://sim:Holberton@sim.cjkvehd.mongodb.net/?retryWrites=true&w=majority")
        db = client.silverpos
        users = db.users
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        uname = user.text
        passw = pwd.text
        user.text = ''
        pwd.text = ''
        if uname == '' or passw == '':
            info.text = '[color=#FF0000]username and/ or password required[/color]'
        else:
            user = users.find_one({'user_name':uname})
            if user == None:
                info.text = '[color=#FF0000]Invalid Username and/or Password[/color]'
            else:
                passw = hashlib.sha256(passw.encode()).hexdigest()
                if passw == user['password']:
                    des = user['designation']
                    info.text = ''
                    self.parent.parent.parent\
                        .ids.scrn_op.children[0]\
                            .ids.loggedin_user.text = uname
                    if des == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = 'scrn_op'
                else:
                    info.text = '[color=#FF0000]Invalid Username and/or Password[/color]'


class SigninApp(App):
    '''Builder of app'''
    def build(self):
        return SigninWindow()


if __name__=="__main__":
    sa = SigninApp()
    sa.run()