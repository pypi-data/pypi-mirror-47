"""
Test the command line script dials.scale, for successful completion.
"""

from __future__ import absolute_import, division, print_function

import json
import os
import pytest

from libtbx import easy_run, phil
from dials.util import Sorry
from dxtbx.serialize import load, dump
from dxtbx.model.experiment_list import ExperimentList
from dxtbx.model import Crystal, Scan, Beam, Goniometer, Detector, Experiment
from dials.array_family import flex
from dials.util.options import OptionParser
from dials.command_line.scale import Script
from dials.algorithms.scaling.scaling_library import scaled_data_as_miller_array
from dials.algorithms.scaling.scaling_utilities import DialsMergingStatisticsError
import procrunner


def run_delta_cchalf(pickle_path_list, sweep_path_list, extra_args):
    """Run dials.compute_delta_cchalf"""
    args = (
        ["dials.compute_delta_cchalf"]
        + pickle_path_list
        + sweep_path_list
        + extra_args
        + [
            "output.reflections=filtered_reflections.pickle",
            "output.experiments=filtered_experiments.json",
        ]
    )
    command = " ".join(args)
    print(command)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("filtered_experiments.json")
    assert os.path.exists("filtered_reflections.pickle")


def run_one_scaling(pickle_path_list, sweep_path_list, extra_args):
    """Run the dials.scale algorithm."""
    args = ["dials.scale"] + pickle_path_list + sweep_path_list + extra_args
    command = " ".join(args)
    print(command)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")
    assert os.path.exists("scaling.html")

    table = flex.reflection_table.from_pickle("scaled.pickle")

    assert "inverse_scale_factor" in table
    assert "inverse_scale_factor_variance" in table


def get_merging_stats(
    scaled_unmerged_mtz,
    anomalous=False,
    n_bins=20,
    use_internal_variance=False,
    eliminate_sys_absent=False,
    data_labels=None,
):
    import iotbx.merging_statistics

    i_obs = iotbx.merging_statistics.select_data(
        scaled_unmerged_mtz, data_labels=data_labels
    )
    i_obs = i_obs.customized_copy(anomalous_flag=False, info=i_obs.info())
    result = iotbx.merging_statistics.dataset_statistics(
        i_obs=i_obs,
        n_bins=n_bins,
        anomalous=anomalous,
        use_internal_variance=use_internal_variance,
        eliminate_sys_absent=eliminate_sys_absent,
    )
    return result


def generated_exp(n=1):
    """Generate an experiment list with two experiments."""
    experiments = ExperimentList()
    exp_dict = {
        "__id__": "crystal",
        "real_space_a": [1.0, 0.0, 0.0],
        "real_space_b": [0.0, 1.0, 0.0],
        "real_space_c": [0.0, 0.0, 2.0],
        "space_group_hall_symbol": " C 2y",
    }
    crystal = Crystal.from_dict(exp_dict)
    scan = Scan(image_range=[0, 90], oscillation=[0.0, 1.0])
    beam = Beam(s0=(0.0, 0.0, 1.01))
    goniometer = Goniometer((1.0, 0.0, 0.0))
    detector = Detector()
    experiments.append(
        Experiment(
            beam=beam,
            scan=scan,
            goniometer=goniometer,
            detector=detector,
            crystal=crystal,
        )
    )
    if n > 1:
        for _ in range(n - 1):
            experiments.append(
                Experiment(
                    beam=beam,
                    scan=scan,
                    goniometer=goniometer,
                    detector=detector,
                    crystal=crystal,
                )
            )
    return experiments


def generated_param():
    """Generate the default scaling parameters object."""
    phil_scope = phil.parse(
        """
      include scope dials.command_line.scale.phil_scope
  """,
        process_includes=True,
    )

    optionparser = OptionParser(phil=phil_scope, check_format=False)
    parameters, _ = optionparser.parse_args(
        args=[], quick_parse=True, show_diff_phil=False
    )
    return parameters


