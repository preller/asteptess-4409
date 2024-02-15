import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def analyze_observations(blue_file, red_file):
    # Load the data
    blue_band_df = pd.read_csv(blue_file)
    red_band_df = pd.read_csv(red_file)

    # Filter data where time is greater than 2000
    blue_band_filtered = blue_band_df[blue_band_df['#time'] > 2000]
    red_band_filtered = red_band_df[red_band_df['#time'] > 2000]

    # Interpolate red band flux to match blue band time points
    red_band_interpolated_flux = np.interp(
        blue_band_filtered['#time'], red_band_filtered['#time'], red_band_filtered['flux'])

    # Calculate the Pearson correlation coefficient
    correlation_coef, p_value = pearsonr(
        blue_band_filtered['flux'], red_band_interpolated_flux)

    # Plot the correlation between blue and red band fluxes
    plt.figure(figsize=(10, 6))
    plt.scatter(
        blue_band_filtered['flux'], red_band_interpolated_flux, color='purple', alpha=0.5)
    plt.title('Correlation between Blue and Red Band Fluxes for ASTEP observations')
    plt.xlabel('Blue Band Flux')
    plt.ylabel('Red Band Interpolated Flux')
    plt.grid(True)
    m, b = np.polyfit(
        blue_band_filtered['flux'], red_band_interpolated_flux, 1)
    plt.plot(blue_band_filtered['flux'], m *
             blue_band_filtered['flux'] + b, color='red')
    plt.show()

    return correlation_coef, p_value

# blue_file_path = 'path/to/blue_band_file.csv'
# red_file_path = 'path/to/red_band_file.csv'
# analyze_observations(blue_file_path, red_file_path)
