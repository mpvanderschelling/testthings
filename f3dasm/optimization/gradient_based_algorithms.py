import numpy as np

from ..base.optimization import Optimizer
from ..base.function import Function


class RandomSearch(Optimizer):
    """Naive random search"""

    def init_parameters(self):

        # Default hyperparameters
        self.defaults = {"population": 1}

    def update_step(self, function: Function) -> None:
        x_new = np.random.uniform(
            low=function.scale_bounds[0],
            high=function.scale_bounds[1],
            size=(self.hyperparameters["population"], function.dimensionality),
        )

        self.data.add_numpy_arrays(input=x_new, output=function.eval(x_new))


class SGD(Optimizer):
    """Gradient-based Stochastig Gradient Descent (SGD) optimizer"""

    def init_parameters(self):

        # Default hyperparameters
        self.defaults = {"step_size": 1e-2, "population": 1, "force_bounds": True}

    def update_step(self, function: Function) -> None:

        x = self.data.get_input_data().iloc[-self.hyperparameters["population"] :].to_numpy()

        g = function.dfdx(x)

        x_new = x - self.hyperparameters["step_size"] * g

        if self.hyperparameters["force_bounds"]:
            x_new[x_new < function.scale_bounds[0]] = function.scale_bounds[0]
            x_new[x_new > function.scale_bounds[1]] = function.scale_bounds[1]

        self.data.add_numpy_arrays(input=x_new, output=function.eval(x_new))


class Momentum(Optimizer):
    """Gradient-based Momentum optimizer"""

    def init_parameters(self):

        # Default hyperparameters
        self.defaults = {
            "step_size": 1e-2,
            "beta": 0.9,
            "population": 1,
            "force_bounds": True,
        }

        # Dynamic parameters
        self.m = 0

    def update_step(self, function: Function) -> None:

        x = self.data.get_input_data().iloc[-self.hyperparameters["population"] :].to_numpy()

        g = function.dfdx(x)

        m = self.hyperparameters["beta"] * self.m + (1 - self.hyperparameters["beta"]) * g
        x_new = x - self.hyperparameters["step_size"] * m

        if self.hyperparameters["force_bounds"]:
            x_new[x_new < function.scale_bounds[0]] = function.scale_bounds[0]
            x_new[x_new > function.scale_bounds[1]] = function.scale_bounds[1]

        self.data.add_numpy_arrays(input=x_new, output=function.eval(x_new))
        self.m = m


class Adam(Optimizer):
    """Gradient-based Adam optimizer"""

    def init_parameters(self):

        # Default hyperparameters
        self.defaults = {
            "step_size": 1e-2,
            "beta_1": 0.9,
            "beta_2": 0.999,
            "epsilon": 1e-8,
            "population": 1,
            "force_bounds": True,
        }
        # Dynamic parameters
        self.m = 0
        self.v = 0

    def update_step(self, function: Function) -> None:

        x = self.data.get_input_data().iloc[-self.hyperparameters["population"] :].to_numpy()

        g = function.dfdx(x)
        t = self.data.get_number_of_datapoints()
        m = self.hyperparameters["beta_1"] * self.m + (1 - self.hyperparameters["beta_2"]) * g
        v = self.hyperparameters["beta_2"] * self.v + (1 - self.hyperparameters["beta_2"]) * np.power(g, 2)

        m_hat = m / (1 - np.power(self.hyperparameters["beta_1"], t))
        v_hat = v / (1 - np.power(self.hyperparameters["beta_2"], t))
        x_new = x - self.hyperparameters["step_size"] * m_hat / (np.sqrt(v_hat) + self.hyperparameters["epsilon"])

        if self.hyperparameters["force_bounds"]:
            x_new[x_new < function.scale_bounds[0]] = function.scale_bounds[0]
            x_new[x_new > function.scale_bounds[1]] = function.scale_bounds[1]

        self.data.add_numpy_arrays(input=x_new, output=function.eval(x_new))

        self.m = m
        self.v = v
