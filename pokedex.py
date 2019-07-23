import pandas as pd
import sys, urllib3
import requests
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
import PokemonData


class PokeDex(QWidget):

    def __init__(self):
        super(PokeDex, self).__init__()

        self.initUI()

    def initUI(self):
        '''Initial UI'''

        # Grid Layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Parse JSON for DataFrame
        self.df = pd.read_json('PokemonData.json')
        self.df = self.df.set_index(['#'])
        # Drop Down
        self.dropdown = QComboBox(self)
        self.names = self.df['Name'].values
        self.dropdown.addItems(self.names)
        self.grid.addWidget(self.dropdown, 0, 0, 1, 1)

        # Search Button
        self.btn = QPushButton('Search',self)
        self.btn.clicked.connect(self.runSearch)
        self.grid.addWidget(self.btn, 0, 1, 1, 1)



        # Image
        self.img = QLabel(self)
        self.grid.addWidget(self.img, 1, 1, 1, 1)


        # Data
        self.label = QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('\nName:\n\nType:\n\nHP:\n\nAttack\n\nSp. Attack\n\nDefense:\n\nSp. Defense:\n\nSpeed:\n\nTotal:')
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.label, 1, 0, 1, 1)

        # Customize Widgets
        self.resize(500, 250)
        self.center()
        self.setWindowTitle('PokeDex')
        self.show()

    def runSearch(self):
        '''Event for run button'''
        # Parse value
        index = self.dropdown.currentIndex()

        val = self.names[index]

        cond = self.df['Name'] == val


        # Image

        base = 'https://img.pokemondb.net/artwork/'
        img_url = base + PokemonData.str_layout(val) + '.jpg'
        data = urllib3.PoolManager().urlopen('GET',img_url).data


        image = QtGui.QImage()
        image.loadFromData(data)


        self.img.setPixmap(QtGui.QPixmap(image))




        # Set values
        name = 'Name:\t\t\t' + val + '\n\n'
        ty = 'Type:\t\t\t' + ', '.join(self.df[cond]['Type'].values[0]) + '\n\n'
        hp = 'HP:\t\t\t' + str(self.df[cond]['HP'].values[0]) + '\n\n'
        atk = 'Attack:\t\t\t' + str(self.df[cond]['Attack'].values[0]) + '\n\n'
        satk = 'Sp. Attack:\t\t' + str(self.df[cond]['Sp. Atk'].values[0]) + '\n\n'
        deff = 'Defense:\t\t\t' + str(self.df[cond]['Defense'].values[0]) + '\n\n'
        sdef = 'Sp. Defense:\t\t' + str(self.df[cond]['Sp. Def'].values[0]) + '\n\n'
        speed = 'Speed:\t\t\t' + str(self.df[cond]['Speed'].values[0]) + '\n\n'
        total = 'Total:\t\t\t' + str(self.df[cond]['Total'].values[0]) + '\n\n'

        # Add text
        final = name + ty + hp + atk + satk + deff + sdef + speed + total
        self.label.setText(final)






    def center(self):
        '''Center Widget on screen'''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    '''Codes for running GUI'''

    # Create Application object to run GUI
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)


    # Run GUI
    gui = PokeDex()
    # gui.show()
    # Exit cleanly when closing GUI
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

if __name__ == '__main__':
    main()