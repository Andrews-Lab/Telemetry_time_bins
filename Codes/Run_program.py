import os
from tqdm import tqdm
from Create_GUI import default_values, GUI
from Create_time_bins import (import_data, clean_data, find_time_bins, 
                              add_headings_and_split_into_sheets, 
                              color_code_night_periods, export_data)

# Run the GUI.
default = default_values()
inputs = GUI(default)

# Analyse the data in each CSV file.
import_files = [file for file in os.listdir(inputs['Import location']) if 
                (file.endswith(".asc") and file.startswith("~$")==False)]

for inputs['Filename'] in tqdm(import_files, ncols=70):
    
    df, inputs     = import_data(inputs)
    df             = clean_data(df, inputs)
    df_bins        = find_time_bins(df, inputs)
    df_LA, df_temp = add_headings_and_split_into_sheets(df_bins, inputs)
    df_LA, df_temp = color_code_night_periods(df_bins, df_LA, df_temp)
    export_data(df_LA, df_temp, inputs)
    