def test_reflections():
    reflections = flex.reflection_table()
    reflections["intensity.sum.value"] = flex.double([1.0, 2.0, 3.0, 4.0])
    reflections["intensity.sum.variance"] = flex.double([1.0, 2.0, 3.0, 4.0])
    reflections["miller_index"] = flex.miller_index(
        [(0, 0, 1), (0, 0, 1), (0, 0, 2), (0, 0, 2)]
    )
    reflections["xyzobs.px.value"] = flex.vec3_double(
        [(0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4)]
    )
    reflections["id"] = flex.int([0, 0, 0, 0])
    return reflections


def generate_test_input(n=1):
    reflections = []
    for _ in range(n):
        reflections.append(test_reflections())
    return generated_param(), generated_exp(n), reflections


def return_first_arg_side_effect(*args):
    """Side effect for overriding the call to reject_outliers."""
    return args[0]


def test_scale_merging_stats():
    """Test the merging stats method of dials.scale script"""
    params = generated_param()
    exp = generated_exp()
    reflections = flex.reflection_table()
    reflections["intensity.scale.value"] = flex.double([1.0, 2.0, 3.0, 4.0])
    reflections["intensity.scale.variance"] = flex.double([1.0, 2.0, 3.0, 4.0])
    reflections["miller_index"] = flex.miller_index(
        [(0, 0, 1), (0, 0, 1), (0, 0, 2), (0, 0, 2)]
    )
    reflections["id"] = flex.int([0, 0, 0, 0])
    reflections["inverse_scale_factor"] = flex.double([0.5, 0.4, 0.9, 1.0])
    reflections["xyzobs.px.value"] = flex.vec3_double(
        [(0, 0, 0.5), (0, 0, 1.5), (0, 0, 2.5), (0, 0, 3.5)]
    )
    reflections.set_flags(flex.bool(4, False), reflections.flags.bad_for_scaling)
    params.output.merging.nbins = 1
    scaled_array = scaled_data_as_miller_array([reflections], exp)
    merging_statistics_result = Script.merging_stats_from_scaled_array(
        scaled_array, params
    )
    assert merging_statistics_result is not None

    # test for sensible return if small dataset with no equivalent reflections
    reflections["miller_index"] = flex.miller_index(
        [(0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4)]
    )
    scaled_array = scaled_data_as_miller_array([reflections], exp)
    with pytest.raises(DialsMergingStatisticsError):
        _ = Script.merging_stats_from_scaled_array(scaled_array, params)


