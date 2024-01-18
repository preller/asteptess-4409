from __future__ import print_function, division, absolute_import
# import sys
# import os
import matplotlib.pyplot as plt
import allesfitter
# import numpy as np

# ::: plotting settings
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep',
        font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({"xtick.direction": "in", "ytick.direction": "in"})
sns.set_context(rc={'lines.markeredgewidth': 1})

# ::: modules


# datadir = "C:\HOME\Work\asteptess\asteptesss-4409\allesfitter\all_runs\runs_with_2458bjd\2_allesfit_ephemerides_multi_instrument_alltessfixed"
# datadir = "../../allesfitter/all_runs/runs_with_2458bjd/2_allesfit_ephemerides_multi_instrument_alltessfixed_midtimes"
# datadir = "./ttvs"
# fit = allesfitter.allesclass(datadir)


# # print(fit.posterior_samples_at_maximum_likelihood)

# # Print all the parameters of fit; extract them as if fit was an object, and hence the parameters were attributes of the object
# # print(dir(fit))
# breakpoint()


# ------------------------------------------------------------------------------
# 2.1) Full time series
# ------------------------------------------------------------------------------
# ::: settings
datadir = "./ttvs"
alles = allesfitter.allesclass(datadir)

inst = 'TESS_1800s'
key = 'flux'

# ::: load the time, flux, and flux_err
time = alles.data[inst]['time']
flux = alles.data[inst][key]
flux_err = alles.data[inst]['err_scales_'+key] * \
    alles.posterior_params_median['err_'+key+'_'+inst]

baseline = alles.get_posterior_median_baseline(inst, key)
model = alles.get_posterior_median_model(inst, key)


# m = model
# tolerance = 1e-5
# time_ingress_index = next(
#     (i for i, x in enumerate(m) if abs(x - 1.0) > tolerance), None)
# time_egress_index = len(
#     m) - next((i for i, x in enumerate(reversed(m)) if abs(x - 1.0) > tolerance), None) - 1
# time_ingress, time_egress = time[time_ingress_index], time[time_egress_index]

# transit_duration_days = time_egress - time_ingress


def get_transit_info(instruments, n, key='flux', tolerance=1e-6):
    all_transits = {}
    all_models = {}
    for instrument in instruments:
        print(f'processing instrument {instrument}')

        # Check if the key is in the instrument's data
        if key not in alles.data[instrument]:
            raise ValueError(
                f'Key "{key}" not found in instrument "{instrument}"')
        # Check if the length of the key array is zero
        elif len(alles.data[instrument][key]) == 0:
            raise ValueError(
                f'Key "{key}" in instrument "{instrument}" has no entries')

        # Load the time, flux, and flux_err
        time = alles.data[instrument]['time']
        flux = alles.data[instrument][key]
        flux_err = alles.data[instrument]['err_scales_'+key] * \
            alles.posterior_params_median['err_'+key+'_'+instrument]

        baseline = alles.get_posterior_median_baseline(instrument, key)
        model = alles.get_posterior_median_model(instrument, key)
        all_models[instrument] = model

        transits = []
        in_transit = False
        for i in range(len(model)):
            if not in_transit and abs(model[i] - 1.0) > tolerance:
                in_transit = True
                ingress_index = i
            elif in_transit and (abs(model[i] - 1.0) <= tolerance or i == len(model) - 1):
                in_transit = False
                egress_index = i
                ingress_time = time[ingress_index]
                egress_time = time[egress_index]
                transit_duration = egress_time - ingress_time
                transits.append((ingress_index, egress_index,
                                ingress_time, egress_time, transit_duration))
        all_transits[instrument] = transits

    return all_transits, all_models


