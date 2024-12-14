
import sys
from PyQt5.QtWidgets import QApplication, QWidget , QVBoxLayout , QGridLayout , QListWidget , QLabel , QPushButton , QHBoxLayout , QInputDialog , QMessageBox
from PyQt5.QtCore import QDateTime,Qt
from PyQt5.QtGui import QColor , QPixmap


class PosApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code WZ D POS")
        self.setGeometry(100,100,1280,720)
        self.setFixedSize(1280,720)

        self.main_layout = QHBoxLayout()
        #layout
        self.left_layout = QVBoxLayout()
        self.logo = QLabel(self)
        pixmap = QPixmap("logo.png")
        resized_pixmap = pixmap.scaled(200, 200)  # Width: 200, Height: 200
        self.logo.setPixmap(resized_pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.header_layout = QVBoxLayout()
        self.resturant_label = QLabel("code with D Cafe" , self)
        self.resturant_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; background-color: #4CAF50; padding: 10px;")
        self.resturant_label.setAlignment(Qt.AlignCenter)
        self.date_time_label = QLabel(self)
        self.update_date_time() 
        self.date_time_label.setStyleSheet("font-size: 18px; color: #ffffff; background-color: #4CAF50; padding: 5px;")
        self.date_time_label.setAlignment(Qt.AlignCenter)
        self.header_layout.addWidget(self.logo)
        self.header_layout.addWidget(self.resturant_label)
        self.header_layout.addWidget(self.date_time_label)

        self.grid_layout = QGridLayout()
  
        self.menu_items = [
            ("برجر", 5.00), ("بيتزا", 8.00), ("مكرونه", 7.00),
            ("كولا", 2.00), ("سلطه", 4.00), ("فريز", 3.00),
            ("حلويات", 3.50), ("قهوة", 2.50), ("شاي", 1.50),
            ("مشويات", 12.00), ("شوربه", 4.50), ("مقبلات", 5.50)
        ]    

        for i , (item, price) in enumerate(self.menu_items):
            button = QPushButton(f"{item}\n{price:.2f} L.E", self)
            button.clicked.connect(lambda checked, item = item , price=price: self.add_item(item,price))
            self.grid_layout.addWidget(button , i//3 , i%3)
        
        self.bottom_layout = QVBoxLayout()
        self.new_check_button = QPushButton("new check" , self)
        self.clear_check_button = QPushButton("clear check" , self)
        self.exit_button = QPushButton("Exit" , self)
        self.new_check_button.setStyleSheet("font-size: 18px; background-color: #4CAF50; color: #ffffff; padding: 15px; margin: 5px;")
        self.clear_check_button.setStyleSheet("font-size: 18px; background-color: #FF9800; color: #ffffff; padding: 15px; margin: 5px;")
        self.exit_button.setStyleSheet("font-size: 18px; background-color: #f44336; color: #ffffff; padding: 15px; margin: 5px;")

        self.new_check_button.clicked.connect(self.new_check)
        self.clear_check_button.clicked.connect(self.clear_check)
        self.exit_button.clicked.connect(self.close)
        
        self.bottom_layout.addWidget(self.new_check_button)
        self.bottom_layout.addWidget(self.clear_check_button)
        self.bottom_layout.addWidget(self.exit_button)

        self.left_layout.addLayout(self.header_layout)
        self.left_layout.addLayout(self.grid_layout)
        self.left_layout.addLayout(self.bottom_layout)

        self.right_layout = QVBoxLayout()
        self.item_list = QListWidget(self)
        self.item_list.setStyleSheet("font-size : 16px; background-color:#f1f1f1; padding:10px;")
        self.total_label = QLabel("total: 0 " , self) 
        self.total_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; padding: 10px;")
        self.item_list.setFixedWidth(300)
        self.right_layout.addWidget(self.item_list)
        self.right_layout.addWidget(self.total_label)
       

        self.main_layout.addLayout(self.left_layout,1)
        self.main_layout.addLayout(self.right_layout,2)

        self.setLayout(self.main_layout)

        self.total_cost = 0

        self.item_list.itemClicked.connect(self.confirm_delete)

    def add_item(self , item , price):
        quantity , ok  = QInputDialog.getInt(self, "Quantity" , f"Entrt quantity for {item}:" , 1 , 1 , 100 , 1)

        if ok:
            total_price = price * quantity

            item_text = f"{item} X {quantity} - {total_price:.2f} - L.E"
            self.item_list.addItem(item_text)

            self.total_cost += total_price
            self.total_label.setText(f"total : {self.total_cost:.2f} L.E")

    
    def update_date_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.date_time_label.setText(f"Date & time :{current_time}")

    def new_check(self):
        self.item_list.clear()
        self.total_cost = 0 
        self.total_label.setText("total : 0")
    def clear_check(self):
        self.item_list.clear()
        self.total_cost = 0 
        self.total_label.setText("total : 0")
    def confirm_delete(self,item):
        item_text = item.text()
        reply = QMessageBox.question(self, "Delete Item !!" , f"Are you sure you want to delete {item_text} ? ",
                                     QMessageBox.Yes |QMessageBox.No , QMessageBox.No)
        if reply == QMessageBox.Yes:
            item_price = self.get_price(item_text)
            self.item_list.takeItem(self.item_list.row(item))
            self.total_cost-=item_price
            self.total_label.setText(f'Total: {self.total_cost:.2f} L.E')
    def get_price(self, text):
        price = text.split("-") 
        return float(price[1]) if len(price) > 1 else 0.0

app= QApplication(sys.argv)
window = PosApp()
window.show()
sys.exit(app.exec_())
