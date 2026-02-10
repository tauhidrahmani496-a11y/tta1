import sys
import os
import sqlite3
import zipfile
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

# ==========================================
# কনফিগারেশন
# ==========================================
if getattr(sys, 'frozen', False):
    folder_path = os.path.dirname(sys.executable)
else:
    folder_path = os.path.dirname(os.path.abspath(__file__))

db_name = "dhaka13.db"
zip_name = "dhaka13.zip"
font_name = "font.ttf"

# ==========================================
# 🔥 অটোমেটিক জিপ এক্সট্র্যাক্টর 🔥
# ==========================================
# অ্যাপ চালুর সময় যদি ডাটাবেজ না পায়, কিন্তু জিপ ফাইল পায়, তবে সে আনজিপ করে নেবে
db_full_path = os.path.join(folder_path, db_name)
zip_full_path = os.path.join(folder_path, zip_name)

if not os.path.exists(db_full_path):
    if os.path.exists(zip_full_path):
        try:
            print("Extracting database...")
            with zipfile.ZipFile(zip_full_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
            print("Database extracted successfully!")
        except Exception as e:
            print(f"Error extracting zip: {e}")

# বাংলা টু ইংরেজি ম্যাপ
bangla_to_eng_map = {
    "২৮": "28", "২৯": "29", "৩০": "30",
    "৩১": "31", "৩২": "32", "৩৩": "33", "৩৪": "34"
}

# ফন্ট লোডার
def load_custom_font():
    font_path = os.path.join(folder_path, font_name)
    if os.path.exists(font_path):
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return families[0]
    return "Nirmala UI"

APP_FONT_FAMILY = load_custom_font()

# ফাইল লোড ফাংশন
def load_ui_file(filename, self):
    full_path = os.path.join(folder_path, filename)
    if os.path.exists(full_path):
        try:
            uic.loadUi(full_path, self)
        except Exception as e:
            QMessageBox.critical(self, "Design Error", f"Error loading {filename}:\n{e}")
            sys.exit(1) 
    else:
        QMessageBox.warning(self, "File Missing", f"'{filename}' ফাইলটি পাওয়া যাচ্ছে না!\nLocation: {folder_path}")
        sys.exit(1)

def get_table_name(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return tables[0][0] if tables else None

def clean_header_text(text):
    if "(" in text and ")" in text:
        return text.split("(")[-1].replace(")", "").strip()
    return text

# ডিটেইল উইন্ডো
class DetailWindow(QtWidgets.QDialog):
    def __init__(self, data_dict):
        super().__init__()
        self.setWindowTitle("বিস্তারিত তথ্য")
        self.resize(400, 600) 
        self.setStyleSheet("background-color: #f0f8ff;") 

        layout = QtWidgets.QVBoxLayout()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)

        title_font = QtGui.QFont(APP_FONT_FAMILY, 12)
        title_font.setBold(True)
        value_font = QtGui.QFont(APP_FONT_FAMILY, 14)
        
        for key, value in data_dict.items():
            label_title = QtWidgets.QLabel(f"{key}:")
            label_title.setFont(title_font)
            label_title.setStyleSheet("color: #2c3e50; margin-top: 15px;")
            label_value = QtWidgets.QLabel(f"{value}")
            label_value.setFont(value_font)
            label_value.setStyleSheet("color: #000000; padding: 5px; border-bottom: 2px solid #bdc3c7;")
            label_value.setWordWrap(True)
            label_value.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            content_layout.addWidget(label_title)
            content_layout.addWidget(label_value)
            
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        close_btn = QtWidgets.QPushButton("বন্ধ করুন")
        close_btn.setFont(title_font)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(close_btn)
        self.setLayout(layout)

# ২য় উইন্ডো
class WindowTwo(QtWidgets.QDialog):
    def __init__(self):
        super(WindowTwo, self).__init__()
        load_ui_file('Dhaka13_2.ui', self)
        self.setFixedSize(450, 800)

        try:
            old_box = self.findChild(QtWidgets.QWidget, "lineEdit")
            if old_box:
                geom = old_box.geometry()
                parent = old_box.parent()
                old_box.setParent(None)
                old_box.deleteLater()
                
                self.lineEdit = QtWidgets.QLineEdit(parent)
                self.lineEdit.setGeometry(geom)
                self.lineEdit.setObjectName("lineEdit")
                self.lineEdit.setFont(QtGui.QFont(APP_FONT_FAMILY, 12))
                self.lineEdit.setPlaceholderText("হোল্ডিং নাম্বার লিখুন...")
                self.lineEdit.setAttribute(QtCore.Qt.WidgetAttribute.WA_InputMethodEnabled, False)
                self.lineEdit.show()
        except: pass

        try: self.lb1.setFont(QtGui.QFont(APP_FONT_FAMILY, 16, QtGui.QFont.Weight.Bold))
        except: pass

        try:
            current_y = self.tableWidget.y()
            current_x = self.tableWidget.x()
            new_height = 800 - current_y - 20 
            self.tableWidget.setGeometry(current_x, current_y, 430, new_height)
            self.tableWidget.setFont(QtGui.QFont(APP_FONT_FAMILY, 10))
        except: pass

        self.selected_ward = None
        try: self.btn_back.clicked.connect(self.close)
        except: pass
        try: self.pushButton.clicked.connect(self.search_data)
        except: pass
        try:
            try: self.listWidget.itemClicked.disconnect()
            except: pass
            self.listWidget.itemClicked.connect(self.handle_ward_click)
            self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
            self.listWidget.setFont(QtGui.QFont(APP_FONT_FAMILY, 11))
        except: pass
        try: 
            self.tableWidget.cellClicked.connect(self.show_details)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        except: pass

    def handle_ward_click(self, item):
        ward_text = item.text().strip()
        eng_ward = None
        for bangla, eng in bangla_to_eng_map.items():
            if bangla in ward_text:
                eng_ward = eng
                break
        if eng_ward:
            self.selected_ward = eng_ward
        else:
            self.selected_ward = ward_text

    def search_data(self):
        if not self.selected_ward:
            if self.listWidget.currentItem():
                self.handle_ward_click(self.listWidget.currentItem())
            else:
                QMessageBox.warning(self, "Warning", "ওয়ার্ড সিলেক্ট করুন।")
                return
        try: holding_no = self.lineEdit.text().strip()
        except: return
        if not holding_no:
            QMessageBox.warning(self, "Warning", "হোল্ডিং নাম্বার লিখুন।")
            return
        
        # ডাটাবেজ কানেকশন (এখন জিপ থেকে বের করা ডাটাবেজ ধরবে)
        db_path = os.path.join(folder_path, db_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            table_name = get_table_name(cursor)
            query = f"SELECT * FROM {table_name} WHERE `Ward No.(ওয়ার্ড নং)` = ? AND `Address (ঠিকানা)` LIKE ?"
            cursor.execute(query, (self.selected_ward, f"%{holding_no}%"))
            rows = cursor.fetchall()
            col_names = [d[0] for d in cursor.description]
            self.populate_table(rows, col_names)
            conn.close()
            if not rows: QMessageBox.warning(self, "Not Found", "তথ্য পাওয়া যায়নি।")
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def populate_table(self, rows, columns):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for r, row_data in enumerate(rows):
            self.tableWidget.insertRow(r)
            for c, data in enumerate(row_data):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(data)))

    def show_details(self, r, c):
        cols = self.tableWidget.columnCount()
        data_dict = {}
        for i in range(cols):
            raw_header = self.tableWidget.horizontalHeaderItem(i).text()
            clean_header = clean_header_text(raw_header)
            value = self.tableWidget.item(r, i).text()
            data_dict[clean_header] = value
        DetailWindow(data_dict).exec()

