"""
Your favorite Audio Cutter.
Author : Bilal Elmoussaoui (bil.elmoussaoui@gmail.com)
Artist : Alfredo Hernández
Website : https://github.com/bil-elmoussaoui/Audio-Cutter
This file is part of AudioCutter.
AudioCutter is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
AudioCutter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with AudioCutter. If not, see <http://www.gnu.org/licenses/>.
"""
from gettext import gettext as _

from .time import TimeButton
from ..utils import format_ns

from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk


class SoundConfig(Gtk.Box):
    """
        Audio configurations like:
        - Start time
        - End time
        - Fade in/out
    """
    instance = None

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.set_border_width(18)
        self._start_time = TimeButton()
        self._end_time = TimeButton()
        self._fade_in = Gtk.Switch()
        self._fade_out = Gtk.Switch()
        self._setup_widgets()

    @staticmethod
    def get_default():
        if SoundConfig.instance is None:
            SoundConfig.instance = SoundConfig()
        return SoundConfig.instance

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def is_fade_in(self):
        return self._fade_in.get_active()

    @property
    def is_fade_out(self):
        return self._fade_out.get_active()

    def _setup_widgets(self):
        """Setup the main SoundConfig widgets."""
        # Start time/ Fade in widget
        self._start_time.set_sensitive(False)
        self._fade_in.set_sensitive(False)
        start_box = SoundConfig.setup_box([
            (_("Start time"), self._start_time),
            (_("Fade in"), self._fade_in)
        ])
        self.pack_start(start_box, True, True, 6)
        # End time/ Fade out widget
        self._fade_out.set_sensitive(False)
        self._end_time.set_sensitive(False)
        end_box = SoundConfig.setup_box([
            (_("End time"), self._end_time),
            (_("Fade out"), self._fade_out)
        ])
        self.pack_end(end_box, True, True, 6)

    @staticmethod
    def setup_box(list_):
        """Setup a listbox from a list of (label, widget)."""
        # Setup the listbox
        listbox = Gtk.ListBox()
        listbox.get_style_context().add_class("config-list-box")
        listbox.set_halign(Gtk.Align.FILL)
        listbox.set_valign(Gtk.Align.FILL)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        def _resize_listbox_childs(listbox):
            """Set the listbox childs to have the same height."""
            max_height = 0
            for row in listbox.get_children():
                height = row.get_allocated_height()
                if height > max_height:
                    max_height = height
            for row in listbox.get_children():
                row.props.height_request = max_height

        for label, widget in list_:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                          spacing=6)
            widget.set_valign(Gtk.Align.CENTER)
            label_ = Gtk.Label(label=label)
            label_.get_style_context().add_class("config-list-box-label")
            box.pack_start(label_, False, False, 12)
            box.pack_end(widget, False, False, 12)
            listboxrow = Gtk.ListBoxRow()
            listboxrow.get_style_context().add_class("config-list-box-row")
            listboxrow.add(box)
            listbox.add(listboxrow)
        listbox.connect("realize", _resize_listbox_childs)

        return listbox

    def set_state(self, state):
        """Set the SoundConfig state active/inactive."""
        self._end_time.set_sensitive(state)
        self._start_time.set_sensitive(state)
        self._fade_in.set_sensitive(state)
        self._fade_out.set_sensitive(state)

    def set_duration(self, duration):
        """Set the max duration."""
        time_obj = format_ns(duration)
        self._start_time.duration = time_obj
        self._end_time.duration = time_obj
        self._end_time.time = time_obj
