import datetime as dt
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry


######################
# VALIDATION CLASSES #
######################


class ValidatedMixin:
    """Adds a validation functionality to an input widget"""

    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.config(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
        )

    def _toggle_error(self, on=False):
        '''sets foreground colour to red if error found'''

        self.config(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        self._toggle_error(False)
        self.error.set('')
        valid = True
        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_validate(event=event)
        elif event == 'key':
            self._key_invalid(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )

    def _focusout_invalid(self, *args, **kwargs):
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid


class IntEntry(ValidatedMixin, ttk.Entry):
    '''Only allows integer entry'''

    def _key_validate(self, action, index, char, **kwargs):

        valid = True
        if action == '0':
            valid = True
        elif char.isdigit():
            valid = True
        else:
            valid = False

        return valid

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')

        return valid


class RequiredEntry(ValidatedMixin, ttk.Entry):
    '''Entry field is required to have value'''

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class DateInput(ValidatedMixin, DateEntry):
    """An Entry for ISO-style dates (Year-month-day)"""

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            self.error.set('A value is required')
            valid = False
        try:
            dt.datetime.strptime(self.get(), '%Y-%m-%d')
        except ValueError:
            self.error.set('Invalid date')
            valid = False
        return valid


class TimeEntry(ValidatedMixin, ttk.Entry):
    '''An Entry for hh:mm:ss style time'''

    def _key_validate(self, action, index, char, **kwargs):
        valid = True
        if action == '0':
            valid = True
        elif index in ('0', '1', '3', '4', '6', '7'):
            valid = char.isdigit()
        elif index in ('2', '5'):
            valid = (char == ':')
        else:
            valid = False
        return valid

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            self.error.set('A value is required')
            valid = False
        try:
            dt.datetime.strptime(self.get(), "%H:%M:%S")
        except ValueError:
            self.error.set('Invalid Time')
            valid = False
        return valid


class ValidatedCombobox(ValidatedMixin, ttk.Combobox):
    '''Combobox with all the error checking done:-
        ~ guesses the value from user input
        ~ sees if the value is provided or not
        ~ prevents wrong keystrokes'''

    def _key_validate(self, proposed, action, **kwargs):
        valid = True
        # if the user tries to delete, just clear the field
        if action == '0':
            self.set('')
            return True

        # get our values list
        values = self.cget('values')
        # Do a case-insensitive match against the entered text
        matching = [
            x for x in values
            if x.lower().startswith(proposed.lower())
        ]

        if len(matching) == 0:
            valid = False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            valid = False

        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        if not self.get():
            valid = False
            self.error.set("A value is required")
        return valid
