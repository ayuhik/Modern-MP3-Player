from PyQt6.QtWidgets import QMessageBox

"""Error box, file not found"""
def no_file_error():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText("Couldn't find the file")
    msg_box.setWindowTitle("Error")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()

"""Error box, the file already exists"""
def file_exists_error():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText("The file already exists")
    msg_box.setWindowTitle("Error")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()