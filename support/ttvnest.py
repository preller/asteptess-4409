import numpy as np
import pandas as pd
import pymc as pm
import matplotlib.pyplot as plt
import arviz as az
import os

# Ensure the plots directory exists
os.makedirs('./plots', exist_ok=True)

# Data
data = {
    "t0": [
        336.415813, 428.907419, 521.399016, 613.890608, 798.873799, 1076.348597,
        1168.840191, 1353.823388, 1446.314984, 1538.806577, 1816.281369, 1908.772976,
        2093.756166, 2278.739353
    ],
    "ttv_median_minutes": [
        -0.416693, 0.374567, 0.304755, -0.167623, -0.445227, 0.123243,
        -0.179054, 0.042534, -0.113693, -0.429742, -0.418209, 0.405187,
        0.022990, -0.630686
    ],
    "sigma_t0_minutes": [
        0.118620, 0.138600, 0.129744, 0.226128, 0.093780, 0.068220,
        0.053940, 0.052920, 0.270660, 0.119400, 0.171180, 0.154560,
        0.088200, 0.252300
    ]
}

df = pd.DataFrame(data)

with pm.Model() as model:
    amplitude = pm.Normal("amplitude", mu=10, sigma=5)
    period = pm.Normal("period", mu=400, sigma=200)
    phase = pm.Uniform("phase", lower=0, upper=2 * np.pi)
    offset = pm.Normal("offset", mu=0, sigma=10)

    theta = (2 * np.pi / period) * (df['t0'] - df['t0'].min()) + phase
    sine = amplitude * np.sin(theta) + offset

    obs = pm.Normal(
        "obs", mu=sine, sigma=df['sigma_t0_minutes'], observed=df['ttv_median_minutes'])

    trace = pm.sample(1000, tune=1000, cores=2, target_accept=0.95)

# Correct way to obtain posterior predictive checks
with model:
    ppc = pm.sample_posterior_predictive(trace)

# Fixing the plot issue by ensuring the correct dimensionality
plt.figure(figsize=(12, 6))
plt.errorbar(df['t0'], df['ttv_median_minutes'], yerr=df['sigma_t0_minutes'],
             fmt='o', label='Observed', ecolor='red', capsize=5, capthick=2, color='blue')
observed_y = ppc['obs'] if 'obs' in ppc else ppc.posterior_predictive['obs'].mean(
    dim=['chain', 'draw']).values
plt.plot(df['t0'], np.mean(observed_y, axis=0),
         label='Fitted Model', color='green')
plt.fill_between(df['t0'], np.percentile(observed_y, 2.5, axis=0), np.percentile(
    observed_y, 97.5, axis=0), color='green', alpha=0.5)
plt.axhline(y=0, color='k', linestyle='--')
plt.xlabel('Time (BJD - 2457000)')
plt.ylabel('TTV (minutes)')
plt.title('TTV of Exoplanets Over Time with Sine Model Fit')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the figure
plt.savefig('./plots/ttvnested.png')
plt.show()
