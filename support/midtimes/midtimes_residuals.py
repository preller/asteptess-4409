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
fig, axes = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={
                         'height_ratios': [3, 1]}, sharex=True)
fig.subplots_adjust(hspace=0)

# ::: top panel: plot the data and 20 curves from random posterior samples (evaluated on a fine time grid)
ax = axes[0]
ax.errorbar(time, flux, flux_err, fmt='b.')
for i in range(20):
    time_fine = np.arange(time[0], time[-1], 0.05)
    model_fine, baseline_fine, _ = alles.get_one_posterior_curve_set(
        inst, key, xx=time_fine)
    ax.plot(time_fine, 1.+baseline_fine, 'g-', lw=2, zorder=11)
    ax.plot(time_fine, model_fine+baseline_fine, 'r-', lw=2, zorder=12)

# ::: bottom panel: plot the residuals;
# ::: for that, subtract the "posterior median model" and "posterior median baseline" from the data (evaluated on the time stamps of the data)
ax = axes[1]
baseline = alles.get_posterior_median_baseline(inst, key)
model = alles.get_posterior_median_model(inst, key)
ax.errorbar(time, flux-(model+baseline), flux_err, fmt='b.')
ax.axhline(0, color='grey', linestyle='--')

# save the figure
fig.savefig('./PLOT.png', dpi=300, bbox_inches='tight')

# plt.show()
