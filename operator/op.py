from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import re


class OpWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = []
        self.qty = []
        self.total = 0.00

    def update_purchases(self):
        pname = self.ids.code_input.text
        products_container = self.ids.products
        if pname == 'Product One' or pname == 'Product Two':
            details = BoxLayout(size_hint_y=None, height=30,
                                pos_hint={'top': 1})
            products_container.add_widget(details)
            code = Label(text='1', size_hint_x=.2, color=(0, 0, 0, 1))
            name = Label(text=pname, size_hint_x=.3,
                         color=(0, 0, 0, 1))
            qty = Label(text='1', size_hint_x=.1, color=(0, 0, 0, 1))
            total = Label(text='0.00', size_hint_x=.2,
                          color=(0, 0, 0, 1))
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(total)
            # Update Preview

            pprice = 1.00
            pqty = str(1)
            self.total += pprice
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t'+str(self.total)
            self.ids.cur_product.text = pname
            self.ids.cur_price.text = str(pprice)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]
            ptarget = -1
            for i, c in enumerate(self.cart):
                if c == pname:
                    ptarget = i
            if ptarget >= 0:
                pqty = self.qty[ptarget]+1
                self.qty[ptarget] = pqty
                expr = '%s\t\tx\d\t' % (pname)
                rexpr = pname+'\t\tx'+str(pqty)+'\t'
                nu_text = re.sub(expr, rexpr, prev_text)
                preview.text = nu_text + purchase_total
            else:
                self.cart.append(pname)
                self.qty.append(1)
                nu_preview = '\n'.join(
                    [prev_text, pname+'\t\tx'+pqty+'\t\t'+str(pprice), purchase_total])
                preview.text = nu_preview


class OpApp(App):
    def build(self):
        return OpWindow()


if __name__ == "__main__":
    OpApp().run()
