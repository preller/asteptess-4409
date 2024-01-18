import pandas as pd


def csv_to_latex_table_with_bounds(csv_path, latex_file_path, sidewaystable=False):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Group the data by observations
    df_grouped = df.groupby(
        df['property'].str.extract(r'(.*?; .*?; .*?; (.*?))')[0])

    # LaTeX preambles
    latex_string = '\\begin{table*}\n' if not sidewaystable else '\\begin{sidewaystable}\n'
    latex_string += '\\centering\n\\renewcommand{\\arraystretch}{2}\n'
    latex_string += '\\begin{tabular}{|' + 'c|' * \
        (len(df_grouped.groups) + 1) + '}\n\\hline\n'

    # Adding the column headers
    column_headers = "Property & " + \
        " & ".join(df_grouped.groups.keys()) + " \\\\\\hline\n"
    latex_string += column_headers

    # Adding the rows and ensuring proper math mode formatting
    for property, group in df_grouped:
        for index, row in group.iterrows():
            row_string = row['property'].split(';')[0] + ' & '
            # Enclose the item in $ if it looks like a math expression
            if '_' in str(row['value']) or '^' in str(row['value']):
                row_string += f'${row["value"]}_{{-{row["lower_error"]}}}^{{+{row["upper_error"]}}}$ & '
            else:
                row_string += f'{row["value"]}_{{-{row["lower_error"]}}}_{{+{row["upper_error"]}}} & '
        # Remove the last ' & ' and add a new line
        row_string = row_string[:-3] + " \\\\\n"
        latex_string += row_string

    # Closing the LaTeX tabular environment
    latex_string += '\\hline\n\\end{tabular}\n'
    latex_string += '\\end{table*}\n' if not sidewaystable else '\\end{sidewaystable}\n'

    # Writing to the LaTeX file
    with open(latex_file_path, "w") as file:
        file.write(latex_string)


def save_latex_table(csv_file_path, target_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Start building the LaTeX table
    latex_table = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{|l|c|c|c|c|c|c|c|c|c|}\n\\hline\n"
    latex_table += "\\textbf{Parameter} & \\textbf{TESS_1800s} & \\textbf{TESS_600s} & \\textbf{TESS_180s} & \\textbf{ASTEP_R} & \\textbf{ASTEP_B} & \\textbf{ASTEP_Rc} & \\textbf{CHAT_I} & \\textbf{OMES_I} & \\textbf{OMES_R} \\\\\n\\hline\n"

    # Process each row
    for _, row in df.iterrows():
        value = row['value']
        lower = row['lower_error']
        upper = row['upper_error']
        latex_table += f"{row['property']} & \\( {value}^{{+{upper}}}_{{-{lower}}} \\) & & & & & & & & \\\\\n"

    # End the table
    latex_table += "\\hline\n\\end{tabular}\n\\caption{Your caption here}\n\\label{tab:your_label}\n\\end{table}"

    # Save to the target file
    with open(target_file_path, "w") as file:
        file.write(latex_table)


# Example usage
csv_path = "./tmp/ns_derived_table.csv"
latex_file_path = "./tmp/ns_derived_table3.tex"
# csv_to_latex_table_with_bounds(csv_path, latex_file_path, sidewaystable=True)


# Example usage
save_latex_table(csv_path, latex_file_path)
