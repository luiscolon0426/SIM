from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from admin.admin import AdminWindow
from signin.signin import SigninWindow
from op.op import OpWindow


class MainWindow(BoxLayout):
    admin_widget = AdminWindow()
    signin_widget = SigninWindow()
    op_widget = OpWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.op_widget)


class MainApp(App):
    def build(self):
        return MainWindow()


if __name__=='__main__':
    MainApp().run()