def test_scale_script_prepare_input():
    """Test prepare_input method of scaling script."""

    # test the components of the scaling script directly with a test reflection
    # table, experiments list and params.

    params, exp, reflections = generate_test_input()
    # try to pass in unequal number of reflections and experiments
    reflections.append(test_reflections())
    with pytest.raises(Sorry):
        script = Script(params, exp, reflections)

    params, exp, reflections = generate_test_input()
    # Try to use use_datasets when not identifiers set
    params.dataset_selection.use_datasets = ["0"]
    with pytest.raises(Sorry):
        script = Script(params, exp, reflections)
    # Try to use use_datasets when not identifiers set
    params.dataset_selection.use_datasets = None
    params.dataset_selection.exclude_datasets = ["0"]
    with pytest.raises(Sorry):
        _ = Script(params, exp, reflections)

    # Now make two experiments with identifiers and select on them
    params, exp, reflections = generate_test_input(n=2)
    exp[0].identifier = "0"
    reflections[0].experiment_identifiers()[0] = "0"
    exp[1].identifier = "1"
    reflections[1].experiment_identifiers()[0] = "1"
    list1 = ExperimentList().append(exp[0])
    list2 = ExperimentList().append(exp[1])
    reflections[0].assert_experiment_identifiers_are_consistent(list1)
    reflections[1].assert_experiment_identifiers_are_consistent(list2)
    params.dataset_selection.use_datasets = ["0"]
    params, exp, script_reflections = Script.prepare_input(params, exp, reflections)

    assert len(script_reflections) == 1

    # Try again, this time excluding
    params, exp, reflections = generate_test_input(n=2)
    exp[0].identifier = "0"
    reflections[0].experiment_identifiers()[0] = "0"
    exp[1].identifier = "1"
    reflections[1].experiment_identifiers()[0] = "1"
    params.dataset_selection.exclude_datasets = ["0"]
    params, exp, script_reflections = Script.prepare_input(params, exp, reflections)

    assert len(script_reflections) == 1
    assert script_reflections[0] is reflections[1]

    # Try setting space group
    params, exp, reflections = generate_test_input(n=1)
    params.scaling_options.space_group = "P1"
    params, script_exp, script_reflections = Script.prepare_input(
        params, exp, reflections
    )
    assert script_exp[0].crystal.get_space_group().type().number() == 1

    # Try having two unequal space groups
    params, exp, reflections = generate_test_input(n=2)
    exp_dict = {
        "__id__": "crystal",
        "real_space_a": [1.0, 0.0, 0.0],
        "real_space_b": [0.0, 1.0, 0.0],
        "real_space_c": [0.0, 0.0, 2.0],
        "space_group_hall_symbol": " P 1",
    }
    crystal = Crystal.from_dict(exp_dict)
    exp[0].crystal = crystal
    with pytest.raises(Sorry):
        params, script_exp, script_reflections = Script.prepare_input(
            params, exp, reflections
        )

    # Test cutting data
    params, exp, reflections = generate_test_input(n=1)
    params.cut_data.d_min = 1.5
    params, script_exp, script_reflections = Script.prepare_input(
        params, exp, reflections
    )
    r = script_reflections[0]
    assert list(r.get_flags(r.flags.user_excluded_in_scaling)) == [
        False,
        False,
        True,
        True,
    ]
    params.cut_data.d_max = 2.25
    params, script_exp, script_reflections = Script.prepare_input(
        params, exp, reflections
    )
    r = script_reflections[0]
    assert list(r.get_flags(r.flags.user_excluded_in_scaling)) == [
        False,
        False,
        True,
        True,
    ]

    params, exp, reflections = generate_test_input(n=1)
    reflections[0]["partiality"] = flex.double([0.5, 0.8, 1.0, 1.0])
    params.cut_data.partiality_cutoff = 0.75
    params, script_exp, script_reflections = Script.prepare_input(
        params, exp, reflections
    )
    r = script_reflections[0]
    assert list(r.get_flags(r.flags.user_excluded_in_scaling)) == [
        True,
        False,
        False,
        False,
    ]


