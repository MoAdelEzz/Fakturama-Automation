from src.models.order import Order, OrderItem
from src.models.product import Product
from src.ui.window import FakturamaWindow
import pyautogui


class OrderCreationWorkflow:
    def __init__(
        self,
        window: FakturamaWindow,
        order: Order
    ):
        self.window = window
        self.order = order
        
    def open_form(self):
        isOpen, _ = self.window.is_tab_opened("New Order")
        if isOpen:
            return
        
        self.window.click_button(button_name="Create: New Order")
        
    def getOrderNo(self):
        [number_field] = self.window.get_fields(label_name="No.", count=1)
    
        value_pattern = number_field.GetValuePattern()

        if value_pattern is None:
            raise RuntimeError("Could not get value pattern for order number field")

        return value_pattern.Value
        
    def resolveNetGrossComboBox(self, date_control):
        parent = date_control.GetParentControl()
        siblings = parent.GetParentControl().GetChildren()
        return siblings[-1]
        
    def populateGeneralInfo(self):     
        [date_target] = self.window.get_fields(
            label_name="Date",
            count=1
        )
        
        date_parts = [
            f"{self.order.order_date.day:02d}",
            f"{self.order.order_date.month:02d}",
            self.order.order_date.year,
        ]
        
        for value in date_parts:
            date_target.SendKeys(str(value))
            
        grossNetComboBox = self.resolveNetGrossComboBox(date_target)
        self.window.edit_combobox_node(grossNetComboBox, "Net")
        self.window.edit_text_field(
            field_name="Cust.Ref.",
            value=self.order.external_reference
        )
     
    def populateInvoiceAddress(self):
        addressesText = self.window.element.TextControl(
            Name="Addresses",
            searchDepth=30,
        )
        siblings = addressesText.GetParentControl().GetChildren()
        selectAddressTrigger = siblings[1]
        selectAddressTrigger.Click()
        
        dialog = self.window.element.WindowControl(
            Name="Select the address",
            searchDepth=30
        )
        
        searchLabel = dialog.TextControl(
            Name="Search:"
        )
        
        searchGroup = searchLabel.GetParentControl()
        
        searchField = searchGroup.EditControl(Name="")
        searchField.SendKeys("{CTRL}A")
        searchField.SendKeys(
            f"{self.order.debtor.first_name} {self.order.debtor.last_name} { self.order.debtor.company } { self.order.debtor.zip_code } {self.order.debtor.city}"
        )
        
        searchRow = searchGroup.GetParentControl()
        bothRows = searchRow.GetParentControl().GetChildren()
        table = bothRows[1]
        
        rowHeight = 20
        startOffset = 10
        
        table.Click(
            ratioX=0.25,
            y=startOffset + rowHeight
        )
        
        self.window.click_button("OK")
    
    def modifyProductDetails(self, product: OrderItem, index):
        numText = self.window.element.TextControl(
            Name="No.",
            searchDepth=30
        )
        
        table = numText.GetParentControl().GetChildren()[-1]
        
        table.Click(x=75, y=12 + (index + 1) * 20)
        self.window.element.SendKeys(f"{product.quantity}")
        self.window.element.SendKeys("{ENTER}")
        
        width = 100
        
        table.Click(x=75+width*7, y=12 + (index + 1) * 20)
        self.window.element.SendKeys(f"{product.quantity}")
        self.window.element.SendKeys("{ENTER}")
        
    
    def populateProductDetails(self):
        itemsText = self.window.element.TextControl(
            Name="Items",
            searchDepth=30,
        )
        siblings = itemsText.GetParentControl().GetChildren()
        selectProduct = siblings[1]
        
        for index, item in enumerate(self.order.items):
            selectProduct.Click()
            
            dialog = self.window.element.WindowControl(
                Name="Select a product",
                searchDepth=30
            )
            
            searchLabel = dialog.TextControl(
                Name="Search:"
            )
            
            searchGroup = searchLabel.GetParentControl()
            
            searchField = searchGroup.EditControl(Name="")
            searchField.SendKeys("{CTRL}A")
            searchField.SendKeys(
               f"{item.product.sku}"
            )
            
            searchRow = searchGroup.GetParentControl()
            
            if searchRow is None:
                self.modifyProductDetails(item, index)
                continue
            
            # Ambiguity defaults to the first row
            bothRows = searchRow.GetParentControl().GetChildren()
            table = bothRows[1]
            
            rowHeight = 20
            startOffset = 10
            
            table.Click(
                ratioX=0.25,
                y=startOffset + rowHeight
            )
            
            self.window.click_button("OK")
            self.modifyProductDetails(item, index)
    
    
    def populateInvoice(self):
        if self.order.discount is not None:
            self.window.edit_text_field(
                field_name="Discount",
                value=f"{self.order.discount}"
            )

    def run(self):
        self.window.focus()
        self.open_form()
        orderNumber = self.getOrderNo()
        self.populateGeneralInfo()
        self.populateInvoice()
        
        self.populateInvoiceAddress()
        self.populateProductDetails()
        
        self.window.save()
        
        return orderNumber