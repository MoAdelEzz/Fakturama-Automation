from src.models.order import Order, OrderItem
from src.models.product import Product
from src.ui.window import FakturamaWindow
import pyautogui


class InvoiceCreationWorkflow:
    def __init__(
        self,
        window: FakturamaWindow,
        order: Order,
        OID: str
    ):
        self.window = window
        self.order = order
        self.OID = OID
        
    def open_form(self):
        isOpen, tabControl = self.window.is_tab_opened(self.OID)
        
        if not isOpen or tabControl is None:
            raise RuntimeError("Order Form Is Not Opened")
        
        trigger = tabControl.ButtonControl(
            Name="Invoice",
            searchDepth=30
        )
        
        trigger.Click()
        
        isOpen, _ = self.window.is_tab_opened("New Invoice")
        
        if not isOpen:
            raise RuntimeError("OPEN_NEW_INVOICE_FAILED")
    
    def fill_payment(self):
        if self.order.isPaid and self.order.paid_at is not None:
            checkbox = self.window.element.CheckBoxControl(
                Name='paid',
                searchDepth=30
            )
            
            checkbox.Click()
            
            [date_target] = self.window.get_fields(
                label_name="at",
                count=1
            )
            
            date_parts = [
                f"{self.order.paid_at.day:02d}",
                f"{self.order.paid_at.month:02d}",
                self.order.paid_at.year,
            ]
            
            for value in date_parts:
                date_target.SendKeys(str(value))
    

    def run(self):
        self.window.focus()
        self.open_form()
        self.fill_payment()
        self.window.save()
        self.window.close_active_tab()