@pytest.mark.dataset_test
def test_scale_physical(dials_regression, run_in_tmpdir):
    """Test standard scaling of one dataset."""

    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path = os.path.join(data_dir, "20_integrated_experiments.json")
    extra_args = [
        "model=physical",
        "merged_mtz=merged.mtz",
        "optimise_errors=False",
        "intensity_choice=profile",
        "unmerged_mtz=unmerged.mtz",
        "use_free_set=1",
        "outlier_rejection=simple",
    ]

    run_one_scaling([pickle_path], [sweep_path], extra_args)
    assert os.path.exists("unmerged.mtz")
    assert os.path.exists("merged.mtz")

    # Now inspect output, check it hasn't changed drastically, or if so verify
    # that the new behaviour is more correct and update test accordingly.
    result = get_merging_stats("unmerged.mtz")
    print(result.overall.r_pim, result.overall.cc_one_half, result.overall.n_obs)
    assert result.overall.r_pim < 0.0255  # at 30/01/19, value was 0.02410
    assert result.overall.cc_one_half > 0.9955  # at 30/01/19, value was 0.9960
    assert result.overall.n_obs > 2300  # at 30/01/19, was 2320

    # Try running again with the merged.mtz as a target, to trigger the
    # target_mtz option
    extra_args.append("target_mtz=merged.mtz")
    run_one_scaling([pickle_path], [sweep_path], extra_args)
    result = get_merging_stats("unmerged.mtz")
    assert (
        result.overall.r_pim < 0.0255
    )  # at 14/08/18, value was 0.023, at 07/02/19 was 0.0243
    assert (
        result.overall.cc_one_half > 0.9955
    )  # at 14/08/18, value was 0.999, at 07/02/19 was 0.9961
    assert result.overall.n_obs > 2300  # at 07/01/19, was 2321, at 07/02/19 was 2321

    # run again with the concurrent scaling option turned off and the 'standard'
    # outlier rejection
    extra_args = [
        "model=physical",
        "merged_mtz=merged.mtz",
        "unmerged_mtz=unmerged.mtz",
        "use_free_set=1",
        "outlier_rejection=standard",
        "concurrent=False",
        "intensity_choice=combine",
    ]
    run_one_scaling([pickle_path], [sweep_path], extra_args)

    # Now inspect output, check it hasn't changed drastically, or if so verify
    # that the new behaviour is more correct and update test accordingly.
    result = get_merging_stats("unmerged.mtz")
    assert (
        result.overall.r_pim < 0.024
    )  # at 07/01/19, value was 0.02372, at 30/01/19 was 0.021498
    assert (
        result.overall.cc_one_half > 0.995
    )  # at 07/01/19, value was 0.99568, at 30/01/19 was 0.9961
    assert result.overall.n_obs > 2300  # at 07/01/19, was 2336, at 22/05/19 was 2311
    # test the 'stats_only' option
    extra_args = ["stats_only=True"]
    run_one_scaling(["scaled.pickle"], ["scaled_experiments.json"], extra_args)
    # test the 'export_mtz_only' option
    extra_args = [
        "export_mtz_only=True",
        "unmerged_mtz=test_1.mtz",
        "merged_mtz=test_2.mtz",
    ]
    run_one_scaling(["scaled.pickle"], ["scaled_experiments.json"], extra_args)
    assert os.path.exists("test_1.mtz")
    assert os.path.exists("test_2.mtz")

    # Check that dials-report and dials.show work on the output
    command = " ".join(["dials.show", "scaled.pickle", "scaled_experiments.json"])
    print(command)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    command = " ".join(["dials.report", "scaled.pickle", "scaled_experiments.json"])
    print(command)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()


def test_scale_and_filter(dials_data, run_in_tmpdir):
    location = dials_data("multi_crystal_proteinase_k")

    command = [
        "dials.scale_and_filter",
        "stdcutoff=3.0",
        "mode=image_group",
        "max_cycles=6",
        "plots.histogram=cc_half_histograms.png",
        "d_min=1.4",
        "group_size=5",
        "plots.merging_stats=merging_stats.png",
        "unmerged_mtz=unmerged.mtz",
        "output.analysis_results=analysis_results.json",
        "plots.image_ranges=reduced_image_ranges.png",
        "optimise_errors=False",
    ]
    for i in [1, 2, 3, 4, 5, 7, 10]:
        command.append(location.join("experiments_" + str(i) + ".json").strpath)
        command.append(location.join("reflections_" + str(i) + ".pickle").strpath)

    result = procrunner.run(command)
    assert result["exitcode"] == 0
    assert result["stderr"] == ""
    assert os.path.exists("scaled.pickle")
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("analysis_results.json")
    assert os.path.exists("reduced_image_ranges.png")
    assert os.path.exists("merging_stats.png")
    assert os.path.exists("cc_half_histograms.png")
    result = get_merging_stats("unmerged.mtz")
    assert result.overall.r_pim < 0.17  # 17/05/19 was 0.1525
    assert result.overall.cc_one_half > 0.96  # 17/05/19 was 0.9722
    assert result.overall.n_obs > 51540  # 17/05/19 was 51560
    # for this dataset, expect to have two regions excluded - last 5 images of
    # datasets _4 & _5
    with open("analysis_results.json") as f:
        analysis_results = json.load(f)
    assert analysis_results["cycle_results"]["1"]["image_ranges_removed"] == [
        [[21, 25], 4]
    ]
    assert analysis_results["cycle_results"]["2"]["image_ranges_removed"] == [
        [[21, 25], 3]
    ]
    assert analysis_results["termination_reason"] == "max_percent_removed"

    command = [
        "dials.scale_and_filter",
        "stdcutoff=1.0",
        "mode=dataset",
        "max_cycles=2",
        "plots.histogram=cc_half_histograms.png",
        "d_min=1.4",
        "plots.merging_stats=merging_stats.png",
        "unmerged_mtz=unmerged.mtz",
        "output.analysis_results=analysis_results.json",
        "plots.image_ranges=reduced_image_ranges.png",
        "optimise_errors=False",
    ]
    for i in [1, 2, 3, 4, 5, 7, 10]:
        command.append(location.join("experiments_" + str(i) + ".json").strpath)
        command.append(location.join("reflections_" + str(i) + ".pickle").strpath)

    result = procrunner.run(command)
    assert result["exitcode"] == 0
    assert result["stderr"] == ""
    assert os.path.exists("scaled.pickle")
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("analysis_results.json")
    assert os.path.exists("reduced_image_ranges.png")
    assert os.path.exists("merging_stats.png")
    assert os.path.exists("cc_half_histograms.png")
    with open("analysis_results.json") as f:
        analysis_results = json.load(f)
    assert analysis_results["cycle_results"]["1"]["removed_datasets"] == ["4"]


