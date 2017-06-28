# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
# --------------------------------------------------------------------------
# Name:         InfoBulles
# Purpose:      A class to display a ballon tooltip above a Tkinter widget.
#               Can display an image too.
#
# Author:       Julien Moura (https://github.com/Guts)
# -----------------------------------------------------------------------------

# #############################################################################
# ###### Libraries import #########
# #################################

# Standard library
from tkinter import Toplevel, Label, PhotoImage

# #############################################################################
# ########### Classes #############
# #################################


class ToolTip(Toplevel):
    """Display a text or an image on the mouseover over a tkinter ui widget."""

    def __init__(self, parent=None, message="", image="", time=1000):
        """Create the top level window from the parent widget."""
        Toplevel.__init__(self, parent, bd=1, bg="grey")
        # class variables
        self.time = time
        self.parent = parent
        self.withdraw()             # window can't be resized
        self.overrideredirect(1)    # window without borders
        self.transient()
        # label creation
        l = Label(self, text=message, bg="white", justify="left")
        # update & place
        l.update_idletasks()
        l.pack()
        l.update_idletasks()
        # check if an image has been given
        if image == "":
            pass
        else:
            self.photo = PhotoImage(file=image)
            thumb = Label(self, image=self.photo)
            thumb.pack()
        # get the default width & height
        self.tipwidth = l.winfo_width()
        self.tipheight = l.winfo_height()
        # events handling
        self.parent.bind('<Enter>', self.delay)
        self.parent.bind('<Button-1>', self.undisplay)
        self.parent.bind('<Leave>', self.undisplay)

    def delay(self, event):
        """On attend self.tps avant d'afficher l'infobulle."""
        self.action = self.parent.after(self.time, self.display)
        # End of function
        return event, self.action

    def display(self):
        """Display the ballon tooltip."""
        self.update_idletasks()
        pos_x = self.parent.winfo_rootx() + self.parent.winfo_width() / 2
        pos_y = self.parent.winfo_rooty() + self.parent.winfo_height()
        if pos_x + self.tipwidth > self.winfo_screenwidth():
            pos_x = pos_x - self.winfo_width() - self.tipwidth
        if pos_y + self.tipheight > self.winfo_screenheight():
            pos_y = pos_y - self.winfo_height() - self.tipheight
        self.geometry('+%d+%d' % (pos_x, pos_y))
        self.deiconify()

    def undisplay(self, event):
        """Undisplay the ballon tooltip."""
        self.withdraw()
        self.parent.after_cancel(self.action)


# ############################################################################
# ### Stand alone execution #######
# #################################

if __name__ == '__main__':
    """ test parameters for a stand-alone run """
    from tkinter import Tk, Button
    root = Tk()
    bouton = Button(root, text="Test tooltip")
    bouton.pack()
    ToolTip(bouton, message="Oh a nice tooltip!")
    root.mainloop()
