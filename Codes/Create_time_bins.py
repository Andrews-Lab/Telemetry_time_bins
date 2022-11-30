import pandas as pd
import numpy as np
import csv

def find_sum(list1):
    if (list1 is None or len(list1) == 0):
        return(0)
    else:
        return(sum(list1))
def find_avg(list1):
    if (list1 is None or len(list1) == 0):
        return(0)
    else:
        return(sum(list1)/len(list1))
def find_last(list1):
    if (list1 is None or len(list1) == 0):
        return(np.nan)
    else:
        return(list1[-1])
def cell_color(time):     
    return 'background-color: %s' % 'lightgrey'

def import_data(inputs):
    
    # Define the locations of the import and export files.
    import_name = inputs['Filename']
    inputs['Import destination'] = inputs['Import location'] + import_name
    export_name = 'Organised ' + import_name[:-4] + '.xlsx'
    inputs['Export destination'] = inputs['Export location'] + export_name
    
    # Find the number of rows and columns in the .asc file.
    file = open(inputs['Import destination'])
    reader = csv.reader(file)
    no_rows = len(list(reader))
    file.close()
    last_row = pd.read_csv(inputs['Import destination'], skiprows=no_rows-1)
    no_cols = len(list(last_row))
    
    # Import the .asc file.
    df = pd.read_csv(inputs['Import destination'], names=list(range(no_cols)))
    
    return(df, inputs)

def clean_data(df, inputs):
    
    # Clean the dataframe.
    
    # Delete rows with mouse details by looking for rows with less than 2 non-nan values. 
    df = df.dropna(thresh=2)
    
    # Assign the column headings.
    df.columns = list(df.iloc[0])
    df.index = list(range(len(df)))
    df = df.drop(0)
    df.index = list(range(len(df)))
    
    # Combine the time columns together.
    time_columns = [col for col in df.columns if 
                    (inputs['Times'][0] in col or inputs['Times'][1] in col)]
    df[time_columns[0]] = df[time_columns[0]] + ' ' + df[time_columns[1]]
    df = df.rename(columns={time_columns[0]: "Time"})
    df = df.drop(columns=[time_columns[1]])
    df["Time"] = pd.to_datetime(df["Time"])
    
    # Remove the columns that are entirely nan or 0.
    # Replace all nan values with 0.
    df = df.fillna(0)
    data_columns = [col for col in df.columns if col != "Time"]
    df[data_columns] = df[data_columns].apply(pd.to_numeric,axis=1)
    empty_columns = [col for col in df.columns if all(df[col]==0)]
    df = df.drop(columns=empty_columns)
    
    return(df)

def find_time_bins(df, inputs):
    
    # Add a time column with the minutes since the start time.
    for i in range(len(df)):
        df.at[i,"Time (mins)"] = (df.at[i,"Time"]-df.at[0,"Time"]).total_seconds() / 60
        
    # Create a list of the time bins.
    duration_mins = (df.at[len(df)-1,"Time"] - df.at[0,"Time"]).total_seconds() / 60
    time_bins_labels = list(np.arange(0, duration_mins + inputs['Time bin (mins)'], inputs['Time bin (mins)']))
    time_bins_mins = [-inputs['Time bin (mins)']] + time_bins_labels
    
    # Add the bins to the dataframe.
    df['Time bins (mins)'] = pd.cut(df['Time (mins)'], time_bins_mins, 
                                    labels=time_bins_labels, right=True)
    
    # Group the data into time bins. At each bin, list all the values for pellet 
    # count for example.
    temp_df = df.drop(columns=['Time (mins)'])
    df_bins = temp_df.groupby("Time bins (mins)").agg(list)
    
    # For each bin, find the sum if it is locomotor activity, average if it is 
    # temperature data or last value for the time stamps.
    LA_cols   = [col for col in df_bins.columns if (inputs["LA_activity"] in col)]
    temp_cols = [col for col in df_bins.columns if (inputs["Temperature"] in col)]
    for col in LA_cols:
        df_bins[col]   = df_bins[col].apply(find_sum)
    for col in temp_cols:
        df_bins[col]   = df_bins[col].apply(find_avg)
    df_bins["Time"] = df_bins["Time"].apply(find_last)
    df_bins["Time"] = df_bins["Time"].fillna(method="ffill")
    df_bins.insert(1, 'Time bins (mins)', df_bins.index)
    df_bins = df_bins.rename(columns={"Time": "Date and time"})
    df_bins.index = df_bins["Date and time"]
    
    return(df_bins)
    
def add_headings_and_split_into_sheets(df_bins, inputs):
    
    headings = pd.DataFrame(3*[len(df_bins.columns)*['']],
               index=['Mouse numbers','Genotypes','Treatments'],columns=df_bins.columns)
    for col in headings.columns:
        headings.at['Mouse numbers',col] = ''.join([col[i] if col[i].isdigit() else 
                                                    ' ' for i in range(len(col))])
        for cat in ['Genotypes','Treatments']:
            for key in inputs[cat]:
                if key in col:
                    headings.at[cat,col] = key
    df_bins = pd.concat([headings,df_bins])
    
    # Sort by columns by the genotypes and then the treatments.
    df_bins = df_bins.sort_values(by=['Genotypes','Treatments'], axis=1)
    
    # Split the dataframes into locomotor activity and temperature.
    LA_cols   = [col for col in df_bins.columns if (inputs["LA_activity"] in col)]
    temp_cols = [col for col in df_bins.columns if (inputs["Temperature"] in col)]
    df_LA   = df_bins[["Date and time","Time bins (mins)"] + LA_cols]
    df_temp = df_bins[["Date and time","Time bins (mins)"] + temp_cols]
    
    return(df_LA, df_temp)

def color_code_night_periods(df_bins, df_LA, df_temp):
    
    # Colour code the dark times.
    color_indices = df_bins.between_time('19:00:00', '07:00:00').index
    df_LA = df_LA.style.applymap(cell_color, subset = pd.IndexSlice[color_indices,'Date and time'])
    df_temp = df_temp.style.applymap(cell_color, subset = pd.IndexSlice[color_indices,'Date and time'])
    
    return(df_LA, df_temp)

def export_data(df_LA, df_temp, inputs):
    
    # Export the data.
    with pd.ExcelWriter(inputs['Export destination']) as writer:
        df_LA.to_excel(writer, sheet_name='Locomotor activity data', engine='openpyxl', index=False)
        df_temp.to_excel(writer, sheet_name='Temperature data', engine='openpyxl', index=False)
