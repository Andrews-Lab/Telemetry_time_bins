import PySimpleGUI as sg

def default_values():
    
    default = {}

    # Choose the path of a folder with the .ASC file, so the code can import every 
    # file in the folder.
    # There should not be a slash at the end of these folder paths.
    default['Import location'] = r'/Users/hazza/Desktop/Telemetry code/Import'
    default['Export location'] = r'/Users/hazza/Desktop/Telemetry code/Export'
    
    # Type in keywords in each column heading.
    # Genotypes and treatments are optional and can be left as [].
    default['Genotypes'] = ['AgRP CRE', 'WT']
    default['Treatments'] = ['PDAC', 'PBS']
    default['Temperature'] = 'Deg. C'
    default['LA_activity'] = 'Cnts'
    default['Times'] = ['Date', 'Time']
    
    # Choose the time bin length (in mins).
    # If the raw data is collected in 3 min intervals, ensure the time bin length is 
    # 3, 6, 9, ... mins.
    default['Time bin (mins)'] = 15
    
    return(default)

def GUI(default):
    
    # Create a dictionary with the inputs from the GUI.
    inputs = {}
    
    # Create a GUI.
    sg.theme("DarkTeal2")
    layout = [
        [sg.T("")], [sg.Text("Import the .asc file and export an excel file.")],
        [sg.T("")], [sg.Text("Choose a folder for the import location"), 
                     sg.Input(default_text=default['Import location'],key="Import" ,enable_events=True), 
                     sg.FolderBrowse(key="Import2")],
        [sg.T("")], [sg.Text("Choose a folder for the export location"), 
                     sg.Input(default_text=default['Export location'],key="Export" ,enable_events=True), 
                     sg.FolderBrowse(key="Export2")],
        [sg.T("")], [sg.T("")], [sg.Text("Use a comma to separate each item in a list.")],
        [sg.T("")], [sg.Text("Keywords for the genotypes (optional)",size=(30,1)),
                     sg.Input(default_text=', '.join(default['Genotypes']), key="Genotypes",enable_events=True)],
        [sg.T("")], [sg.Text("Keywords for the treatments (optional)",size=(30,1)), 
                     sg.Input(default_text=', '.join(default['Treatments']), key="Treatments",enable_events=True)],
        [sg.T("")], [sg.Text("Keyword for the temperature data",size=(30,1)), 
                     sg.Input(default_text=default['Temperature'], key="Temperature",enable_events=True)],
        [sg.T("")], [sg.Text("Keyword for the locomotor activity data",size=(30,1)), 
                     sg.Input(default_text=default['LA_activity'], key="LA_activity",enable_events=True)],
        [sg.T("")], [sg.Text("Keywords for the date and time columns",size=(30,1)), 
                     sg.Input(default_text=', '.join(default['Times']), key="Times",enable_events=True)],
        [sg.T("")], [sg.T("")], [sg.Text("If the raw data is collected in 3 min intervals, "
                                         "ensure the time bin length is 3, 6, 9, ... mins.")],
        [sg.T("")], [sg.Text("Time bin length (mins)"),
                     sg.Input(default_text=default['Time bin (mins)'], key="Time_bin",enable_events=True, size=(10,1))],
        [sg.T("")], [sg.Button("Submit")]
              ]
    window = sg.Window('Telemetry analysis', layout)
        
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            window.close()
            exit()
        elif event == "Submit":
            inputs['Import location'] = values["Import"] + '/'
            inputs['Export location'] = values["Export"] + '/'
            inputs['Genotypes'] = [x.strip() for x in values["Genotypes"].split(',')]
            inputs['Treatments'] = [x.strip() for x in values["Treatments"].split(',')]
            inputs['Temperature'] = values["Temperature"]
            inputs['LA_activity'] = values["LA_activity"]
            inputs['Times'] = [x.strip() for x in values["Times"].split(',')]
            inputs['Time bin (mins)'] = float(values["Time_bin"])
            window.close()
            break
        
    return(inputs)
