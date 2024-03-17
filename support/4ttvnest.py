import matplotlib.pyplot as plt
import numpy as np

# Data
transits = ["transit_1", "transit_2", "transit_3", "transit_4", "transit_5",
            "transit_6", "transit_7", "transit_8", "transit_9", "transit_10",
            "transit_11", "transit_12", "transit_13", "transit_14"]
ttv_median_days = np.array([-0.006924845781934794, 0.006229394733801574, 0.005065882806223488,
                            -0.0027937100542970335, -0.007420453036931077, 0.002054081039830055,
                            -0.0029842394088109153, 0.0007088925605658464, -0.0018948888710073886,
                            -0.0071623703280649445, -0.006970131900768253, 0.006753123550029973,
                            0.0003831425095255567, -0.010511413090913552])
midtimes = np.array([336.415813, 428.907419, 521.399016, 613.890608, 798.873799,
                     1076.348597, 1168.840191, 1353.823388, 1446.314984, 1538.806577,
                     1816.281369, 1908.772976, 2093.756166, 2278.739353])
ttv_median_minutes = ttv_median_days * 24 * 60
lower_error_minutes = np.array([0.00198950133208331, 0.002283025352245396, 0.0021829367431661327,
                                0.0038836988160141604, 0.001571476843614493, 0.0011415214722101455,
                                0.0009166318977503751, 0.0008746985996461276, 0.004191235991610247,
                                0.002029932514047428, 0.002958293828194059, 0.0025748285260919343,
                                0.001474316903284619, 0.004148911410755414]) * 24 * 60
upper_error_minutes = np.array([0.0019642691488789277, 0.0023373501101205396, 0.0021285989150488065,
                                0.003652866354507176, 0.001554474030758063, 0.0011333045514886828,
                                0.0008810323412379584, 0.000889764531846457, 0.0048304984318270835,
                                0.0019498927404838287, 0.0027470252986381803, 0.002577103074210588,
                                0.00146593133982342, 0.004261231393122102]) * 24 * 60


def generate_sine_wave(x, period, amplitude, phase_shift):
    """Generate sine wave values for given parameters."""
    return amplitude * np.sin(2 * np.pi * x / period + phase_shift)


def fit_and_plot_sine_wave_extended(period_range, amplitude_range, period_step, amplitude_step, x_extension=100, save_path=None, show_plot=True):
    best_loss = np.inf
    best_params = (None, None, None)  # (period, amplitude, phase_shift)

    for period in np.arange(period_range[0], period_range[1] + period_step, period_step):
        for amplitude in np.arange(amplitude_range[0], amplitude_range[1] + amplitude_step, amplitude_step):
            for phase_shift in np.linspace(0, 2 * np.pi, 100):
                fitted_y = generate_sine_wave(
                    midtimes, period, amplitude, phase_shift)
                loss = np.mean((ttv_median_minutes - fitted_y) ** 2)
                if loss < best_loss:
                    best_loss = loss
                    best_params = (period, amplitude, phase_shift)

    # Using the best parameters to generate a sine wave
    best_period, best_amplitude, best_phase_shift = best_params
    # Extending the x-range by x_extension days before the first point and after the last point
    extended_x = np.linspace(midtimes.min() - x_extension,
                             midtimes.max() + x_extension, 1000)
    extended_y_fit = generate_sine_wave(
        extended_x, best_period, best_amplitude, best_phase_shift)

    if show_plot or save_path:
        plt.figure(figsize=(12, 6))
        plt.errorbar(midtimes, ttv_median_minutes, yerr=[lower_error_minutes, upper_error_minutes], fmt='o',
                     ecolor='lightgray', elinewidth=3, capsize=0, label='TTV Data with Errors')
        plt.plot(extended_x, extended_y_fit, 'r-', label='Extended Model: Period = ' + str(best_period) +
                 ' days, Amplitude = ' + str(round(best_amplitude, 2)) + ' minutes')
        plt.axhline(y=0, color='r', linestyle='--')
        plt.title(
            'Extended TTV Data Over Time (in Minutes) with Sine Wave Fit (BJD-2458000)')
        plt.xlabel('Midtime (BJD - 2458000)')
        plt.ylabel('TTV Median (minutes)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        if show_plot:
            plt.show()
        plt.close()

    return best_params


# Running the function with the new x_extension parameter
fit_and_plot_sine_wave_extended(
    period_range=(100, 1200),
    amplitude_range=(5, 15),
    period_step=5,
    amplitude_step=0.5,
    # Extends the plotting range by 100 days before the first and after the last data point
    x_extension=100,
    save_path='./plots/ttv_sine_fit14.png',
    show_plot=False
)
