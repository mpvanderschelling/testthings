# # -*- coding: utf-8 -*-

import numpy as np
import pytest
from f3dasm.sampling.randomuniform import RandomUniform
from f3dasm.sampling.latinhypercube import LatinHypercube
from f3dasm.sampling.sobolsequence import SobolSequencing

from f3dasm.src.designofexperiments import DoE
from f3dasm.src.space import CategoricalSpace, ContinuousSpace, DiscreteSpace


@pytest.fixture
def design():
    # Define the parameters
    x1 = ContinuousSpace(name="x1", lower_bound=2.4, upper_bound=10.3)
    x2 = DiscreteSpace(name="x2", lower_bound=5, upper_bound=80)
    x3 = ContinuousSpace(name="x3", lower_bound=10.0, upper_bound=380.3)
    x4 = CategoricalSpace(name="x4", categories=["test1", "test2", "test3"])
    x5 = ContinuousSpace(name="x5", lower_bound=0.6, upper_bound=7.3)

    # Create the design space
    space = [x1, x2, x3, x4, x5]
    design = DoE(space)
    return design


# Random Uniform Sampling


def test_correct_randomuniform_sampling(design: DoE):
    seed = 42

    # Construct sampler
    random_uniform = RandomUniform(doe=design, seed=seed)

    numsamples = 5

    ground_truth_samples = np.array(
        [
            [5.35886694, 362.04950766, 5.50435941],
            [7.12940203, 67.77370256, 1.64516329],
            [2.85886054, 330.74502678, 4.62747058],
            [7.99377336, 17.62243824, 7.09839601],
            [8.97629686, 88.62917268, 1.81822728],
        ]
    )
    samples = random_uniform.sample_continuous(numsamples=numsamples, doe=design)

    assert samples == pytest.approx(ground_truth_samples)


def test_correct_latinhypercube_sampling(design: DoE):
    seed = 42

    # Construct sampler
    latin_hypercube = LatinHypercube(doe=design, seed=seed)

    numsamples = 5

    ground_truth_samples = np.array(
        [
            [8.25875467, 95.61474051, 1.58087188],
            [5.65177211, 222.26900536, 2.14903266],
            [4.92588041, 80.40990153, 5.9196792],
            [2.99177339, 233.70448765, 6.20364546],
            [10.03525937, 321.96583454, 4.08549412],
        ]
    )
    samples = latin_hypercube.sample_continuous(numsamples=numsamples, doe=design)
    assert samples == pytest.approx(ground_truth_samples)


def test_correct_sobolsequence_sampling(design):
    seed = 42

    # Construct sampler
    sobol_sequencing = SobolSequencing(doe=design, seed=seed)

    numsamples = 5

    ground_truth_samples = np.array(
        [
            [2.4, 10.0, 0.6],
            [6.35, 195.15, 3.95],
            [8.325, 102.575, 2.275],
            [4.375, 287.725, 5.625],
            [5.3625, 148.8625, 4.7875],
        ]
    )
    samples = sobol_sequencing.sample_continuous(numsamples=numsamples, doe=design)
    print(samples)
    assert samples == pytest.approx(ground_truth_samples)


if __name__ == "__main__":  # pragma: no cover
    pytest.main()
