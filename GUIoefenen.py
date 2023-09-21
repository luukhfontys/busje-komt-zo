import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QWidget

class ExcelUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.df = None  # Initialize self.df as None

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Excel File Uploader")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.upload_button = QPushButton("Upload Excel File", self)
        self.upload_button.clicked.connect(self.load_excel_file)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout.addWidget(self.upload_button)
        layout.addWidget(self.text_edit)

        self.central_widget.setLayout(layout)

    def load_excel_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        excel_file, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)

        if excel_file:
            try:
                df = pd.read_excel(excel_file)
                self.df = df  # Store the DataFrame in self.df
                self.text_edit.setPlainText(str(df))
                print(df)
            except Exception as e:
                self.text_edit.setPlainText(f"Error loading Excel file: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = ExcelUploader()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
