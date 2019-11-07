from .model import Model
from .view import View


class Controller:
    def update_model_graph(self):
        self.model.set_var('x0', float(self.view.xy_page.x0_var.get()))
        self.model.set_var('y0', float(self.view.xy_page.y0_var.get()))
        self.model.set_var('grid_size', float(self.view.xy_page.gridsize_var.get()))
        self.model.set_var('step', float(self.view.xy_page.step_var.get()))

    def update_model_step(self):
        self.model.set_var('s0', float(self.view.step_page.s0_var.get()))
        self.model.set_var('sf', float(self.view.step_page.sf_var.get()))
        self.model.set_var('sstep', float(self.view.step_page.sstep_var.get()))

    def toggle_error(self):
        self.error_shown = not self.error_shown
        self.view.toggle_error.configure(text='Show graphs' if self.error_shown else 'Show local errors')
        self.draw_graphs()

    def next_page(self):
        self.view_page = (self.view_page + 1) % 4
        self.draw_graphs()

    def draw_graphs(self):
        if self.view_page == View.GRAPHS:
            self.view.set_title('Graphs')
            self.view.xy_page.tkraise()
            self.view.xy_page.draw_graphs(self.model.get_graphs(),
                                          legend=['Euler', 'Improved Euler', 'Runge-Kutta', 'Exact'])
        elif self.view_page == View.LOCAL_ERRORS:
            self.view.set_title('Local Errors')
            self.view.xy_page.tkraise()
            self.view.xy_page.draw_graphs(self.model.get_local_errors(),
                                          legend=['Euler', 'Improved Euler', 'Runge-Kutta'])
        elif self.view_page == View.GLOBAL_ERRORS:
            self.view.set_title('Global Errors')
            self.view.xy_page.tkraise()
            self.view.xy_page.draw_graphs(self.model.get_global_errors(),
                                          legend=['Euler', 'Improved Euler', 'Runge-Kutta'])
        else:
            self.view.set_title('Step to Errors')
            self.view.step_page.tkraise()
            self.view.step_page.draw_graphs(self.model.get_step_errors(),
                                            legend=['Euler', 'Improved Euler', 'Runge-Kutta'],
                                            axes=('1/step', 'error'))


    def __init__(self, root):
        self.model = Model()
        self.model.add_callback('x0', self.draw_graphs)
        self.model.add_callback('y0', self.draw_graphs)
        self.model.add_callback('grid_size', self.draw_graphs)
        self.model.add_callback('step', self.draw_graphs)
        self.model.add_callback('s0', self.draw_graphs)
        self.model.add_callback('sf', self.draw_graphs)

        self.view = View(root, self.next_page)
        self.view.xy_page.x0_var.set(self.model.vars['x0'])
        self.view.xy_page.y0_var.set(self.model.vars['y0'])
        self.view.xy_page.gridsize_var.set(self.model.vars['grid_size'])
        self.view.xy_page.step_var.set(self.model.vars['step'])
        self.view.step_page.s0_var.set(self.model.vars['s0'])
        self.view.step_page.sf_var.set(self.model.vars['sf'])
        self.view.step_page.sstep_var.set(self.model.vars['sstep'])

        self.view.xy_page.submit.configure(command=self.update_model_graph)
        self.view.step_page.submit.configure(command=self.update_model_step)
        self.view_page = View.GRAPHS

        self.model.initialize()
        self.next_page()
        # self.view.draw_graphs(self.model.get_graphs())