def plot_transit_info(model, time, transits, save_path=None):
    # Plot model on time vs flux
    plt.plot(time, model, 'r-')
    for transit in transits:
        time_ingress_index, time_egress_index, _, _, _ = transit
        # When the model stops being 1, draw a circle and label it "ingress" with the appropriate time
        plt.plot(time[time_ingress_index], 1, "o")
        plt.text(time[time_ingress_index], 1, "ingress")
        # When the model starts being 1 again, draw a circle and label it "egress" with the appropriate time
        plt.plot(time[time_egress_index], 1, "o")
        plt.text(time[time_egress_index], 1, "egress")
        # Plot the transit duration
        plt.axvline(time[time_ingress_index], color='grey', linestyle='--')
        plt.axvline(time[time_egress_index], color='grey', linestyle='--')
    # save the figure
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')


# transits = get_transit_info([inst], 3)

# plot_transit_info(model, time, transits[inst], save_path='./PLOT9c.png')


# # model, t_in, t_eg, t_dur_d, t_in_i, t_eg_i = get_transit_info(
# #     inst)

# transits = get_transit_info([inst], 3)

# # breakpoint()

# first_transit = transits[inst][0]
# t_in_i, t_eg_i, t_in, t_eg, t_dur_d = first_transit

# plot_transit_info(model, time, transits[inst], save_path='./PLOT9d.png')


# Get all instruments
all_instruments = instruments = list(alles.data.keys())
# Keep those only with photometry
instruments = [
    inst for inst in instruments if inst in alles.data['inst_phot']['inst']]

print(instruments)


transits, models = get_transit_info(instruments, 5)



# ASSUMPTION:: All transit midtimes are captured by the ingress and egress times
# Create and sort the all_transit_midtimes, all_ingress_times, and all_egress_times arrays
all_transit_midtimes = sorted(alles.data['b_tmid_observed_transits'])
all_ingress_times = sorted(
    [transit[2] for instrument in instruments for transit in transits[instrument]])
all_egress_times = sorted(
    [transit[3] for instrument in instruments for transit in transits[instrument]])

transit_duration = 10 / 24  # 10 hours in days
# factor of 20% above and below the transit duration
transit_threshold_tolerance_factor = 1.2
tolerance = transit_duration / 2 * transit_threshold_tolerance_factor

# Group ingress and egress times by transit
transit_times = {midtime: {'ingress_times': [], 'egress_times': []}
                 for midtime in all_transit_midtimes}

for instrument in instruments:
    for transit in transits[instrument]:
        ingress_time, egress_time = transit[2], transit[3]
        # Find a matching midtime in all_transit_midtimes
        for midtime in all_transit_midtimes:
            if abs(midtime - ingress_time) <= tolerance:
                transit_times[midtime]['ingress_times'].append(ingress_time)
            if abs(midtime - egress_time) <= tolerance:
                transit_times[midtime]['egress_times'].append(egress_time)

# Check if each midtime has at least one ingress or one egress time
for midtime, times in transit_times.items():
    if not times['ingress_times'] and not times['egress_times']:
        raise ValueError(f'Midtime {midtime} has no ingress or egress times')

# Check if each ingress and egress time that shows up is within the tolerance of at least one midtime
for midtime, times in transit_times.items():
    for ingress_time in times['ingress_times']:
        if not any(abs(midtime - ingress_time) <= tolerance for midtime in all_transit_midtimes):
            raise ValueError(
                f'Ingress time {ingress_time} is not within the tolerance of any midtime')
    for egress_time in times['egress_times']:
        if not any(abs(midtime - egress_time) <= tolerance for midtime in all_transit_midtimes):
            raise ValueError(
                f'Egress time {egress_time} is not within the tolerance of any midtime')


# # plot all the models in the same plot, make it a long plot
# def plot_all_models(models, save_path=None):
#     for instrument, model in models.items():
#         plt.plot(time, model, label=instrument)
#     plt.legend()
#     if save_path is not None:
#         plt.savefig(save_path, dpi=300, bbox_inches='tight')


# plot_all_models(models, save_path='./PLOT10a.png')

breakpoint()
