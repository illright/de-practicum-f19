from .model import Model
from .view import View


class Controller:
    def draw_graphs(self):
        if self.error_shown:
            self.view.draw_graphs(self.model.get_errors())
        else:
            self.view.draw_graphs(self.model.get_graphs())

    def on_x0_change(self, x0):
        self.view.set_x0(x0)
        self.draw_graphs()

    def on_y0_change(self, y0):
        self.view.set_y0(y0)
        self.draw_graphs()

    def on_grid_size_change(self, grid_size):
        self.view.set_grid_size(grid_size)
        self.draw_graphs()

    def on_step_change(self, step):
        self.view.set_step(step)
        self.draw_graphs()

    def update_model(self):
        self.model.set_var('x0', float(self.view.x0_var.get()))
        self.model.set_var('y0', float(self.view.y0_var.get()))
        self.model.set_var('grid_size', float(self.view.gridsize_var.get()))
        self.model.set_var('step', float(self.view.step_var.get()))

    def toggle_error(self):
        self.error_shown = not self.error_shown
        self.view.toggle_error.configure(text='Show graphs' if self.error_shown else 'Show local errors')
        self.draw_graphs()

    def __init__(self, root):
        self.error_shown = False

        self.model = Model()
        self.model.add_callback('x0', self.on_x0_change)
        self.model.add_callback('y0', self.on_y0_change)
        self.model.add_callback('grid_size', self.on_grid_size_change)
        self.model.add_callback('step', self.on_step_change)

        self.view = View(root)
        self.view.submit.configure(command=self.update_model)
        self.view.toggle_error.configure(command=self.toggle_error)

        self.model.initialize()
        self.view.draw_graphs(self.model.get_graphs())
