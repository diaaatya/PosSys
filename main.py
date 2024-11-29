import sys
from PyQt5.QtWidgets import QApplication , QWidget , QPushButton, QVBoxLayout , QGridLayout , QListWidget , QLabel

class PosApp (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("برنامج الكاشير")
        self.setGeometry(100, 100, 500, 500)

        #layouts
        self.main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.item_list = QListWidget(self)
        self.total_label = QLabel( "total : 0 . L.E", self)

        self.menu_items = [
            ("Burger", 5.00), ("Pizza", 8.00), ("Pasta", 7.00),
            ("Soda", 2.00), ("Salad", 4.00), ("Fries", 3.00),
            ("Ice Cream", 3.50), ("Coffee", 2.50), ("Tea", 1.50),
            ("Steak", 12.00), ("Soup", 4.50), ("Sandwich", 5.50)
        ]    

        for i ,(item,price) in enumerate(self.menu_items):
            button = QPushButton(f"{item}\n${price:.2f}",self)
            button.clicked.connect(lambda checked , item = item , price = price: self.add_item(item , price) )
            self.grid_layout.addWidget(button, i // 3, i % 3)  # 4x3 grid

        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(self.item_list)
        self.main_layout.addWidget(self.total_label)

        self.setLayout(self.main_layout)

        self.total_cost = 0 

    def add_item(self , item , price):
        self.item_list.addItem(f"{item} - {price:.2f} L.E")
        self.total_cost +=price
        self.total_label.setText(f"Total : {self.total_cost:.2f} L.E")


app = QApplication(sys.argv)
Window = PosApp()
Window.show()
sys.exit(app.exec_())
