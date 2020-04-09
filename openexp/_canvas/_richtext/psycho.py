# coding=utf-8

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from openexp._canvas._richtext.richtext import RichText
from openexp._canvas._element.psycho import PsychoElement
from psychopy import visual


class Psycho(PsychoElement, RichText):

	def prepare(self):

		im = self._to_pil()
		# When displaying on Mac retina screens, the resolutions reported by psychopy's window object
		# and OpenSesame's experiment object may diverge. This results in incorrectly rendered text
		# with respect to scale and positioning. We correct for the discrepancy between reported sizes
		# by the ratios calculated below.
		x_ratio = self.win.size[0] / self.experiment.width
		y_ratio = self.win.size[1] / self.experiment.height
		im = im.resize((int(im.width * x_ratio), int(im.height * y_ratio)))
		x, y = self.to_xy(int(self.x * x_ratio), int(self.y * y_ratio))
		if not self.center:
			x += im.width // 2
			y -= im.height // 2
		self._stim = visual.SimpleImageStim(self.win, im, pos=(x, y))
