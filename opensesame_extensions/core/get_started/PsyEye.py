from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
import sys


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setFixedHeight(40)
        self.title = QLabel("EyeGuide")
        self.title.setStyleSheet("color: white; font-size: 16px;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addStretch()
        self.layout.addWidget(self.title)
        self.layout.addStretch()

        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("background-color: transparent; color: blue;")
        self.close_button.clicked.connect(self.close_window)

        self.layout.addWidget(self.close_button)
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #2E3440;")

    def close_window(self):
        self.parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.mouse_down_position = (
                event.globalPos() - self.parent.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.mouse_down_position)
            event.accept()


class Chatbot(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.title_bar = CustomTitleBar(self)
        self.layout.addWidget(self.title_bar)
        self.theme_button = QPushButton("🔦")
        self.theme_button.setFixedSize(30, 30)
        self.theme_button.setStyleSheet(
            "border: none; background: transparent; font-size: 20px;"
        )
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_layout = QHBoxLayout()
        self.theme_layout.addStretch()
        self.theme_layout.addWidget(self.theme_button)
        self.theme_layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addLayout(self.theme_layout)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet(
            """
            QTextEdit {
                border-radius: 15px;
                padding: 0px;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
            }
            QScrollBar:vertical {
                border: none;
                background: #3B4252;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #81A1C1;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
                border: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )
        self.layout.addWidget(self.chat_area)
        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
            }
        """
        )
        self.input_layout.addWidget(self.input_field)
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet(
            """
            QPushButton {
                border-radius: 15px;
                background-color: #5E81AC;
                color: #ECEFF4;
                font-size: 14px;
                padding: 5px 10px;
                font-family: 'Arial', sans-serif;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """
        )
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)
        self.apply_dark_mode()

    def send_message(self):
        user_message = self.input_field.text()
        if user_message.strip() == "":
            return

        self.chat_area.append(f"<b>Tú:</b> {user_message}\n")

        bot_response = self.get_bot_response(user_message)

        self.chat_area.append(f"<b>PsyEye:</b> {bot_response}")

        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )

        self.input_field.clear()

    def get_bot_response(self, message):
        message = message.lower()

        respuestas = {
            "open sesame": "OpenSesame es una plataforma de código abierto para construir experimentos en psicología, neurociencia y ciencias cognitivas. Permite crear experimentos de manera visual y a través de código.",
            "que es open sesame": "OpenSesame es un programa de código abierto que se utiliza para diseñar experimentos de manera simple y flexible. Ideal para investigadores que trabajan en ciencias cognitivas, neurociencia y psicología.",
            "experimento": "En OpenSesame, un experimento es una colección de tareas o eventos que se pueden definir en forma de bloques, secuencias y ciclos para mostrar estímulos o recoger respuestas de los participantes.",
            "bloques": "Un bloque en OpenSesame agrupa un conjunto de ensayos o pruebas experimentales. Puedes repetir estos bloques múltiples veces para recolectar más datos.",
            "secuencia": "Una secuencia es un componente fundamental en OpenSesame, donde se define el orden en que se presentan los estímulos, ensayos o eventos. Los experimentos se estructuran en secuencias de eventos o bloques.",
            "ciclos": "Los ciclos en OpenSesame permiten repetir un conjunto de ensayos o tareas varias veces. Un ciclo puede estar controlado por variables para modificar las condiciones experimentales en cada repetición.",
            "variables": "Las variables en OpenSesame son valores que se pueden cambiar durante un experimento, como la duración del estímulo o la respuesta del participante. Se utilizan para controlar el flujo de un experimento.",
            "estímulos": "Un estímulo en OpenSesame puede ser cualquier cosa que se presenta al participante, como una imagen, un sonido, un texto o un video. Los estímulos son parte esencial de cualquier experimento.",
            "respuesta": "La respuesta es la interacción del participante con el experimento, como presionar una tecla, hacer clic con el ratón o hablar. OpenSesame registra las respuestas para su análisis posterior.",
            "dibujo de pantalla": "El elemento de dibujo de pantalla (sketchpad) en OpenSesame te permite diseñar pantallas visuales para mostrar a los participantes. Puedes añadir texto, imágenes, formas y más.",
            "colección de respuestas": "OpenSesame proporciona múltiples maneras de recoger respuestas de los participantes. Puedes usar un teclado, ratón o incluso dispositivos externos como pulsadores.",
            "interfaz gráfica": "OpenSesame tiene una interfaz gráfica de usuario intuitiva donde puedes arrastrar y soltar elementos para diseñar experimentos, lo que facilita el uso sin tener que escribir código.",
            "python": "OpenSesame está basado en Python, lo que significa que puedes utilizar scripts de Python para automatizar y personalizar tu experimento. También puedes interactuar directamente con bibliotecas de Python dentro de OpenSesame.",
            "opensesame versus eprime": "OpenSesame es una alternativa de código abierto a software comercial como E-Prime. Es gratuito y flexible, lo que lo convierte en una opción popular entre los investigadores académicos.",
            "plugins": "OpenSesame admite plugins, lo que significa que puedes expandir sus funcionalidades. Los plugins pueden añadir soporte para nuevos tipos de estímulos, dispositivos de recolección de datos y mucho más.",
            "experimentar con sonido": "Puedes utilizar OpenSesame para incluir estímulos auditivos en tus experimentos. El programa permite reproducir sonidos o música y registrar respuestas basadas en estos estímulos.",
            "pruebas psicológicas": "OpenSesame es muy utilizado para crear pruebas psicológicas como Stroop, Flanker y tareas de memoria de trabajo. Su flexibilidad permite adaptar estos experimentos fácilmente.",
            "hardware": "OpenSesame se integra con varios tipos de hardware, como eye-trackers (seguimiento ocular), dispositivos de respuesta y EEG, lo que lo hace ideal para estudios en neurociencia.",
            "análisis de datos": "Los datos recolectados en OpenSesame se pueden exportar en varios formatos, como CSV o Excel, y pueden ser analizados posteriormente con herramientas como SPSS o Python.",
            "seguimiento ocular": "OpenSesame puede conectarse con eye-trackers para estudios de seguimiento ocular. Con plugins como PyGaze, puedes monitorear hacia dónde mira un participante en tiempo real.",
            "osweb": "OsWeb es una extensión de OpenSesame que te permite ejecutar experimentos en un navegador web. Esto es ideal para experimentos en línea donde los participantes no están físicamente presentes.",
            "temporalización": "La temporalización es crucial en los experimentos. OpenSesame ofrece control preciso sobre el tiempo de presentación de estímulos y la recolección de respuestas, algo fundamental para experimentos de psicología y neurociencia.",
            "tasa de refresco": "La tasa de refresco de la pantalla es importante para presentar estímulos visuales de forma precisa. OpenSesame te permite controlar y ajustar la tasa de refresco de acuerdo con tu hardware.",
            "condiciones experimentales": "Puedes definir condiciones experimentales en OpenSesame utilizando variables para modificar aspectos del experimento, como la duración del estímulo o las respuestas esperadas, en cada ensayo.",
            "documentación": "La documentación de OpenSesame es extensa y está disponible en su sitio web. Hay muchos tutoriales, ejemplos y guías para ayudarte a comenzar rápidamente.",
            "soporte de comunidad": "OpenSesame tiene una comunidad activa de usuarios y desarrolladores. En los foros puedes encontrar ayuda para resolver problemas, compartir plugins y aprender de otros investigadores.",
            "ensayos": "Un ensayo en OpenSesame es una unidad experimental que contiene los estímulos presentados y las respuestas registradas. Los ensayos se agrupan en bloques y secuencias.",
            "pseudorandomización": "Puedes usar pseudorandomización en OpenSesame para presentar los estímulos en un orden aleatorio controlado, asegurando que cada participante vea estímulos de manera equilibrada.",
            "open science": "OpenSesame se alinea con los principios de la ciencia abierta. Es una herramienta gratuita y de código abierto que promueve la transparencia y reproducibilidad en la investigación científica.",
            "ventana de registro": "La ventana de registro en OpenSesame muestra información en tiempo real sobre la ejecución del experimento. Aquí puedes ver mensajes de depuración y resultados de prueba.",
            "multiplataforma": "OpenSesame está disponible para Windows, macOS y Linux, lo que lo hace accesible para la mayoría de los investigadores sin importar su sistema operativo.",
            "randomización": "Puedes randomizar los ensayos y las condiciones en OpenSesame para evitar sesgos en la presentación de los estímulos, lo que es crucial para experimentos controlados.",
            "guía rápida": "La guía rápida de OpenSesame te ayudará a empezar con los conceptos básicos, como la creación de experimentos simples y la configuración de bloques y secuencias.",
            "guis": "Las GUI (interfaces gráficas de usuario) en OpenSesame permiten crear fácilmente tareas experimentales complejas mediante un sistema de arrastrar y soltar, sin necesidad de programar.",
            "timing": "El control preciso del timing es fundamental en OpenSesame. Puedes sincronizar la presentación de estímulos y la recogida de respuestas con alta precisión temporal.",
            "codificación en python": "Además de la interfaz gráfica, OpenSesame permite escribir scripts personalizados en Python, lo que añade flexibilidad a la creación y análisis de experimentos complejos.",
            "paquetes de python": "Puedes integrar paquetes de Python como NumPy o Pandas en OpenSesame para realizar cálculos complejos o manipulación avanzada de datos durante el experimento.",
            "multimedia": "OpenSesame admite la presentación de varios tipos de contenido multimedia, incluyendo imágenes, videos y sonidos, lo que lo hace ideal para estudios multisensoriales.",
            "distractores": "Puedes crear tareas con distractores visuales o auditivos en OpenSesame para probar la atención de los participantes y cómo manejan la interferencia en tareas cognitivas.",
        }

        for palabra_clave, respuesta in respuestas.items():
            if palabra_clave in message:
                return respuesta

        return "Lo siento, no entiendo tu consulta. Intenta preguntar algo más relacionado con OpenSesame."

    def toggle_theme(self):
        if self.is_dark_mode:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()
        self.is_dark_mode = not self.is_dark_mode

    def apply_dark_mode(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1E1E1E;
            }
            QTextEdit {
                background-color: #2E2E2E;
                color: #ECEFF4;
                font-size: 14px;
                border-radius: 15px;
            }
            QLineEdit {
                background-color: #2E2E2E;
                color: #ECEFF4;
                font-size: 14px;
                border-radius: 15px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                font-size: 14px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """
        )
        self.chat_area.setStyleSheet(
            """
            QTextEdit {
                background-color: #2E2E2E;
                color: #ECEFF4;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
            }
            QScrollBar:vertical {
                border: none;
                background: #3B4252;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #81A1C1;
                min-height: 20px;
                border-radius: 7px;
            }
        """
        )
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                background-color: #2E2E2E;
                color: #ECEFF4;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
            }
        """
        )

    def apply_light_mode(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #ECEFF4;
            }
            QTextEdit {
                background-color: #C0C0C0;
                color: #2E3440;
                font-size: 14px;
                border-radius: 15px;
            }
            QLineEdit {
                background-color: #C0C0C0;
                color: #2E3440;
                font-size: 14px;
                border-radius: 15px;
            }
            QPushButton {
                background-color: #A3BE8C;
                color: #2E3440;
                font-size: 14px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #88C0D0;
            }
        """
        )
        self.chat_area.setStyleSheet(
            """
            QTextEdit {
                background-color: #D3D3D3;
                color: #2E3440;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
            }
            QScrollBar:vertical {
                border: none;
                background: #D8DEE9;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #D3D3D3;
                min-height: 20px;
                border-radius: 7px;
            }
        """
        )
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                background-color: #D3D3D3;
                color: #2E3440;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
            }
        """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot = Chatbot()
    chatbot.show()

    sys.exit(app.exec_())
