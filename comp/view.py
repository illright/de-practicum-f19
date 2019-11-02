import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from PIL import Image, ImageTk

style.use('ggplot')
LARGE_FONT = ('Roboto', 12)
EQUATION_PICTURE = 'original_de.png'
EQUATION_W_TO_H = 3
EQUATION_WIDTH = 120


class View:
    '''The data-presenting class. It is tied to the data from the model
    through the controller's callbacks.'''

    def set_x0(self, x0):
        self.x0_var.set(str(x0))

    def set_y0(self, y0):
        self.y0_var.set(str(y0))

    def set_grid_size(self, grid_size):
        self.gridsize_var.set(str(grid_size))

    def set_step(self, step):
        self.step_var.set(str(step))

    def draw_graphs(self, graphs):
        '''Plot the graphs on the canvas. The graphs should be an array of
        four pairs of (xs, ys) array with the points on the corresponding axes'''
        self.plot.clear()

        for xs, ys in graphs:
            self.plot.plot(xs, ys)

        self.plot.legend(['Euler', 'Improved Euler', 'Runge-Kutta', 'Exact'])
        self.canvas.draw()

    def __init__(self, root):
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.fig.add_subplot(111)

        root.title('Computational Practicum')
        root.configure(background='white')

        top_frame = tk.Frame(root)
        top_frame.configure(background='white')
        top_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        eq_label = tk.Label(top_frame, text='Original Equation:', font=LARGE_FONT)
        eq_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=15)
        eq_label.configure(background='white')

        img_size = (EQUATION_WIDTH, EQUATION_WIDTH // EQUATION_W_TO_H)
        img = ImageTk.PhotoImage(Image.open(EQUATION_PICTURE).resize(img_size,
                                                                     Image.ANTIALIAS))
        equation = tk.Label(top_frame, image=img)
        equation.image = img
        equation.grid(row=1, column=0, columnspan=2, pady=5, padx=10)

        self.canvas = FigureCanvasTkAgg(self.fig, root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        x0_label = tk.Label(top_frame, text="x0", font=LARGE_FONT)
        x0_label.grid(row=2, column=0, sticky='e', padx=5)
        x0_label.configure(background='white')

        self.x0_var = tk.StringVar(top_frame)
        self.x0_textbox = tk.Entry(top_frame, width=5, textvariable=self.x0_var)
        self.x0_textbox.grid(row=2, column=1, pady=15)

        y0_label = tk.Label(top_frame, text="y0", font=LARGE_FONT)
        y0_label.grid(row=3, column=0, sticky='e', padx=5)
        y0_label.configure(background='white')

        self.y0_var = tk.StringVar(top_frame)
        self.y0_textbox = tk.Entry(top_frame, width=5, textvariable=self.y0_var)
        self.y0_textbox.grid(row=3, column=1)

        gridsize_label = tk.Label(top_frame, text='Grid Size', font=LARGE_FONT)
        gridsize_label.grid(row=4, column=0, padx=5, sticky='e')
        gridsize_label.configure(background='white')

        self.gridsize_var = tk.StringVar(top_frame)
        self.gridsize_textbox = tk.Entry(top_frame, width=5, textvariable=self.gridsize_var)
        self.gridsize_textbox.grid(row=4, column=1, pady=15)

        step_label = tk.Label(top_frame, text='Step', font=LARGE_FONT)
        step_label.grid(row=5, column=0, padx=5, sticky='e')
        step_label.configure(background='white')

        self.step_var = tk.StringVar(top_frame)
        self.step_textbox = tk.Entry(top_frame, width=5, textvariable=self.step_var)
        self.step_textbox.grid(row=5, column=1, pady=15)

        self.submit = tk.Button(top_frame, text='Set')
        self.submit.grid(row=6, column=0, columnspan=2, pady=15)

        self.toggle_error = tk.Button(top_frame, text='Show local errors')
        self.toggle_error.grid(row=7, column=0, columnspan=2, pady=30)