# ৩য় উইন্ডো
class WindowThree(QtWidgets.QDialog):
    def __init__(self):
        super(WindowThree, self).__init__()
        load_ui_file('Dhaka13_3.ui', self)
        self.setFixedSize(450, 800)
        
        try: self.lb1.setFont(QtGui.QFont(APP_FONT_FAMILY, 16, QtGui.QFont.Weight.Bold))
        except: pass
        try:
            current_y = self.tableWidget.y()
            current_x = self.tableWidget.x()
            new_height = 800 - current_y - 20 
            self.tableWidget.setGeometry(current_x, current_y, 430, new_height)
            self.tableWidget.setFont(QtGui.QFont(APP_FONT_FAMILY, 10))
        except: pass
        self.selected_ward = None
        try: self.btn_back.clicked.connect(self.close)
        except: pass
        try: 
            self.listWidget.itemClicked.connect(self.set_ward)
            self.listWidget.setFont(QtGui.QFont(APP_FONT_FAMILY, 11))
        except: pass
        try: self.pushButton.clicked.connect(self.search_data)
        except: pass
        try: 
            self.tableWidget.cellClicked.connect(self.show_details)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        except: pass

    def set_ward(self, item):
        ward_text = item.text().strip()
        for bangla, eng in bangla_to_eng_map.items():
            if bangla in ward_text:
                self.selected_ward = eng
                QMessageBox.information(self, "Ward Selected", f"ওয়ার্ড নং {eng} সিলেক্ট করা হয়েছে।")
                return
        self.selected_ward = ward_text

    def search_data(self):
        if not self.selected_ward:
            QMessageBox.warning(self, "Warning", "ওয়ার্ড সিলেক্ট করুন।")
            return
        try: dob = self.dateEdit.date().toString("dd/MM/yyyy")
        except: return
        
        db_path = os.path.join(folder_path, db_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            table_name = get_table_name(cursor)
            query = f"SELECT * FROM {table_name} WHERE `Ward No.(ওয়ার্ড নং)` = ? AND `Date of Birth (জন্ম তারিখ)` = ?"
            cursor.execute(query, (self.selected_ward, dob))
            rows = cursor.fetchall()
            col_names = [d[0] for d in cursor.description]
            self.populate_table(rows, col_names)
            conn.close()
            if not rows: QMessageBox.warning(self, "Not Found", "তথ্য পাওয়া যায়নি।")
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def populate_table(self, rows, columns):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for r, row_data in enumerate(rows):
            self.tableWidget.insertRow(r)
            for c, data in enumerate(row_data):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(data)))

    def show_details(self, r, c):
        cols = self.tableWidget.columnCount()
        data_dict = {}
        for i in range(cols):
            raw_header = self.tableWidget.horizontalHeaderItem(i).text()
            clean_header = clean_header_text(raw_header)
            value = self.tableWidget.item(r, i).text()
            data_dict[clean_header] = value
        DetailWindow(data_dict).exec()