@pytest.mark.dataset_test
def test_scale_optimise_errors(dials_regression, run_in_tmpdir):
    """Test standard scaling of one dataset with error optimisation."""
    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path = os.path.join(data_dir, "20_integrated_experiments.json")
    extra_args = ["model=physical", "optimise_errors=True"]
    run_one_scaling([pickle_path], [sweep_path], extra_args)


@pytest.mark.dataset_test
def test_scale_array(dials_regression, run_in_tmpdir):
    """Test a standard dataset - ideally needs a large dataset or full matrix
    round may fail. Currently turning off absorption term to avoid
    overparameterisation and failure of full matrix minimisation."""

    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path = os.path.join(data_dir, "20_integrated_experiments.json")
    extra_args = ["model=array", "absorption_term=0", "full_matrix=0"]

    run_one_scaling([pickle_path], [sweep_path], extra_args)


@pytest.mark.dataset_test
def test_multi_scale(dials_regression, run_in_tmpdir):
    """Test standard scaling of two datasets."""

    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path_1 = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path_1 = os.path.join(data_dir, "20_integrated_experiments.json")
    pickle_path_2 = os.path.join(data_dir, "25_integrated.pickle")
    sweep_path_2 = os.path.join(data_dir, "25_integrated_experiments.json")
    extra_args = [
        "unmerged_mtz=unmerged.mtz",
        "optimise_errors=False",
        "intensity_choice=profile",
        "outlier_rejection=simple",
    ]

    run_one_scaling(
        [pickle_path_1, pickle_path_2], [sweep_path_1, sweep_path_2], extra_args
    )

    # Now inspect output, check it hasn't changed drastically, or if so verify
    # that the new behaviour is more correct and update test accordingly.
    result = get_merging_stats("unmerged.mtz")
    expected_nobs = 5460
    assert abs(result.overall.n_obs - expected_nobs) < 30
    assert result.overall.r_pim < 0.0221  # at 22/10/18, value was 0.22037
    assert result.overall.cc_one_half > 0.9975  # at 07/08/18, value was 0.99810
    print(result.overall.r_pim)
    print(result.overall.cc_one_half)

    # run again, optimising errors, and continuing from where last run left off.
    extra_args = [
        "optimise_errors=True",
        "unmerged_mtz=unmerged.mtz",
        "check_consistent_indexing=True",
    ]
    run_one_scaling(["scaled.pickle"], ["scaled_experiments.json"], extra_args)
    # Now inspect output, check it hasn't changed drastically, or if so verify
    # that the new behaviour is more correct and update test accordingly.
    # Note: error optimisation currently appears to give worse results here!
    result = get_merging_stats("unmerged.mtz")
    expected_nobs = 5411
    print(result.overall.r_pim)
    print(result.overall.cc_one_half)
    assert abs(result.overall.n_obs - expected_nobs) < 100
    assert result.overall.r_pim < 0.023  # at 07/08/18, value was 0.022722
    assert result.overall.cc_one_half > 0.9965  # at 07/08/18, value was 0.996925

    # test multi-wavelength export option
    exps = load.experiment_list("scaled_experiments.json", check_format=False)
    # fake a multi-wavelength case
    exps[0].beam.set_wavelength(0.5)
    exps[1].beam.set_wavelength(1.0)
    dump.experiment_list(exps, "tmp_exp.json")
    extra_args = [
        "export_mtz_only=True",
        "unmerged_mtz='unmerged_1.mtz unmerged_2.mtz'",
        "merged_mtz='merged_1.mtz merged_2.mtz'",
    ]
    run_one_scaling(["scaled.pickle"], ["tmp_exp.json"], extra_args)
    assert os.path.exists("unmerged_1.mtz")
    assert os.path.exists("unmerged_2.mtz")
    assert os.path.exists("merged_1.mtz")
    assert os.path.exists("merged_2.mtz")

    # until scaled data is available in dials_regression, test the command
    # line script dials.compute_delta_cchalf here
    run_delta_cchalf(
        ["scaled.pickle"], ["scaled_experiments.json"], extra_args=["stdcutoff=0.0"]
    )  # set 0.0 to force one to be 'rejected'


