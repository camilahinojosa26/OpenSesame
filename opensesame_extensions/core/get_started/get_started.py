# -*- coding:utf-8 -*-
"""
Este archivo es parte de OpenSesame.
...
"""

from libopensesame.py3compat import *
import os
import sys
from openexp import resources
from libopensesame import misc, metadata
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.translate import translation_context
from libqtopensesame.misc import template_info
import subprocess  # Para ejecutar el archivo Python

_ = translation_context(u'get_started', category=u'extension')


class GetStarted(BaseExtension):
    r"""Muestra la pestaña "Get started" y abre un experimento al inicio, si uno
    fue pasado en la línea de comandos.
    """
    
    def activate(self):
        # Inicializa plantillas
        templates = []
        for i, (path, desc) in enumerate(template_info.templates):
            try:
                path = resources[path]
            except:
                continue
            if not i:
                cls = u'important-button'
            else:
                cls = u'button'
            path = os.path.abspath(path).replace(u'\\', u'/')
            md = u'<a href="opensesame://%s" class="%s">%s</a><br />' % (path, cls, desc)
            templates.append(md)
        
        # Inicializa experimentos recientes
        if not self.main_window.recent_files:
            recent = []
        else:
            recent = [_(u'Continue with a recent experiment:')+u'<br />']
            for i, path in enumerate(self.main_window.recent_files):
                cls = u'important-button' if not i else u'button'
                md = u'<a href="opensesame://event.open_recent_%d" class="%s">%s</a><br />' % \
                    (i, cls, self._unambiguous_path(path))
                recent.append(md)
        
        # Añadir botón para ejecutar PsyEye.py
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
        psyeye_path = os.path.join(script_dir, "PsyEye.py")  # Ruta del archivo PsyEye.py
        psyeye_button = u'<a href="opensesame://event.run_psyeye" class="button">Run PsyEye</a><br />'

        # Crear markdown
        with safe_open(self.ext_resource(u'get_started.md')) as fd:
            md = fd.read()
        md = md % {
            u'version': metadata.__version__,
            u'codename': metadata.codename,
            u'templates': u'  \n'.join(templates),
            u'recent_experiments': u'  \n'.join(recent)
        }

        # Insertar botón de PsyEye en el markdown
        md += u'  \n' + psyeye_button

        self.tabwidget.open_markdown(md, title=_(u'Get started!'), icon=u'document-new')

    def _unambiguous_path(self, path):
        r"""Si el nombre del archivo es único entre los experimentos recientes, se
        utiliza. De lo contrario, se usa la ruta completa.

        Parameters
        ----------
        path
            La ruta a acortar de manera unívoca.

        Returns
        -------
        La ruta acortada unívocamente.
        """
        basename = os.path.basename(path)
        basenames = \
            [os.path.basename(_path)
             for _path in self.main_window.recent_files]
        return path if basenames.count(basename) > 1 else basename

    def event_open_recent_0(self):
        self.main_window.open_file(path=self.main_window.recent_files[0])

    def event_open_recent_1(self):
        self.main_window.open_file(path=self.main_window.recent_files[1])

    def event_open_recent_2(self):
        self.main_window.open_file(path=self.main_window.recent_files[2])

    def event_open_recent_3(self):
        self.main_window.open_file(path=self.main_window.recent_files[3])

    def event_open_recent_4(self):
        self.main_window.open_file(path=self.main_window.recent_files[4])

    @BaseExtension.as_thread(wait=500)
    def event_startup(self):
        # Abrir un experimento si se ha especificado como argumento en la línea de
        # comandos y suprimir el asistente en ese caso.
        if len(sys.argv) >= 2 and os.path.isfile(sys.argv[1]):
            path = safe_decode(sys.argv[1], enc=sys.getfilesystemencoding(),
                               errors=u'ignore')
            self.main_window.open_file(path=path)
            return
        self.activate()

    def event_run_psyeye(self):
        """Evento que ejecuta el archivo PsyEye.py."""
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del archivo actual
        psyeye_path = os.path.join(script_dir, "PsyEye.py")  # Ruta del archivo PsyEye.py
        subprocess.run([sys.executable, psyeye_path])  # Ejecutar el archivo PsyEye.py
