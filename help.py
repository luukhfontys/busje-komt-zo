from Functions import prestatiemaat_materiaal_minuten
import pandas as pd
from bus_class import bus
from minimale_oplaadtijd import minimale_oplaadtijd
from GUIoefenen import ExcelUploader
import sys
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = ExcelUploader()
    window.show()
    if window.df is not None:
    # You can use the df variable here
        my_dataframe = window.df
    # Perform operations on my_dataframe as needed
        print(my_dataframe.head())  # For example, printing the first few rows
    else:
        print("No DataFrame available.")

    # Als je bijvoorbeeld de load_excel_file-methode wilt aanroepen wanneer een knop wordt geklikt, kun je dit doen binnen de GUI zelf, niet hier.

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

main().df