@pytest.mark.dataset_test
def test_multi_scale_exclude_images(dials_regression, run_in_tmpdir):

    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path_1 = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path_1 = os.path.join(data_dir, "20_integrated_experiments.json")
    pickle_path_2 = os.path.join(data_dir, "25_integrated.pickle")
    sweep_path_2 = os.path.join(data_dir, "25_integrated_experiments.json")
    # Expect this dataset to be given batches 1-1800 and 1901-3600
    # Try excluding last two batches
    extra_args = [
        "optimise_errors=False",
        "intensity_choice=profile",
        "outlier_rejection=simple",
        "exclude_images=0:1601:1800",
        "exclude_images=1:1501:1700",
    ]

    run_one_scaling(
        [pickle_path_1, pickle_path_2], [sweep_path_1, sweep_path_2], extra_args
    )

    experiments_list = load.experiment_list(
        "scaled_experiments.json", check_format=False
    )
    assert experiments_list.scaling_models()[0].configdict["valid_image_range"] == [
        1,
        1600,
    ]
    assert experiments_list.scaling_models()[1].configdict["valid_image_range"] == [
        1,
        1500,
    ]
    assert pytest.approx(
        experiments_list.scaling_models()[0].configdict["valid_osc_range"], [0, 160.0]
    )
    assert pytest.approx(
        experiments_list.scaling_models()[1].configdict["valid_osc_range"],
        [-145.0, 5.0],
    )

    extra_args = [
        "optimise_errors=False",
        "intensity_choice=profile",
        "outlier_rejection=simple",
        "exclude_images=0:1401:1600",
    ]
    run_one_scaling(["scaled.pickle"], ["scaled_experiments.json"], extra_args)
    experiments_list = load.experiment_list(
        "scaled_experiments.json", check_format=False
    )
    assert experiments_list.scaling_models()[0].configdict["valid_image_range"] == [
        1,
        1400,
    ]
    assert experiments_list.scaling_models()[1].configdict["valid_image_range"] == [
        1,
        1500,
    ]
    assert pytest.approx(
        experiments_list.scaling_models()[0].configdict["valid_osc_range"], [0, 140.0]
    )
    assert pytest.approx(
        experiments_list.scaling_models()[1].configdict["valid_osc_range"],
        [-145.0, 5.0],
    )


