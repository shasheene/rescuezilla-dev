from typing import Optional, Callable

from gi._gi import GObject
from gi.repository import Gtk, GLib

from logger import Logger
from utility import ErrorMessageModalPopup, Utility




# Duck-typed public interface, same as CliUiManager
class GtkUiManager:
    def __init__(self,
                 builder: Gtk.Builder,
                 main_statusbar: Gtk.StatusBar,
                 progress_bar: Gtk.ProgressBar,
                 progress_status: Gtk.Label,
                 post_task_action_combobox: Optional[Gtk.ComboBox] = None,
                 summary_program_defined_text: Optional[Gtk.Label] = None):
        self.logger: Optional[Logger] = None
        self.builder: Gtk.Builder = builder
        self.main_statusbar: Gtk.StatusBar = main_statusbar
        self.progress_bar: Gtk.ProgressBar = progress_bar
        self.progress_status: Gtk.Label = progress_status
        self.post_task_action_combobox: Optional[Gtk.ComboBox] = post_task_action_combobox
        self.summary_program_defined_text: Optional[Gtk.Label] = summary_program_defined_text

    def set_logger(self, logger: Logger):
        self.logger = logger

    def update_progress_bar(self,
                            **kwargs):
        GLib.idle_add(self._update_progress_bar(**kwargs))

    def _update_progress_bar(self,
                            fraction: float):
        if self.logger is not None:
            self.logger.write("Updating progress bar to " + str(fraction))
        self.progress_bar.set_fraction(fraction)

    def update_progress_status(self,
                               **kwargs):
        GLib.idle_add(self._update_progress_status(**kwargs))

    def _update_progress_status(self, message):
        self.progress_status.set_text(message)

    # Intended to be called via event thread
    def get_post_task_action(self) -> str:
        return Utility.get_combobox_key(self.post_task_action_combobox)

    def update_main_statusbar(self, message):
        context_id = self.main_statusbar.get_context_id("backup")
        self.main_statusbar.pop(context_id)
        self.main_statusbar.push(context_id, message)

    def display_status(self, **kwargs):
        GLib.idle_add(self._update_progress_status(**kwargs))

    def remove_all_main_statusbar(self,
                                  **kwargs):
        GLib.idle_add(self._remove_all_main_statusbar, **kwargs)

    def _remove_all_main_statusbar(self,
                                  context_id: str):
        self.main_statusbar.remove_all(self.main_statusbar.get_context_id(context_id))

    # Intended to be called via event thread
    def _display_status(self, msg1, msg2):
        self.update_progress_status(message=msg1 + "\n" + msg2)
        if msg2 != "":
            status_bar_msg = msg1 + ": " + msg2
        else:
            status_bar_msg = msg1
        GLib.idle_add(self.update_main_statusbar, status_bar_msg)

    def display_error_message(self, **kwargs):
        GLib.idle_add(self._display_error_message, **kwargs)

    def _display_error_message(self, summary_message: str, heading: str = ""):
        error = ErrorMessageModalPopup(self.builder, summary_message, error_heading=heading)

    def completed_operation(self,
                             **kwargs):
        GLib.idle_add(self._completed_operation, **kwargs)

    def _completed_operation(self,
                             callable_fn: Callable,
                             succeeded: bool,
                             message: str):
        callable_fn(succeeded=succeeded, message=message)

    def escape_text(self, input: str) -> str:
        return GObject.markup_escape_text(input)

    def display_summary_text(self, text_to_display):
        self.summary_program_defined_text.set_market(text_to_display)

class UiManager(GtkUiManager):
    pass