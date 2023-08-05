"""
Tests for the reflection selection algorithm.
"""
from __future__ import absolute_import, division, print_function
import os
import itertools
from libtbx import phil
from cctbx import sgtbx
from dxtbx.serialize import load
from dials.array_family import flex
from dials.algorithms.scaling.Ih_table import IhTable
from dials.algorithms.scaling.reflection_selection import (
    select_highly_connected_reflections,
    select_connected_reflections_across_datasets,
    select_highly_connected_reflections_in_bin,
    calculate_scaling_subset_ranges_with_E2,
    calculate_scaling_subset_ranges,
)
from dials.algorithms.scaling.scaling_utilities import calc_crystal_frame_vectors


def test_select_highly_connected_reflections_in_bin():
    """Test the single-bin selection algorithm."""
    r1 = flex.reflection_table()
    n_list = [3, 3, 2, 1, 1, 2, 2]
    miller_indices = [[(0, 0, i + 1)] * n for i, n in enumerate(n_list)]
    r1["miller_index"] = flex.miller_index(
        list(itertools.chain.from_iterable(miller_indices))
    )
    r1["class_index"] = flex.int([0, 1, 1, 0, 1, 2, 0, 0, 2, 1, 1, 2, 0, 1])
    r1["intensity"] = flex.double(sum(n_list), 1)
    r1["variance"] = flex.double(sum(n_list), 1)
    r1["inverse_scale_factor"] = flex.double(sum(n_list), 1)

    sg = sgtbx.space_group("P1")
    Ih_table_block = IhTable([r1], sg).Ih_table_blocks[0]
    Ih_table_block.Ih_table["class_index"] = r1["class_index"].select(
        Ih_table_block.Ih_table["loc_indices"]
    )

    indices, total_in_classes = select_highly_connected_reflections_in_bin(
        Ih_table_block, min_per_class=2, min_total=6, max_total=100
    )
    assert list(total_in_classes) == [2, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert list(indices) == [0, 1, 2, 3, 4, 5, 10, 11]


def test_select_connected_reflections_across_datasets():
    """Test the basic cross-dataset reflection selection algorithm.

    Make three reflection tables with the following reflections:
               symmetry groups
               0  1  2  3  4  5  6
            0  3  3  2  0  1  1  1
    classes 1  0  2  0  0  3  2  1
            2  2  1  1  5  0  4  0

    With target=5, expect:
    number of chosen reflections per class: [8, 7, 7]
    symmetry groups used:                   [1, 5, 0, 4]
    """

    n1 = [3, 3, 2, 0, 1, 1, 1]
    n2 = [0, 2, 0, 0, 3, 2, 1]
    n3 = [2, 1, 1, 5, 0, 4, 0]

    def make_refl_table(n_list, class_idx=0):
        """Make a reflection table with groups based on n_list."""
        r1 = flex.reflection_table()
        miller_indices = [[(0, 0, i + 1)] * n for i, n in enumerate(n_list)]
        r1["miller_index"] = flex.miller_index(
            list(itertools.chain.from_iterable(miller_indices))
        )
        r1["intensity"] = flex.double(sum(n_list), 1)
        r1["variance"] = flex.double(sum(n_list), 1)
        r1["inverse_scale_factor"] = flex.double(sum(n_list), 1)
        r1["class_index"] = flex.int(sum(n_list), class_idx)
        return r1

    reflections = [
        make_refl_table(n1, 0),
        make_refl_table(n2, 1),
        make_refl_table(n3, 2),
    ]

    space_group = sgtbx.space_group("P1")
    table = IhTable(reflections, space_group)
    indices, datset_ids, total_in_classes = select_connected_reflections_across_datasets(
        table, min_per_class=5, Isigma_cutoff=0.0
    )
    assert list(total_in_classes) == [8, 7, 7]
    assert list(indices) == [0, 1, 2, 3, 4, 5, 8, 9] + [0, 1, 2, 3, 4, 5, 6] + [
        0,
        1,
        2,
        9,
        10,
        11,
        12,
    ]
    assert list(datset_ids) == [0] * 8 + [1] * 7 + [2] * 7


def generated_param():
    """Generate a param phil scope."""
    phil_scope = phil.parse(
        """
      include scope dials.algorithms.scaling.scaling_options.phil_scope
  """,
        process_includes=True,
    )
    param = phil_scope.extract()
    return param


def generated_refl_for_subset_calculation():
    """Create a reflection table suitable for splitting into blocks."""
    reflections = flex.reflection_table()
    reflections["intensity"] = flex.double([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    reflections["variance"] = flex.double(6, 1.0)
    reflections["d"] = flex.double([0.8, 2.1, 2.0, 1.4, 1.6, 2.5])
    reflections["partiality"] = flex.double(6, 1.0)
    reflections.set_flags(flex.bool(6, True), reflections.flags.integrated)
    reflections.set_flags(flex.bool(6, False), reflections.flags.bad_for_scaling)
    return reflections


def test_selection_scaling_subset_ranges_with_E2():
    """Test the scaling subset calculation with E2 range."""
    test_params = generated_param()
    rt = generated_refl_for_subset_calculation()
    rt["Esq"] = flex.double([1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    test_params.reflection_selection.E2_range = 0.8, 5.0
    test_params.reflection_selection.d_range = 1.0, 5.0  # all but first
    test_params.reflection_selection.Isigma_range = 0.9, 5.5  # all but last
    sel = calculate_scaling_subset_ranges_with_E2(rt, test_params)
    assert list(sel) == [False, True, True, True, True, False]
    rt["Esq"] = flex.double([1.0, 1.0, 1.0, 0.1, 6.0, 1.0])
    sel = calculate_scaling_subset_ranges_with_E2(rt, test_params)
    assert list(sel) == [False, True, True, False, False, False]


def test_selection_scaling_subset_ranges():
    """Test the scaling subset calculation with E2 range."""
    test_params = generated_param()
    rt = generated_refl_for_subset_calculation()
    test_params.reflection_selection.E2_range = 0.8, 5.0
    test_params.reflection_selection.d_range = 1.0, 5.0  # all but first
    test_params.reflection_selection.Isigma_range = 0.9, 5.5  # all but last
    sel = calculate_scaling_subset_ranges(rt, test_params)
    assert list(sel) == [False, True, True, True, True, False]


def test_reflection_selection(dials_regression):
    """Use a real dataset to test the selection algorithm."""
    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path = os.path.join(data_dir, "20_integrated_experiments.json")
    reflection_table = flex.reflection_table.from_pickle(pickle_path)
    experiment = load.experiment_list(sweep_path, check_format=False)[0]

    reflection_table["intensity"] = reflection_table["intensity.sum.value"]
    reflection_table["variance"] = reflection_table["intensity.sum.variance"]
    reflection_table["inverse_scale_factor"] = flex.double(reflection_table.size(), 1.0)
    reflection_table = reflection_table.select(reflection_table["variance"] > 0)
    reflection_table = reflection_table.select(
        reflection_table.get_flags(reflection_table.flags.integrated, all=True)
    )

    Ih_table_block = IhTable(
        [reflection_table], experiment.crystal.get_space_group()
    ).Ih_table_blocks[0]

    reflection_table["phi"] = (
        reflection_table["xyzobs.px.value"].parts()[2]
        * experiment.scan.get_oscillation()[1]
    )
    reflection_table = calc_crystal_frame_vectors(reflection_table, experiment)
    Ih_table_block.Ih_table["s1c"] = reflection_table["s1c"].select(
        Ih_table_block.Ih_table["loc_indices"]
    )

    indices = select_highly_connected_reflections(
        Ih_table_block, experiment, min_per_area=10, n_resolution_bins=10
    )
    assert len(indices) > 1710 and len(indices) < 1800

    # Give a high min_per_area to check that all reflections with multiplciity > 1
    # are selected.
    indices = select_highly_connected_reflections(
        Ih_table_block, experiment, min_per_area=50, n_resolution_bins=10
    )
    # this dataset has 48 reflections with multiplicity = 1
    assert len(indices) == reflection_table.size() - 48
