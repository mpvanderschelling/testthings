from typing import Callable, List
import numpy as np
import pytest
from f3dasm.src.designofexperiments import DoE
from f3dasm.src.space import (
    ContinuousSpace,
    DiscreteSpace,
    CategoricalSpace,
    SpaceInterface,
)
from hypothesis import given, settings
from hypothesis.strategies import integers, floats, text, composite, SearchStrategy


@composite
def design_space(
    draw: Callable[[SearchStrategy[int]], int], min_value: int = 1, max_value: int = 20
):
    number_of_input_parameters = draw(integers(min_value, max_value))
    number_of_output_parameters = draw(integers(min_value, max_value))

    def get_space(number_of_parameters: int) -> List[SpaceInterface]:
        space = []
        for i in range(number_of_parameters):
            parameter: SpaceInterface = np.random.choice(
                a=["ContinuousSpace", "DiscreteSpace", "CategoricalSpace"]
            )
            name = draw(
                text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=10, max_size=10)
            )

            if parameter == "ContinuousSpace":
                lower_bound, upper_bound = (
                    draw(floats(max_value=0.0)),
                    draw(floats(min_value=0.1)),
                )

                space.append(
                    ContinuousSpace(
                        name=name, lower_bound=lower_bound, upper_bound=upper_bound
                    )
                )

            elif parameter == "DiscreteSpace":
                lower_bound, upper_bound = (
                    draw(integers(max_value=0)),
                    draw(integers(min_value=1)),
                )

                space.append(
                    DiscreteSpace(
                        name=name, lower_bound=lower_bound, upper_bound=upper_bound
                    )
                )
            elif parameter == "CategoricalSpace":
                categories = ["test1", "test2"]
                space.append(CategoricalSpace(name=name, categories=categories))

        return space

    design_space = DoE(
        input_space=get_space(number_of_input_parameters),
        output_space=get_space(number_of_output_parameters),
    )
    return design_space


@given(design_space())
@settings(max_examples=10)
def test_check_length_input_when_adding_parameter(design: DoE):
    length_input_space = len(design.input_space)
    parameter = DiscreteSpace(name="test")
    design.add_input_space(space=parameter)
    assert length_input_space + 1 == (len(design.input_space))


if __name__ == "__main__":  # pragma: no cover
    pytest.main()
