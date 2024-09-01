from PyQt6.QtWidgets import QMenu, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QUrl
import os

"""Delete music file"""
def delete_file(music_list, music_name_label, play_button, pause_button, player, file_name):
    item = music_list.currentItem()
    if item:
        music_name = item.text()
        music_list.takeItem(music_list.row(item))
        
        with open(r"source/settings/music_list/list.txt", 'r') as file:
            lines = file.readlines()
        with open(r"source/settings/music_list/list.txt", 'w') as file:
            for line in lines:
                if not os.path.basename(line.strip()[:-4]) == music_name:
                    file.write(line)
        
        music_name_label.setText("")
        file_name = None
        pause_button.hide()
        play_button.show()
        player.setSource(QUrl.fromLocalFile(None))
        
        QMessageBox.information(None, "File deletion", f'The file "{music_name}" was successfully deleted')
    else:
        QMessageBox.warning(None, "Error", "Select file to delete")

"""Show context menu"""
def show_context_menu(pos, music_list, music_name_label, play_button, pause_button, player, file_name):
    menu = QMenu()
    delete_action = QAction("Delete File", menu)
    delete_action.triggered.connect(lambda: delete_file(music_list, music_name_label, play_button, pause_button, player, file_name))
    menu.addAction(delete_action)
    menu.exec(music_list.viewport().mapToGlobal(pos))