# মেইন উইন্ডো
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        load_ui_file('Dhaka13.ui', self)
        self.setFixedSize(450, 800)

        try:
            label = self.findChild(QtWidgets.QLabel, "lb1")
            if label:
                label.setGeometry(0, 0, 450, 60)
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                label.setFont(QtGui.QFont(APP_FONT_FAMILY, 16, QtGui.QFont.Weight.Bold))
        except: pass

        button_width = 400
        button_height = 60
        margin_left = (450 - button_width) // 2 
        try:
            current_y1 = self.pushButton.y()
            self.pushButton.setGeometry(margin_left, current_y1, button_width, button_height)
            self.pushButton.setFont(QtGui.QFont(APP_FONT_FAMILY, 12, QtGui.QFont.Weight.Bold))
        except: pass
        try:
            current_y2 = self.pushButton_5.y()
            self.pushButton_5.setGeometry(margin_left, current_y2, button_width, button_height)
            self.pushButton_5.setFont(QtGui.QFont(APP_FONT_FAMILY, 12, QtGui.QFont.Weight.Bold))
        except: pass

        try: self.pushButton.clicked.connect(self.open_window_three)
        except: pass
        try: self.pushButton_5.clicked.connect(self.open_window_two)
        except: pass

    def open_window_three(self):
        self.w3 = WindowThree()
        self.w3.show()
    def open_window_two(self):
        self.w2 = WindowTwo()
        self.w2.show()

if __name__ == '__main__':
    if hasattr(os, "environ"):
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        os.environ["QT_SCALE_FACTOR"] = "1"

    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont(APP_FONT_FAMILY, 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
