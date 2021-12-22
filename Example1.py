import sys
from PyQt5.QtWidgets import QApplication, QWidget

#application object
app = QApplication(sys.argv)

window = QWidget()

window.show()

# Start the event loop.
app.exec_()