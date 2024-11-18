import json
from qtpy import QtCore, QtGui, QtWidgets
from libopensesame.py3compat import *
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.drag_and_drop import send
from libqtopensesame.misc.translate import translation_context
from qtpy.QtMultimedia import QSoundEffect
import os

_ = translation_context(u'toolbar_items_item', category=u'core')

class ToolbarItemsItem(BaseSubcomponent, QtWidgets.QLabel):
    r"""A draggable toolbar icon."""
    def __init__(self, parent, item, pixmap=None):
        super().__init__(parent)
        self.setup(parent)
        self.item = item
        self.pixmap = pixmap if pixmap else self.theme.qpixmap(item)
        self.setToolTip(_("Drag this <b>%s</b> item to the intended location in the overview area or into the item list of a sequence tab") % self.item)
        self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.setPixmap(self.pixmap)

        # Construct the full path to the .wav file
        sound_path = os.path.join(os.path.dirname(__file__), "drag_4.wav")
        sound_path2 = os.path.join(os.path.dirname(__file__), "drop_4.wav")

        # Initialize sound effect
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QtCore.QUrl.fromLocalFile(sound_path))
        self.sound_effect.setVolume(0.8)
        self.sound_effect.setLoopCount(QSoundEffect.Infinite) 

        self.sound_effect2 = QSoundEffect()
        self.sound_effect2.setSource(QtCore.QUrl.fromLocalFile(sound_path2))
        self.sound_effect2.setVolume(0.8)

    def mousePressEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        
        self.start_pos = e.pos()
        self.name = u'new_%s' % self.item
        self.data = {
            u'type': u'item-snippet',
            u'main-item-name': self.name,
            u'items': [{
                u'item-type': self.item,
                u'item-name': self.name,
                u'script': u''
            }]
        }
        self.item_toolbar.collapse()

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            if (e.pos() - self.start_pos).manhattanLength() >= QtWidgets.QApplication.startDragDistance():

                self.sound_effect.play()

                drag = QtGui.QDrag(self)
                mime_data = QtCore.QMimeData()
                mime_data.setData('application/json', json.dumps(self.data).encode('utf-8'))
                drag.setMimeData(mime_data)

                # Crear un pixmap para el ícono de arrastre
                drag_icon = QtGui.QPixmap(self.pixmap.size())
                drag_icon.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(drag_icon)
                painter.drawPixmap(0, 0, self.pixmap)
                painter.end()

                drag.setPixmap(drag_icon)
                drag.setHotSpot(e.pos() - self.rect().topLeft())

                # Inicia el arrastre y la animación de tambaleo
                self.start_shake_animation()
                drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
                
                # Detener la animación de tambaleo cuando se suelta
                self.stop_shake_animation()

                self.stop_sound()

                name = u'new_%s' % self.item
                data = {
                    u'type': u'item-snippet',
                    u'main-item-name': name,
                    u'items': [{
                        u'item-type': self.item,
                        u'item-name': name,
                        u'script': u''
                    }]
                }
                self.item_toolbar.collapse()
                send(self, data)

    def start_shake_animation(self):
        """Creates a simple shake animation while dragging."""
        self.animation = QtCore.QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        self.animation.setKeyValueAt(0.25, self.pos() + QtCore.QPoint(5, 0))
        self.animation.setKeyValueAt(0.75, self.pos() - QtCore.QPoint(5, 0))
        self.animation.setEndValue(self.pos())
        self.animation.setLoopCount(-1)  # Hacer que el tambaleo se repita indefinidamente
        self.animation.start()

    def stop_shake_animation(self):
        """Stops the shake animation."""
        if hasattr(self, 'animation'):
            self.animation.stop()
            self.sound_effect2.play()
            self.setPixmap(self.pixmap)  # Reset the pixmap when leaving
        
    def stop_sound(self):
        """Stop the looping sound effect."""
        if self.sound_effect.isPlaying():
            self.sound_effect.stop()
        

# Alias for backwards compatibility
toolbar_items_item = ToolbarItemsItem