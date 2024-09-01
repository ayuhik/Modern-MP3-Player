from PyQt6.QtWidgets import QFileDialog, QMainWindow, QLabel, QWidget, QPushButton, QListWidget, QSlider
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl, QRect, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from errors import no_file_error, file_exists_error
from delete_music import delete_file, show_context_menu
import os
import shutil

class Music_Player(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        
        self.setFixedSize(600, 570)
        self.setWindowTitle("MP3 Player")
        self.setStyleSheet("")
        self.setIconSize(QSize(1000, 1000))
        
        
        self.frame_label = QLabel(self)
        self.frame_label.setGeometry(QRect(0, 0, 641, 571))
        self.frame_label.setText("")
        self.frame_label.setPixmap(QPixmap(r"source\images\frame.png"))
        
        
        self.open_file_button = QPushButton(self.frame_label)
        self.open_file_button.setGeometry(QRect(0, 70, 151, 51))
        icon = QIcon()
        icon.addPixmap(QPixmap(r"source\images\open_file_button.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_file_button.setIcon(icon)
        self.open_file_button.setIconSize(QSize(200, 200))
        self.open_file_button.clicked.connect(self.select_music)
        
        
        self.music_list_text = QLabel(self.frame_label)
        self.music_list_text.setGeometry(QRect(0, 170, 151, 51))
        self.music_list_text.setText("")
        self.music_list_text.setPixmap(QPixmap(r"source\images\music_list_text.png"))
        
        
        self.music_name_label = QLabel(self.frame_label)
        self.music_name_label.setGeometry(QRect(260, 450, 1000, 25))
        font = QFont()
        font.setFamily("Yu Gothic UI Light")
        font.setPointSize(14)
        font.setBold(False)
        self.music_name_label.setFont(font)
        self.music_name_label.setWordWrap(True)
        
        self.music_bar  = QLabel(self.frame_label)
        self.music_bar.setGeometry(QRect(170, 510, 440, 51))
        self.music_bar.setPixmap(QPixmap(r"source\images\music_bar.png"))
        
        
        self.play_button = QPushButton(self.frame_label)
        self.play_button.setGeometry(QRect(350, 515, 41, 41))
        self.play_button.setStyleSheet("background: transparent;\n"
"border: none;")
        icon = QIcon()
        icon.addPixmap(QPixmap(r"source\images\play_button.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.play_button.setIcon(icon)
        self.play_button.setIconSize(QSize(50, 50))
        self.play_button.clicked.connect(self.play)
        
        
        self.pause_button = QPushButton(self.frame_label)
        self.pause_button.setGeometry(QRect(350, 515, 41, 41))
        self.pause_button.setStyleSheet("background: transparent;\n"
"border: none;")
        icon = QIcon()
        icon.addPixmap(QPixmap(r"source\images\pause_button.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.pause_button.setIcon(icon)
        self.pause_button.setIconSize(QSize(50, 50))
        self.pause_button.hide()
        self.pause_button.clicked.connect(self.pause)
        
        
        self.close_button = QPushButton(self.frame_label)
        self.close_button.setGeometry(QRect(520, 515, 41, 41))
        self.close_button.setStyleSheet("background: transparent;\n"
"border: none;")
        icon = QIcon()
        icon.addPixmap(QPixmap(r"source\images\close_button.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.close_button.setIcon(icon)
        self.close_button.setIconSize(QSize(50, 50))
        self.close_button.clicked.connect(self.close_music)
        
        
        self.undo_button = QPushButton(self.frame_label)
        self.undo_button.setGeometry(QRect(300, 515, 41, 41))
        self.undo_button.setStyleSheet("background: transparent;\n"
"border: none;")
        icon = QIcon()
        icon.addPixmap(QPixmap(r"source\images\undo_button.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.undo_button.setIcon(icon)
        self.undo_button.setIconSize(QSize(50, 50))
        self.undo_button.clicked.connect(self.next_song)
        
        self.redo_button = QPushButton(self.frame_label)
        self.redo_button.setGeometry(QRect(400, 515, 41, 41))
        self.redo_button.setStyleSheet("background: transparent;\n"
"border: none;")
        icon = QIcon()
        icon.addPixmap(QPixmap(r"source\images\redo_button.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.redo_button.setIcon(icon)
        self.redo_button.setIconSize(QSize(50, 50))
        self.redo_button.clicked.connect(self.undo_song)
        
        self.music_list = QListWidget(self.frame_label)
        self.music_list.setGeometry(QRect(20, 240, 100, 180))
        self.music_list.setStyleSheet("""
    QListWidget {
        background-color: #130722;
        border-radius: 10px;
    }
    QListWidget::item {
        background-color: #130722;
        color: #49316d;
        padding: 10px;
    }
    QListWidget::item:selected {
        background-color: #0e0619;
        color: #49316d;
        border: none; 
        outline: none;
    }
""")
        self.music_list.itemClicked.connect(self.open_music)
        self.music_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.music_list.customContextMenuRequested.connect(lambda pos: show_context_menu(pos, self.music_list, self.music_name_label, self.play_button, self.pause_button, self.player, self.file_name))
        
        
        self.time_slider = QSlider(self.frame_label)
        self.time_slider.setGeometry(QRect(250, 490, 231, 16))
        self.time_slider.setStyleSheet("""
    QSlider::groove:horizontal {
        border: 0px solid #999999;
        height: 4px;
        background: url('source/images/time_bar.png');
        margin: 2px 0;
    }
    QSlider::handle:horizontal {
        background: #45174a;
        border: 0px solid #45174a;
        width: 10px;
        margin: -5px 0;
        border-radius: 10px;
    }
""")
        self.time_slider.setOrientation(Qt.Orientation.Horizontal)
        self.time_slider.setMinimum(0)
        self.time_slider.setValue(0)
        self.time_slider.sliderPressed.connect(self.pause_music_slider)
        self.time_slider.sliderReleased.connect(self.play_music_slider)
        self.time_slider.sliderMoved.connect(lambda position: self.player.setPosition(position))
        
        
        self.volume_icon = QLabel(self.frame_label)
        self.volume_icon.setGeometry(QRect(450, 515, 41, 41))
        self.volume_icon.setStyleSheet("background: transparent;\n"
        "border: none;")
        self.volume_icon.setPixmap(QPixmap(r"source\images\volume_up.png"))
        
        
        self.volume_slider = QSlider(self.frame_label)
        self.volume_slider.setGeometry(QRect(480, 528, 32, 16))
        self.volume_slider.setStyleSheet("""
    QSlider::groove:horizontal {
        border: 0px solid #999999;
        height: 4px;
        background: url('source/images/volume_bar.png');
        margin: 2px 0;
    }
    QSlider::handle:horizontal {
        background: #45174a;
        border: 0px solid #45174a;
        width: 8px;
        height: 1px;
        margin: -4px 0;
        border-radius: 10px;
    }
""")
        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setValue(50)
        self.volume_slider.sliderMoved.connect(lambda value: (self.audio_output.setVolume(value / 100), self.update_volume_icon()))

        
        self.player.durationChanged.connect(lambda duration: self.time_slider.setMaximum(duration))
        self.player.positionChanged.connect(lambda position: self.time_slider.setValue(position))
        
        self.file_name = None
        self.current = 0
        
        """Loading music"""     
        with open(r"source\settings\music_list\list.txt", "r") as file:
            music_string = file.readlines()
            for line in music_string:
                self.music_list.addItem(os.path.basename(line.strip()[:-4]))
                 
                 
    def select_music(self):
        self.file_name, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Audio Files (*.mp3 *.wav)")
        if self.file_name:
            music_name = os.path.basename(self.file_name)[:-4]
            self.music_name_label.setText(music_name)
            
            items = self.music_list.findItems(music_name, Qt.MatchFlag.MatchContains)
            if any(item.text() == music_name for item in items):
                self.music_name_label.setText("")
                file_exists_error()
                
            else:
                self.music_list.addItem(music_name)
                self.player.setSource(QUrl.fromLocalFile(self.file_name))
                print(self.file_name)
                shutil.copy(self.file_name, r"source\settings\tracks")
                with open(r"source\settings\music_list\list.txt", "a+", encoding="utf-8") as file:
                    file.write(self.file_name + "\n")
            
            
    def play(self):
        if not self.file_name:
            no_file_error()
        else:
            self.play_button.hide()
            self.pause_button.show()
            self.player.play()

    def pause(self):
        if not self.file_name:
            no_file_error()
        else:
            self.pause_button.hide()
            self.play_button.show()
            self.player.pause()
            
    """Move slider if music is pausing"""    
    def play_music_slider(self):
        if self.was_playing:
            self.player.play()
        
        
    def pause_music_slider(self):
        self.was_playing = self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        self.player.pause()

            
    """Stop music and clear player"""    
    def close_music(self):
        if not self.file_name:
            no_file_error()
            
        else:
            self.player.stop()
            self.music_name_label.setText("")
            self.file_name = None
            self.pause_button.hide()
            self.play_button.show()
            self.player.setSource(QUrl.fromLocalFile(None))

    """Open music from list"""
    def open_music(self, item):
        music_name = item.text()
        self.file_name = None
        with open(r"source\settings\music_list\list.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                if os.path.basename(line.strip()[:-4]) == music_name:
                    self.file_name = line.strip()
                    break
                    
        if self.file_name:
            os.path.isfile(self.file_name)
            self.music_name_label.setText(music_name)
            self.player.setSource(QUrl.fromLocalFile(self.file_name))
            self.play()
        else:
           no_file_error()
    
    
    def update_volume_icon(self):
        if self.volume_slider.value() <= 5:
            self.volume_icon.setPixmap(QPixmap(r"source\images\volume_off.png"))
        else:
            self.volume_icon.setPixmap(QPixmap(r"source\images\volume_up.png")) 
            
    
    def undo_song(self):
        self.current -= 1
        if self.current < 0:
            self.current = self.music_list.count() - 1
        
        self.music_list.setCurrentRow(self.current)
        self.play_current_song()


    def next_song(self):
        self.current += 1
        if self.current >= self.music_list.count():
            self.current = 0
        
        self.music_list.setCurrentRow(self.current)
        self.play_current_song()


    def play_current_song(self):
        current_item = self.music_list.currentItem()
        if current_item:
            music_name = current_item.text()
            with open(r"source\settings\music_list\list.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if os.path.basename(line.strip()[:-4]) == music_name:
                        self.file_name = line.strip()
                        break
            
            if self.file_name:
                self.music_name_label.setText(music_name)
                self.player.setSource(QUrl.fromLocalFile(self.file_name))
                self.play()
            else:
                no_file_error()