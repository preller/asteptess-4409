import pandas as pd
import os
import pathlib
from astropy.io import fits


def convert_to_allesfitter_csv(input_file, output_file):
    # Load the input data.
    data = pd.read_csv(input_file)

    # Time is already normalized to BJD, so we don't need to do anything.

    # Save first FLUX value for later calculations.
    first_flux = data['flux'][0]

    # Normalize flux to be relative to first reading.
    data['FLUX'] = data['flux'] / first_flux

    # Update ERRFLUX proportionally.
    data['ERRFLUX'] = data['flux_err'] / first_flux

    # Keep only the time, flux, and flux_err columns.
    data = data[['time', 'FLUX', 'ERRFLUX']]

    # Rename columns to match allesfitter format.
    data = data.rename(
        columns={'time': 'time', 'FLUX': 'flux', 'ERRFLUX': 'flux_err'})

    # Write to output.csv, excluding the index and including a header.
    data.to_csv(output_file, index=False, header=[
                "time", "flux", "flux_err"], float_format='%.18e')


def convert_to_allesfitter(input_file, output_file):
    # Load data from the FITS file.
    with fits.open(input_file) as hdul:
        data = hdul[1].data  # Assuming the data is in the first extension
        df = pd.DataFrame(data)

    # Ensure the necessary columns are present.
    required_columns = ['TIME', 'FLUX', 'FLUX_ERR']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Input FITS file must contain {required_columns}")

    # Save first FLUX value for later calculations.
    first_flux = df['FLUX'][0]

    # Normalize flux to be relative to first reading.
    df['normalized_flux'] = df['FLUX'] / first_flux

    # Update normalized flux error proportionally.
    df['normalized_flux_err'] = df['FLUX_ERR'] / first_flux

    # Keep only the TIME, normalized flux, and normalized flux error columns.
    df = df[['TIME', 'normalized_flux', 'normalized_flux_err']]

    # Rename columns to match allesfitter format.
    df = df.rename(columns={
                   'TIME': 'time', 'normalized_flux': 'flux', 'normalized_flux_err': 'flux_err'})

    # Write to output.csv, excluding the index and including a header.
    df.to_csv(output_file, index=False, header=[
              "time", "flux", "flux_err"], float_format='%.18e')


# convert_all_path_dir = "/workspaces/astep-tess-targets/data/tess_folded"
# output_path_dir = "/workspaces/astep-tess-targets/data/tess_converted"
# convert_path = "/home/preller/h/workspace/astep-tess-targets/astep-tess-targets/toi4409/toi4409-tess-stitched-single-initial-test.csv"
# output_path= "/home/preller/h/workspace/astep-tess-targets/astep-tess-targets/toi4409/toi4409-tess-stitched-single-initial-test_converted.csv"
# convert_path = "/workspaces/astep-tess-targets/toi4409/toi4409-full-tess-stitched-nonans-filtered1day-sorted.csv"
# output_path = "/workspaces/astep-tess-targets/toi4409/toi4409-full-tess-stitched-nonans-filtered1day-sorted_converted.csv"

# convert_to_allesfitter(convert_path, output_path)


# For each file in the path, convert it to the allesfitter format, and save it to the output path.
# for file in os.listdir(convert_all_path_dir):
#     convert_to_allesfitter(os.path.join(convert_all_path_dir, file), os.path.join(output_path_dir, file))


# If main, run
if __name__ == "__main__":
    file_to_convert_path = pathlib.Path(
        "../data/tess-stitched/raw/4409-tess-lightcurves-1800s.fits")
    output_path = pathlib.Path(
        "../data/tess-stitched/allesfitter_converted/4409-tess-lightcurves-1800s_converted.csv")

    convert_to_allesfitter(file_to_convert_path, output_path)