@pytest.mark.dataset_test
def test_targeted_scaling(dials_regression, run_in_tmpdir):
    """Test the targeted scaling workflow."""
    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path_1 = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path_1 = os.path.join(data_dir, "20_integrated_experiments.json")
    pickle_path_2 = os.path.join(data_dir, "25_integrated.pickle")
    sweep_path_2 = os.path.join(data_dir, "25_integrated_experiments.json")
    pickle_path_3 = os.path.join(data_dir, "30_integrated.pickle")
    sweep_path_3 = os.path.join(data_dir, "30_integrated_experiments.json")

    extra_args = ["model=physical"]

    args = ["dials.scale"] + [pickle_path_1] + [sweep_path_1] + extra_args
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")

    experiments_list = load.experiment_list(
        "scaled_experiments.json", check_format=False
    )
    assert len(experiments_list.scaling_models()) == 1

    # Once individual has run, do targeted scaling of second dataset.
    # Use this as a chance to test the KB model as well.
    extra_args = ["model=KB"]
    args = (
        ["dials.scale"]
        + ["scaled.pickle"]
        + ["scaled_experiments.json"]
        + [pickle_path_2]
        + [sweep_path_2]
        + extra_args
    )
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")

    experiments_list = load.experiment_list(
        "scaled_experiments.json", check_format=False
    )
    assert len(experiments_list.scaling_models()) == 2
    assert experiments_list.scaling_models()[0].id_ == "physical"
    assert experiments_list.scaling_models()[1].id_ == "KB"

    extra_args = ["model=KB"]
    args = (
        ["dials.scale"]
        + [pickle_path_3]
        + [sweep_path_3]
        + ["scaled.pickle"]
        + ["scaled_experiments.json"]
        + extra_args
    )
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")

    extra_args = ["model=KB", "only_target=True"]
    args = (
        ["dials.scale"]
        + ["scaled.pickle"]
        + ["scaled_experiments.json"]
        + [pickle_path_2]
        + [sweep_path_2]
        + extra_args
    )
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")


def test_incremental_scale_workflow(dials_regression, run_in_tmpdir):
    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path = os.path.join(data_dir, "20_integrated_experiments.json")

    args = ["dials.scale"] + [pickle_path] + [sweep_path]
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")

    # test order also - first new file before scaled
    pickle_path = os.path.join(data_dir, "25_integrated.pickle")
    sweep_path = os.path.join(data_dir, "25_integrated_experiments.json")
    args = (
        ["dials.cosym"]
        + [pickle_path]
        + [sweep_path]
        + ["scaled.pickle", "scaled_experiments.json"]
    )
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("reindexed_experiments.json")
    assert os.path.exists("reindexed_reflections.pickle")

    args = ["dials.scale", "reindexed_reflections.pickle", "reindexed_experiments.json"]
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")

    # test order also - first scaled file then new file
    pickle_path = os.path.join(data_dir, "30_integrated.pickle")
    sweep_path = os.path.join(data_dir, "30_integrated_experiments.json")
    args = (
        ["dials.cosym"]
        + ["scaled.pickle", "scaled_experiments.json"]
        + [pickle_path]
        + [sweep_path]
        + ["output.reflections=reindexed.pickle", "output.experiments=reindexed.json"]
    )
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("reindexed_experiments.json")
    assert os.path.exists("reindexed_reflections.pickle")

    args = ["dials.scale", "reindexed_reflections.pickle", "reindexed_experiments.json"]
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
    assert os.path.exists("scaled_experiments.json")
    assert os.path.exists("scaled.pickle")


@pytest.mark.dataset_test
def test_scale_cross_validate(dials_regression, run_in_tmpdir):
    """Test standard scaling of one dataset."""

    data_dir = os.path.join(dials_regression, "xia2-28")
    pickle_path = os.path.join(data_dir, "20_integrated.pickle")
    sweep_path = os.path.join(data_dir, "20_integrated_experiments.json")
    extra_args = [
        "cross_validation_mode=single",
        "nfolds=2",
        "full_matrix=0",
        "optimise_errors=0",
    ]

    args = ["dials.scale"] + [pickle_path] + [sweep_path] + extra_args
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()

    extra_args = [
        "cross_validation_mode=multi",
        "nfolds=2",
        "full_matrix=0",
        "optimise_errors=0",
        "parameter=absorption_term",
    ]

    args = ["dials.scale"] + [pickle_path] + [sweep_path] + extra_args
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()

    extra_args = [
        "cross_validation_mode=multi",
        "nfolds=2",
        "full_matrix=0",
        "optimise_errors=0",
        "parameter=model",
        'parameter_values="physical array"',
    ]

    args = ["dials.scale"] + [pickle_path] + [sweep_path] + extra_args
    command = " ".join(args)
    _ = easy_run.fully_buffered(command=command).raise_if_errors()
