# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoordinateDialog
                                 A QGIS plugin
 Restituisce le coordinate cliccate
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-06-20
        git sha              : $Format:%H$
        copyright            : (C) 2018 by matteo
        email                : matteo@matteo.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox #GDF se non avessi fatto questo, nel codice avrei dovuto scrivere QtWidgets.QFileDialogs.getSaveFileName alla riga 61 e QtWidgets.QMessageBox.information alla riga 91
import csv #GDF metodo che scrive i file csv in python

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'coordinate_dialog_base.ui'))


class CoordinateDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CoordinateDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
		
        self.pushButton.clicked.connect(self.stampa) #GDF quando clicco il pulsante pushButton, connetti questo segnale al metodo stampa
		                                             #queste connessioni vanno tutte nella funzione __init__

        self.chooseButton.clicked.connect(self.outputPath) #GDF quando clicco il pulsante chooseButton, connetti questo segnale al metodo outputPath
        self.pushButton_2.clicked.connect(self.copyField) #GDF quando clicco il pulsante pushButton_2, connetti questo segnale al metodo copyField

        self.comboBox_2.setLayer(self.comboBox.currentLayer()) #GDF segnale tra la combo box del vettore filtrato e la combo box dei campi di quel vettore
		                                                       #(questo segnale è stato già impostato nella .ui tramite QtDesigner e deve essere ribadito qui)

    def stampa(self):
        print('ciao')
		
        print(self.comboBox.currentLayer()) #GDF comboBox è un oggetto della .ui che si popola con i layer in legenda.
		                                    #In questo caso stampa nella console l'oggetto corrispondente al layer selezionato nella comboBox
        for i in self.comboBox.currentLayer().getFeatures():
            print(i.attributes()) #GDF stampa nella console gli attributi del layer selezionato nella comboBox

    def outputPath(self):
        myfile,res=QFileDialog.getSaveFileName(self,"Select output file", "", '*.csv') #GDF si apre una finestra con intestazione "Select output file" che
                                                                                       #permette di creare un nuovo file (myfile). Le "" seguenti
                                                                                       #permettono di far aprire questa finestra sempre sullo stesso percorso.
                                                                                       #(Se voglio che la finestra si apra su una particolare cartella devo
																					   #mettere il percorso della cartella tra "").
                                                                                       #Il metodo getSaveFileName, oltre al file myfile, restituisce anche un
                                                                                       #controllo (res) che dice se abbiamo o meno clccato su Salva.
																					   #'*.csv' filtra i file csv
        if res: #GDF se ho cliccato su Apri...
            myfile +='.csv' #GDF ...aggiunge l'estensione .csv al nome del myfile (in windows non c'è bisogno). 
			                #myfile in realtà è l'intero percorso del file che si sta creando

        self.pathLine.setText(myfile) #GDF la barra pathLine si riempie con il percorso del myfile

        self.percorso=self.pathLine.text() #GDF percorso è una stringa con il percorso del file (è solo una copia di quello che è stato stampato nella barra pathLine)		

    def copyField(self):
        vl=self.comboBox.currentLayer() #GDF resituisce un oggetto di tipo QgsVectorLayer (è il layer filtrato nella comboBox)
        
        field=self.comboBox_2.currentText() #GDF prende il testo che compare nella comboBox_2 (si dovrebbe rempire con i campi del layer selezionato nella comboBox)
        
        with open(self.percorso,'w') as f: #GDF prende il percorso e apre il file in scrittura (w). f è un alias relativo al file csv in scrittura
            fieldname=[field] #GDF intestazione del file csv (ho solo una colonna con intestazione field). Per ora fieldname è solo un oggetto, non c'è scritto ancora niente nel file csv
            writer=csv.DictWriter(f,fieldnames=fieldname) #GDF writer è una specie di provider che si occupa della scrittura del csv usando il modulo DictWriter della classe csv
            writer.writeheader() #GDF scrive l'intestazione
            for i in vl.getFeatures(): #GDF itera sulle features del vettore vl
                writer.writerow({field: i[field]}) #GDF il metodo writerow permette di riempire le righe. writerow vuole come argomento un dizionario,
                                                   #dove le chiavi sono i nomi dei campi e i valori sono le singole features del vettore vl

        QMessageBox.information(self,'Information','Copia effettuata') #GDF finestra che ci informa che i campi sono stati copiati												   