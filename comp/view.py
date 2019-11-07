import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from PIL import Image, ImageTk

style.use('ggplot')
LARGE_FONT = ('Roboto', 12)
EQUATION_PICTURE = 'original_de.png'
EQUATION_W_TO_H = 3
EQUATION_WIDTH = 120


class GraphPage(tk.Frame):
    def draw_graphs(self, graphs, legend=None, axes=('x', 'y')):
        '''Plot the graphs on the canvas. The graphs should be an array of
        four pairs of (xs, ys) array with the points on the corresponding axes'''
        self.plot.clear()

        for xs, ys in graphs:
            self.plot.plot(xs, ys)

        if legend is not None:
            self.plot.legend(legend)

        self.plot.set_xlabel(axes[0])
        self.plot.set_ylabel(axes[1])
        self.canvas.draw()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.fig.add_subplot(111)


class XYPage(GraphPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(background='white')

        controls = tk.Frame(self)
        controls.configure(background='white')
        controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        eq_label = tk.Label(controls, text='Original Equation:', font=LARGE_FONT)
        eq_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=15)
        eq_label.configure(background='white')

        img_size = (EQUATION_WIDTH, EQUATION_WIDTH // EQUATION_W_TO_H)
        img = ImageTk.PhotoImage(Image.open(EQUATION_PICTURE).resize(img_size,
                                                                     Image.ANTIALIAS))
        equation = tk.Label(controls, image=img)
        equation.image = img
        equation.grid(row=1, column=0, columnspan=2, pady=5, padx=10)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        x0_label = tk.Label(controls, text="x0", font=LARGE_FONT)
        x0_label.grid(row=2, column=0, sticky='e', padx=5)
        x0_label.configure(background='white')

        self.x0_var = tk.StringVar(controls)
        x0_textbox = tk.Entry(controls, width=5, textvariable=self.x0_var)
        x0_textbox.grid(row=2, column=1, pady=15)

        y0_label = tk.Label(controls, text="y0", font=LARGE_FONT)
        y0_label.grid(row=3, column=0, sticky='e', padx=5)
        y0_label.configure(background='white')

        self.y0_var = tk.StringVar(controls)
        y0_textbox = tk.Entry(controls, width=5, textvariable=self.y0_var)
        y0_textbox.grid(row=3, column=1)

        gridsize_label = tk.Label(controls, text='Grid Size', font=LARGE_FONT)
        gridsize_label.grid(row=4, column=0, padx=5, sticky='e')
        gridsize_label.configure(background='white')

        self.gridsize_var = tk.StringVar(controls)
        gridsize_textbox = tk.Entry(controls, width=5, textvariable=self.gridsize_var)
        gridsize_textbox.grid(row=4, column=1, pady=15)

        step_label = tk.Label(controls, text='Step', font=LARGE_FONT)
        step_label.grid(row=5, column=0, padx=5, sticky='e')
        step_label.configure(background='white')

        self.step_var = tk.StringVar(controls)
        step_textbox = tk.Entry(controls, width=5, textvariable=self.step_var)
        step_textbox.grid(row=5, column=1, pady=15)

        self.submit = ttk.Button(controls, text='Set')
        self.submit.grid(row=6, column=0, columnspan=2, pady=15)

        self.next_page = ttk.Button(controls, text='Next page')
        self.next_page.grid(row=7, column=0, columnspan=2, pady=15)


class StepPage(GraphPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(background='white')

        controls = tk.Frame(self)
        controls.configure(background='white')
        controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        eq_label = tk.Label(controls, text='Original Equation:', font=LARGE_FONT)
        eq_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=15)
        eq_label.configure(background='white')

        img_size = (EQUATION_WIDTH, EQUATION_WIDTH // EQUATION_W_TO_H)
        img = ImageTk.PhotoImage(Image.open(EQUATION_PICTURE).resize(img_size,
                                                                     Image.ANTIALIAS))
        equation = tk.Label(controls, image=img)
        equation.image = img
        equation.grid(row=1, column=0, columnspan=2, pady=5, padx=10)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        s0_label = tk.Label(controls, text="1/step initial", font=LARGE_FONT)
        s0_label.grid(row=2, column=0, sticky='e', padx=5)
        s0_label.configure(background='white')

        self.s0_var = tk.StringVar(controls)
        s0_textbox = tk.Entry(controls, width=5, textvariable=self.s0_var)
        s0_textbox.grid(row=2, column=1, pady=15)

        sf_label = tk.Label(controls, text="1/step final", font=LARGE_FONT)
        sf_label.grid(row=3, column=0, sticky='e', padx=5)
        sf_label.configure(background='white')

        self.sf_var = tk.StringVar(controls)
        sf_textbox = tk.Entry(controls, width=5, textvariable=self.sf_var)
        sf_textbox.grid(row=3, column=1)

        sstep_label = tk.Label(controls, text="Step step", font=LARGE_FONT)
        sstep_label.grid(row=4, column=0, sticky='e', padx=5)
        sstep_label.configure(background='white')

        self.sstep_var = tk.StringVar(controls)
        sstep_textbox = tk.Entry(controls, width=5, textvariable=self.sstep_var)
        sstep_textbox.grid(row=4, column=1)

        self.submit = ttk.Button(controls, text='Set')
        self.submit.grid(row=6, column=0, columnspan=2, pady=15)

        self.next_page = ttk.Button(controls, text='Next page')
        self.next_page.grid(row=7, column=0, columnspan=2, pady=15)


class View:
    '''The data-presenting class. It is tied to the data from the model
    through the controller's callbacks.'''
    GRAPHS = 0
    GLOBAL_ERRORS = 1
    LOCAL_ERRORS = 2
    STEP_ERRORS = 3

    def set_title(self, title):
        self.root.title(title)

    def __init__(self, root, next_page):
        self.root = root
        
        self.xy_page = XYPage(root)
        self.xy_page.next_page.configure(command=next_page)
        self.xy_page.grid(row=0, column=0, sticky='nsew')

        self.step_page = StepPage(root)
        self.step_page.next_page.configure(command=next_page)
        self.step_page.grid(row=0, column=0, sticky='nsew')
