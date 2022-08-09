import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, field

from ..base.design import DesignSpace


@dataclass
class Data:
    """Class that contains data

    Args:
        data (DataFrame): data stored in a DataFrame
    """

    designspace: DesignSpace
    data: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.data = self.designspace.get_empty_dataframe()

    def reset_data(self) -> None:
        self.__post_init__()

    def show(self) -> None:
        print(self.data)
        return

    def add(self, data: pd.DataFrame, ignore_index: bool = False) -> None:
        """Add data

        Args:
            data (pd.DataFrame): data to append
        """
        self.data = pd.concat([self.data, data], ignore_index=ignore_index)

        # Apparently you need to cast the types again
        # TODO: Breaks if values are NaN or infinite
        self.data = self.data.astype(self.designspace.cast_types_dataframe(self.designspace.input_space, "input"))
        self.data = self.data.astype(self.designspace.cast_types_dataframe(self.designspace.output_space, "output"))

    def add_output(self, output: np.ndarray, label: str) -> None:
        self.data[("output", label)] = output

    def add_numpy_arrays(self, input: np.ndarray, output: np.ndarray) -> None:
        df = pd.DataFrame(np.hstack((input, output)), columns=self.data.columns)
        self.add(df, ignore_index=True)

    def get_input_data(self) -> pd.DataFrame:
        return self.data["input"]

    def get_output_data(self) -> pd.DataFrame:
        return self.data["output"]

    def get_n_best_output_samples(self, nosamples: int) -> pd.DataFrame:
        return self.data.nsmallest(n=nosamples, columns=self.designspace.get_output_names())

    def get_n_best_input_parameters_numpy(self, nosamples: int) -> np.ndarray:
        return self.get_n_best_output_samples(nosamples)["input"].to_numpy()

    def get_number_of_datapoints(self) -> int:
        return len(self.data)

    def plot(self, input_par1: str, input_par2: str = None, output_par: str = None) -> None:
        """Plot the data of two parameters in a figure

        Args:
            input_par1 (str): name of first parameter (x-axis)
            input_par2 (str): name of second parameter (x-axis)
            output_par (str): name of output parameter (y-axis)
        """
        fig, ax = plt.figure(), plt.axes()

        ax.scatter(self.data[("input", input_par1)], self.data[("input", input_par2)], s=3)

        ax.set_xlabel(input_par1)
        ax.set_ylabel(input_par2)

        fig.show()

    def plot_pairs(self):
        import seaborn as sb

        sb.pairplot(data=self.get_input_data())