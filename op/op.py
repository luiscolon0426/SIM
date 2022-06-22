from email import message
from socket import timeout
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.garden.notification import Notification
import re
from pymongo import MongoClient
import plyer
Builder.load_file('op/op.kv')


class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        self.db = client.silverpos
        self.stocks = self.db.stocks
        self.cart = []
        self.qty = []
        self.total = 0.00

    def logout(self):
        self.parent.parent.current = 'scrn_si'
        
    def update_purchases(self):
        pname = self.ids.name_inp.text
        pqty = self.ids.qty_inp.text
        products_container = self.ids.products
        target_code = self.stocks.find_one({'product_name':pname})
        if target_code == None:
            pass
        else:
            details = BoxLayout(size_hint_y=None,height=30,pos_hint={'top': 1})
            products_container.add_widget(details)
            code = Label(text=target_code['product_code'],size_hint_x=.2,color=(.06,.45,.45,1))
            name = Label(text=pname,size_hint_x=.3,color=(.06,.45,.45,1))
            qty = Label(text=pqty,size_hint_x=.1,color=(.06,.45,.45,1))
            price = Label(text=str(target_code['product_price']),size_hint_x=.1,color=(.06,.45,.45,1))
            if int(pqty) <= int(target_code['in_stock']):
                details.add_widget(code)
                details.add_widget(name)
                details.add_widget(qty)
                details.add_widget(price)
                temp_qty = int(target_code['in_stock']) - int(pqty)
                temp_sold = int(target_code['sold']) + int(pqty)
                if temp_qty <= 5 and temp_qty > 0:
                    plyer.notification.notify(
                        title="Low stock",
                        message="Item low on stock, reorder soon",
                        timeout=5,
                    )
                elif temp_qty <= 0:
                    plyer.notification.notify(
                        title="Out of stock",
                        message="Item is out of stock",
                        timeout=5,
                    )
                self.stocks.update_one({'product_name':pname},{'$set':{'in_stock':temp_qty}})
                self.stocks.update_one({'product_name':pname},{'$set':{'sold':temp_sold}})
                rec_qty = int(qty.text)
                pprice = float(price.text) * int(pqty)
                pprice = round(pprice,2)
                rec_qty += int(qty.text)
                self.total += pprice
                purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t'+'$'+str(round(self.total,2))
                self.ids.cur_product.text = pname
                self.ids.cur_price.text = '$' + price.text
                preview = self.ids.receipt_preview
                prev_text = preview.text
                _prev = prev_text.find('`')
                if _prev:
                    prev_text = prev_text[:_prev]
                ptarget = -1
                for i,c in enumerate(self.cart):
                    if c == pname:
                        ptarget = i
                if ptarget >= 0:
                    expr = '%s\t\tx\d\t'%(pname)
                    rexpr = pname+'\t\tx'+str(rec_qty)+'\t'
                    nu_text = re.sub(expr,rexpr,prev_text)
                    preview.text = nu_text + purchase_total
                else:
                    self.cart.append(pname)
                    self.qty.append(1)
                    nu_preview = '\n'.join([prev_text,pname+'\t\tx'+pqty+'\t\t'+str(pprice),purchase_total])
                    preview.text = nu_preview
            else:
                Notification().open(
                    title="Error",
                    message="Error, not that many available",
                    timeout=5,
                )


class OperatorApp(App):
    def build(self):
        return OperatorWindow()


if __name__=="__main__":
    oa = OperatorApp()
    oa.run()