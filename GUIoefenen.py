import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QWidget
#ja er zijn moker veel imports nodig

class ExcelUploader(QMainWindow):
    """
    Ik heb een class aan gemaakt omdat dit tochwel de belangrijkste functie van het hele bestand is wat we 
    gebruiken en nodig hebben voor onze UI
    
    """
    def __init__(self):
        #Dit start de UI op. dit gebeurd door de zojuist aangemaakte functie aan te roepen. Hij inilialised hier
        #Dus ook de UI
        super().__init__()

        self.initUI()


    def initUI(self):
        #Dit is de positie van het scherm waar de popup terecht komt maar ook de venster grootte. Eerste 2 inputs positie 
        #linksboven, laatste 2 inputs grootte van venster
         
        self.setGeometry(100, 100, 600, 400)
        #dit is de titel van de popup
        self.setWindowTitle("Excel File Uploader")


        #Dit is maken van het hoofdonderdeel van de UI. Is een functie van qwidget
        self.central_widget = QWidget(self)
        #Het daadwerkelijk positioneren van
        self.setCentralWidget(self.central_widget)
        #layout instellingen, heb nog geen idee hoe dit moet
        layout = QVBoxLayout()


        #Wajot, dit is een optie om knoppen te maken en we maken gebruik van een functie die we later maken
        self.upload_button = QPushButton("Upload Excel File", self)
        self.upload_button.clicked.connect(self.load_excel_file)


        # Oke leuk, we hebben een excelfile geupload, maar door deze instellingen hebben we een tekstvak om daadwerkelijk
        # in te schrijven
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        #Hierdoor kunnen we excelfiles blijven uploaden
        layout.addWidget(self.upload_button)
        layout.addWidget(self.text_edit)

        #Updating van het venster
        self.central_widget.setLayout(layout)

    
    ''' Oke we hebben eerder een knop gemaakt. We gaan nu de functie schrijven die daardwerkelijk invloed heeft op
     wat er met de knop gebeurd. Dit is echt 1 op 1 overgenomen van het internet. Sorry not sorry '''
    def load_excel_file(self):
  
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Dialoog venster openen zodat er daadwerkelijk een bestand kan worden geselecteerd
        excel_file, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)

        if excel_file:
            try:
                # Pandas gebruiken om excel in te lezen die zojuist is geselecteerd.
                df = pd.read_excel(excel_file)
                # De excel weergeven in het tekstvak, super chill
                self.text_edit.setPlainText(str(df))
                
            except Exception as e:
                # Gelijk een kleine foutcode erin gejankt
                self.text_edit.setPlainText(f"Error loading Excel file: {str(e)}")

def main():
    """Het daadwerkelijk uitvoeren van de functie, jullie kennen dit beter dan ik"""
    app = QApplication(sys.argv)
    window = ExcelUploader()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
