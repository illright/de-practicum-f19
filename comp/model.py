# y' = 2x^3 + 2y/x
y_prime = lambda y, x: 2 * (x ** 3) + 2 * y / x
# y = x^4 + x^2
y_exact = lambda x: x ** 4 + x ** 2


class DENumericalMethod:
    def __init__(self, derivative_expr):
        self.derivative_expr = derivative_expr

    def compute(self, x0, y0, x_limit, step):
        raise NotImplemented('Override this method in child classes.')


class Euler(DENumericalMethod):
    def compute(self, x0, y0, x_limit, step):
        x = x0
        y = y0
        xs = [x]
        ys = [y]

        while x < x_limit:
            y += self.derivative_expr(y, x) * step
            x += step
            xs.append(x)
            ys.append(y)

        return xs, ys


class ImprovedEuler(DENumericalMethod):
    def compute(self, x0, y0, x_limit, step):
        x = x0
        y = y0
        xs = [x]
        ys = [y]
        while x < x_limit:
            k1 = self.derivative_expr(y, x)
            k2 = self.derivative_expr(y + step * k1, x + step)
            x += step
            y += step / 2 * (k1 + k2)
            xs.append(x)
            ys.append(y)

        return xs, ys


class RungeKutta(DENumericalMethod):
    def compute(self, x0, y0, x_limit, step):
        x = x0
        y = y0
        xs = [x]
        ys = [y]

        while x < x_limit:
            k1 = self.derivative_expr(y, x)
            k2 = self.derivative_expr(y + step * k1 / 2, x + step / 2)
            k3 = self.derivative_expr(y + step * k2 / 2, x + step / 2)
            k4 = self.derivative_expr(y + step * k3, x + step)

            y += (k1 + k2 * 2 + k3 * 2 + k4) * step / 6
            x += step

            xs.append(x)
            ys.append(y)

        return xs, ys


class Exact:
    def __init__(self, exact_expr):
        self.exact_expr = exact_expr

    def compute(self, x0, y0, x_limit, step):
        x = x0
        xs = [x]
        ys = [y0]

        while x < x_limit:
            x += step
            xs.append(x)
            ys.append(self.exact_expr(x))

        return xs, ys


class Model:
    '''The data model. Keeps the most up-to-date state of data, alerts the controller
    about any changes to handle in the view.'''
    
    def __init__(self):
        self.vars = {
            'x0': 1,
            'y0': 2,
            'grid_size': 10,
            'step': 1,
        }

        self.callbacks = {
            'x0': [],
            'y0': [],
            'grid_size': [],
            'step': [],
        }

        self.euler = Euler(y_prime)
        self.imp_euler = ImprovedEuler(y_prime)
        self.runge_kutta = RungeKutta(y_prime)
        self.exact = Exact(y_exact)

    def add_callback(self, var_name, callback):
        if var_name not in self.vars:
            raise ValueError(f'No such variable `{var_name}`')

        self.callbacks[var_name].append(callback)

    def set_var(self, var_name, value):
        old_value = self.vars[var_name]
        if value == old_value:
            return

        self.vars[var_name] = value
        for callback in self.callbacks[var_name]:
            callback(self.vars[var_name])

    def _do_callbacks(self):
        for var, callbacks in self.callbacks.items():
            for callback in callbacks:
                callback(self.vars[var])

    def initialize(self):
        self._do_callbacks()

    def get_graphs(self):
        graphs = []
        for method in (self.euler, self.imp_euler, self.runge_kutta, self.exact):
            graphs.append(method.compute(self.vars['x0'],
                                         self.vars['y0'],
                                         self.vars['x0'] + self.vars['grid_size'],
                                         self.vars['step']))

        return graphs

    def get_errors(self):
        graphs = []
        xs, exact = self.exact.compute(self.vars['x0'],
                                       self.vars['y0'],
                                       self.vars['x0'] + self.vars['grid_size'],
                                       self.vars['step'])

        for method in (self.euler, self.imp_euler, self.runge_kutta, self.exact):
            _, points = method.compute(self.vars['x0'],
                                       self.vars['y0'],
                                       self.vars['x0'] + self.vars['grid_size'],
                                       self.vars['step'])
            graphs.append((xs, [abs(ex - act) for ex, act in zip(exact, points)]))

        return graphs
