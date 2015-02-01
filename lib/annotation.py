__author__ = 'kulkarnik'

from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import csv

class Annotate(object):
    def __init__(self,scatterplot,toolbar,listbox,x_points,y_points,names,colors,seqs,dir):
        self.path = dir + '/selected.fas'
        self.x_points = x_points
        self.y_points = y_points
        self.names = names
        self.selectedpoints = []
        self.selectedseqs = []
        self.scatter = scatterplot
        self.toolbar = toolbar
        self.listbox = listbox
        self.colors = colors
        self.seqs = seqs
        self.thecolors = []

        for (i, name) in enumerate(self.names):
            self.thecolors.append(self.colors[i])

        self.scatter.scatter(self.x_points, self.y_points,c=self.thecolors,picker=2)

        self.rect = Rectangle((0,0), 0, 0,facecolor='grey', alpha=0.3)
        self.scatter.add_patch(self.rect)
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.isPressed = False

        self.scatter.figure.canvas.draw()
        self.connect()



    def on_press(self, event):
        if self.toolbar._active is None:
            self.isPressed = True
            self.x0 = event.xdata
            self.y0 = event.ydata

    def on_motion(self,event):
        if self.isPressed:
            self.x1 = event.xdata
            self.y1 = event.ydata
            try:
                self.rect.set_width(self.x1 - self.x0)
                self.rect.set_height(self.y1 - self.y0)
            except TypeError:
                pass
            self.rect.set_xy((self.x0, self.y0))
            self.scatter.figure.canvas.draw()

    def on_release(self, event):

        if self.toolbar._active is None:
            self.isPressed = False
            self.x1 = event.xdata
            self.y1 = event.ydata
            lowerx = min(self.x0,self.x1)
            upperx = max(self.x0,self.x1)
            lowery = min(self.y0,self.y1)
            uppery = max(self.y0,self.y1)

            for i, point in enumerate(self.x_points):
                if (lowerx < self.x_points[i] and self.x_points[i] < upperx and
                            uppery > self.y_points[i] and self.y_points[i] > lowery):
                    if not self.names[i] in self.selectedpoints:
                        self.selectedpoints.append(str(self.names[i]))
                        self.selectedseqs.append(self.seqs[i]+','+str(self.colors[i]))
                        self.listbox.insert(END,str(self.names[i])+','+str(self.colors[i]))

        self.rect.set_width(0)
        self.rect.set_height(0)
        self.rect.set_xy((self.x0, self.y0))
        try:
            self.scatter.figure.canvas.draw()
        except TypeError:
            pass


    def on_pick(self, mouseevent):

        if self.toolbar._active is None:
            self.isPressed = False
            self.ind = mouseevent.ind
            self.x1 = np.take(self.x_points,self.ind)
            self.y1 = np.take(self.y_points,self.ind)
        for i, point in enumerate(self.x_points):
            for x in self.x1:
                for y in self.y1:
                    if (x == self.x_points[i] and y == self.y_points[i]):
                        if not self.names[i] in self.selectedpoints:
                            self.selectedpoints.append(str(self.names[i]))
                            self.selectedseqs.append(self.seqs[i]+','+str(self.colors[i]))
                            self.listbox.insert(END,str(self.names[i])+','+str(self.colors[i]))


    def on_key(self,event):
        if event.key == 'escape':
            self.selectedpoints = []
            self.selectedseqs = []
            self.listbox.delete(0, END)

        if event.key == 'r':
            print "Showing all selected points"

        if event.key == 'c':
            self.scatter.clear()
            new_x = []
            new_y = []
            new_colors = []
            for (i, name) in enumerate(self.names):
                if str(self.names[i]) in self.selectedpoints:
                    new_x.append(self.x_points[i])
                    new_y.append(self.y_points[i])
                    new_colors.append(self.colors[i])

            self.scatter.scatter(new_x, new_y,c=new_colors,picker=2)
            self.scatter.add_patch(self.rect)
            self.scatter.figure.canvas.draw()

        if event.key == 'a':
            self.scatter.clear()
            self.scatter.scatter(self.x_points,self.y_points,picker=2,c=self.thecolors)
            self.scatter.add_patch(self.rect)
            self.scatter.figure.canvas.draw()

        if event.key == 's':
            with open(self.path, "w") as exportfile:
                for i, name in enumerate(self.selectedpoints):
                    exportfile.write(self.selectedpoints[i] + '\n')
                    exportfile.write(self.selectedseqs[i] + '\n')
            print "Saved to file!"

    def connect(self):
        self.scatter.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.scatter.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.scatter.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.scatter.figure.canvas.mpl_connect('pick_event', self.on_pick)
        self.scatter.figure.canvas.mpl_connect('key_press_event', self.on_key)
        self.scatter.figure.canvas.mpl_connect('button_press_event',
                                               lambda event:self.scatter.figure.canvas._tkcanvas.focus_set())



def tk_window_init(x_points,y_points,names,colors,seqs):

    ## Create Tk main window and assign title and size
    root = Tk()
    root.wm_title("Clustering analysis results")
    root.geometry("1000x700+0+0")

    # Define the quit function used for the Quit Button.
    """# DO NOT USE X TO CLOSE, ONLY USE QUIT"""
    def _quit():
        root.quit()
        root.destroy()

    # Create matplotlib figure and main subplot (ax1)
    fig, ax1 = plt.subplots()
    # Plot points

    ax1.scatter(x_points, y_points,picker=2)
    # Remove axes and labels
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)

    # Create the canvas and place matplotlib figure on canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.show()

    # Create listbox for displaying selected proteins
    listbox = Listbox(master=root,selectmode=EXTENDED)

    # Import toolbar to navigate matplotlib
    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()

    # Create new frame for quit button
    bottomframe = Frame(master=root)

    # Create a scrollbar and attach to listbox
    sb = Scrollbar(master=root,orient=VERTICAL)
    sb.configure(command=listbox.yview)
    listbox.configure(yscrollcommand=sb.set)

    # Pack the components in a reasonable fashion
    toolbar.pack(side=TOP)
    bottomframe.pack(side=BOTTOM)
    canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)
    listbox.pack(side=LEFT,fill=BOTH,expand=1,pady=6,padx=3)
    sb.pack(side=LEFT,fill=Y,pady=6,padx=3)

    # Create quit button
    quitbutton = Button(master=bottomframe, text='Quit', command=_quit)
    quitbutton.pack(side=LEFT)

    return root,ax1,toolbar,listbox