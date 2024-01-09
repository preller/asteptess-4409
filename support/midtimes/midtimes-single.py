from __future__ import print_function, division, absolute_import
import sys
import os
import allesfitter
import matplotlib.pyplot as plt
import numpy as np

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

inst = 'TESS_180s'
key = 'flux'

# ::: load the time, flux, and flux_err
time = alles.data[inst]['time']
flux = alles.data[inst][key]
flux_err = alles.data[inst]['err_scales_'+key] * \
    alles.posterior_params_median['err_'+key+'_'+inst]

# ::: note that the error for RV instruments is calculated differently
# rv_err = np.sqrt( alles.data[inst]['white_noise_'+key]**2 + alles.posterior_params_median['jitter_'+key+'_'+inst]**2 )

# ::: set up the figure
# fig, axes = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={
#                          'height_ratios': [3, 1]}, sharex=True)
# fig.subplots_adjust(hspace=0)

# # ::: top panel: plot the data and 20 curves from random posterior samples (evaluated on a fine time grid)
# ax = axes[0]
# ax.errorbar(time, flux, flux_err, fmt='b.')
# for i in range(20):
#     time_fine = np.arange(time[0], time[-1], 0.002)
#     model_fine, baseline_fine, _ = alles.get_one_posterior_curve_set(
#         inst, key, xx=time_fine)
#     ax.plot(time_fine, 1.+baseline_fine, 'g-', lw=2, zorder=11)
#     ax.plot(time_fine, model_fine+baseline_fine,
#             'r-', lw=0.2, zorder=12, alpha=0.5)

# ::: bottom panel: plot the residuals;
# ::: for that, subtract the "posterior median model" and "posterior median baseline" from the data (evaluated on the time stamps of the data)
# ax = axes[1]
baseline = alles.get_posterior_median_baseline(inst, key)
model = alles.get_posterior_median_model(inst, key)
# ax.errorbar(time, flux-(model+baseline), flux_err, fmt='b.')
# ax.axhline(0, color='grey', linestyle='--')

# save the figure
# fig.savefig('./PLOT3.png', dpi=300, bbox_inches='tight')

# plt.show()
# breakpoint()
# Get the model start and end times
# start_time = alles.posterior_params_median['start_time_'+inst]
# end_time = alles.posterior_params_median['end_time_'+inst]
# print("start_time = ", start_time)
# print("end_time = ", end_time)

# # Get the midtimes
# midtimes = alles.posterior_params_median['midtimes_'+inst]
# print("midtimes = ", midtimes)

# midpoint, ingress_time, egress_time = alles.posterior_params_median['b_epoch'], alles.posterior_params_median[
#     'b_epoch'] - transit_duration / 2, alles.posterior_params_median['b_epoch'] + transit_duration / 2

# Get one sample of the model
# model_single, baseline_single, _ = alles.get_one_posterior_curve_set(
#     inst, key, xx=time)[0]
# time_fine = np.arange(time[0], time[-1], 0.002)
# model_fine, baseline_fine, _ = alles.get_one_posterior_curve_set(
#     inst, key, xx=time_fine)

# # breakpoint()


# m = model_fine
# # Get the first and last value that is not 1 (i.e. the ingress and egress) in the model array
# time_ingress_index, time_egress_index = np.where(
#     m != 1)[0][0], np.where(m != 1)[0][-1]

# # Get the time of the ingress and egress
# time_ingress, time_egress = time[time_ingress_index], time[time_egress_index]

# # Get the transit duration
# transit_duration_days = time_egress - time_ingress
# transit_duration_hours = transit_duration_days * 24


# transit_durations = []
# for _ in range(100):  # Run the code 100 times
#     time_fine = np.arange(time[0], time[-1], 0.002)
#     model_fine, baseline_fine, _ = alles.get_one_posterior_curve_set(
#         inst, key, xx=time_fine)

#     m = model_fine
#     time_ingress_index = next(
#         (i for i, x in enumerate(m) if str(x)[:2] != "1."), None)
#     time_egress_index = len(
#         m) - next((i for i, x in enumerate(reversed(m)) if str(x)[:2] != "1."), None) - 1

#     time_ingress, time_egress = time[time_ingress_index], time[time_egress_index]

#     transit_duration_days = time_egress - time_ingress
#     transit_durations.append(transit_duration_days)

# average_transit_duration = np.mean(transit_durations)
# a = average_transit_duration * 24
# print(a)

m = model
tolerance = 1e-5
time_ingress_index = next(
    (i for i, x in enumerate(m) if abs(x - 1.0) > tolerance), None)
time_egress_index = len(
    m) - next((i for i, x in enumerate(reversed(m)) if abs(x - 1.0) > tolerance), None) - 1
time_ingress, time_egress = time[time_ingress_index], time[time_egress_index]

transit_duration_days = time_egress - time_ingress


# Plot model alone
# breakpoint()

# Plot model on time vs flux
plt.plot(time, model, 'r-')
# When the model stops being 1, draw a circle and label it "ingress" with the appropriate time
plt.plot(time[time_ingress_index], 1, "o")
plt.text(time[time_ingress_index], 1, "ingress")
# When the model starts being 1 again, draw a circle and label it "egress" with the appropriate time
plt.plot(time[time_egress_index], 1, "o")
plt.text(time[time_egress_index], 1, "egress")
# Plot the transit duration
plt.axvline(time_ingress, color='grey', linestyle='--')
plt.axvline(time_egress, color='grey', linestyle='--')


# save the figure
plt.savefig('./PLOT7A.png', dpi=300, bbox_inches='tight')
# np.where(model_fine != 1)[0][0]

breakpoint()
