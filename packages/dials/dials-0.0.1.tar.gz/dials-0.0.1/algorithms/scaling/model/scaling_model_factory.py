"""
Collection of factories for creating the scaling models.
To add a new scaling model, one must define a new extension
in dials.extensions.scaling_model_ext, create a new factory
in this file and create a new model in dials.algorithms.scaling.model.
"""
from __future__ import absolute_import, division, print_function
from collections import OrderedDict
from dials.array_family import flex
import dials.algorithms.scaling.model.model as Model


class KBSMFactory(object):
    """
    Factory for creating a KB scaling model.
    """

    @classmethod
    def create(cls, params, _, __):
        """create the simple KB scaling model."""
        configdict = OrderedDict({"corrections": []})
        parameters_dict = {}

        if params.parameterisation.decay_term:
            configdict["corrections"].append("decay")
            parameters_dict["decay"] = {
                "parameters": flex.double([0.0]),
                "parameter_esds": None,
            }
        if params.parameterisation.scale_term:
            configdict["corrections"].append("scale")
            parameters_dict["scale"] = {
                "parameters": flex.double([1.0]),
                "parameter_esds": None,
            }

        return Model.KBScalingModel(parameters_dict, configdict)


class PhysicalSMFactory(object):
    """
    Factory for creating a physical scaling model.
    """

    @classmethod
    def create(cls, params, experiments, _):
        """Create the scaling model defined by the params."""

        configdict = OrderedDict({"corrections": []})
        parameters_dict = {}

        osc_range = experiments.scan.get_oscillation_range()
        one_osc_width = experiments.scan.get_oscillation()[1]
        configdict.update({"valid_osc_range": osc_range})

        if params.parameterisation.scale_term:
            configdict["corrections"].append("scale")
            n_scale_param, s_norm_fac, scale_rot_int = Model.initialise_smooth_input(
                osc_range, one_osc_width, params.parameterisation.scale_interval
            )
            configdict.update(
                {"s_norm_fac": s_norm_fac, "scale_rot_interval": scale_rot_int}
            )
            parameters_dict["scale"] = {
                "parameters": flex.double(n_scale_param, 1.0),
                "parameter_esds": None,
            }

        if params.parameterisation.decay_term:
            configdict["corrections"].append("decay")
            n_decay_param, d_norm_fac, decay_rot_int = Model.initialise_smooth_input(
                osc_range, one_osc_width, params.parameterisation.decay_interval
            )
            configdict.update(
                {"d_norm_fac": d_norm_fac, "decay_rot_interval": decay_rot_int}
            )
            parameters_dict["decay"] = {
                "parameters": flex.double(n_decay_param, 0.0),
                "parameter_esds": None,
            }

        if params.parameterisation.absorption_term:
            configdict["corrections"].append("absorption")
            lmax = params.parameterisation.lmax
            n_abs_param = (2 * lmax) + (lmax ** 2)  # arithmetic sum formula (a1=3, d=2)
            configdict.update({"lmax": lmax})
            surface_weight = params.parameterisation.surface_weight
            configdict.update({"abs_surface_weight": surface_weight})
            parameters_dict["absorption"] = {
                "parameters": flex.double(n_abs_param, 0.0),
                "parameter_esds": None,
            }

        return Model.PhysicalScalingModel(parameters_dict, configdict)


def calc_n_param_from_bins(value_min, value_max, n_bins):
    """Return the correct number of bins for initialising the gaussian
    smoothers."""
    assert n_bins > 0
    assert isinstance(n_bins, int)
    bin_width = (value_max - value_min) / n_bins
    if n_bins == 1:
        n_param = 2
    elif n_bins == 2:
        n_param = 3
    else:
        n_param = n_bins + 2
    return n_param, bin_width


class ArraySMFactory(object):
    """
    Factory for creating an array-based scaling model.
    """

    @classmethod
    def create(cls, params, experiments, reflections):
        """create an array-based scaling model."""
        reflections = reflections.select(reflections["d"] > 0.0)
        configdict = OrderedDict({"corrections": []})
        # First initialise things common to more than one correction.
        one_osc_width = experiments.scan.get_oscillation()[1]
        osc_range = experiments.scan.get_oscillation_range()
        configdict.update({"valid_osc_range": osc_range})
        n_time_param, time_norm_fac, time_rot_int = Model.initialise_smooth_input(
            osc_range, one_osc_width, params.parameterisation.decay_interval
        )
        (xvalues, yvalues, _) = reflections["xyzobs.px.value"].parts()
        (xmax, xmin) = (flex.max(xvalues) + 0.001, flex.min(xvalues) - 0.001)
        (ymax, ymin) = (flex.max(yvalues) + 0.001, flex.min(yvalues) - 0.001)

        parameters_dict = {}

        if params.parameterisation.decay_term:
            configdict["corrections"].append("decay")
            resmax = (1.0 / (flex.min(reflections["d"]) ** 2)) + 0.001
            resmin = (1.0 / (flex.max(reflections["d"]) ** 2)) - 0.001
            n_res_bins = params.parameterisation.n_resolution_bins
            n_res_param, res_bin_width = calc_n_param_from_bins(
                resmin, resmax, n_res_bins
            )
            configdict.update(
                {
                    "n_res_param": n_res_param,
                    "n_time_param": n_time_param,
                    "resmin": resmin,
                    "res_bin_width": res_bin_width,
                    "time_norm_fac": time_norm_fac,
                    "time_rot_interval": time_rot_int,
                }
            )
            parameters_dict["decay"] = {
                "parameters": flex.double((n_time_param * n_res_param), 1.0),
                "parameter_esds": None,
            }

        if params.parameterisation.absorption_term:
            configdict["corrections"].append("absorption")
            nxbins = nybins = params.parameterisation.n_absorption_bins
            n_x_param, x_bin_width = calc_n_param_from_bins(xmin, xmax, nxbins)
            n_y_param, y_bin_width = calc_n_param_from_bins(ymin, ymax, nybins)
            configdict.update(
                {
                    "n_x_param": n_x_param,
                    "n_y_param": n_y_param,
                    "xmin": xmin,
                    "ymin": ymin,
                    "x_bin_width": x_bin_width,
                    "y_bin_width": y_bin_width,
                    "n_time_param": n_time_param,
                    "time_norm_fac": time_norm_fac,
                    "time_rot_interval": time_rot_int,
                }
            )
            parameters_dict["absorption"] = {
                "parameters": flex.double((n_x_param * n_y_param * n_time_param), 1.0),
                "parameter_esds": None,
            }

        if params.parameterisation.modulation_term:
            configdict["corrections"].append("modulation")
            nx_det_bins = ny_det_bins = params.parameterisation.n_modulation_bins
            n_x_mod_param, x_det_bw = calc_n_param_from_bins(xmin, xmax, nx_det_bins)
            n_y_mod_param, y_det_bw = calc_n_param_from_bins(ymin, ymax, ny_det_bins)
            configdict.update(
                {
                    "n_x_mod_param": n_x_mod_param,
                    "n_y_mod_param": n_y_mod_param,
                    "xmin": xmin,
                    "ymin": ymin,
                    "x_det_bin_width": x_det_bw,
                    "y_det_bin_width": y_det_bw,
                }
            )
            parameters_dict["modulation"] = {
                "parameters": flex.double((n_x_mod_param * n_y_mod_param), 1.0),
                "parameter_esds": None,
            }

        return Model.ArrayScalingModel(parameters_dict, configdict)
