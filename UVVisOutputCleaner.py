### Imports necessary files for csv processing.
import re, os
import pandas as pd


### Reads the "TextFilesHere" directory. Make sure all text files you wish to clean are placed in this directory.
directory_files = os.listdir("TextFilesHere")


### Prints all the files the programme found. Enumerates the generated list then prints it to allow the
### user to see all of the files. Waits for user input to continue processing.
print("==================== Finding Files ====================\n")
print("The following files were found in the folder 'TextFilesHere':\n")
for index, name in enumerate(directory_files):
    print(index + 1, name)
user_input = input("\n" + "Press ENTER to continue processing or quit the program to change the files... ")
print("\n\n==================== Beginnning File Cleanup ====================\n")


### Constructs the dataframes ready for data export.
df_peaks = pd.DataFrame(columns=["X / nm", "Y (Oscillator Strength)", "Y (Maybe Epsilon?)"])
df_spectrum = pd.DataFrame(columns=["X / nm", "Y (Epsilon)", "DY/DX"])


### Initialises some global variables for determination of NStates and Data Points.
same_nstates = False
same_dp = False
asking_nstates = None
asking_dpoints = None


### Starts iteration over all files in the "TextFilesHere" directory.
for i in range(len(directory_files)):


    ### Initialises the count_peaks variable with a value of zero. This is reset with each file such that we only iterate over
    ### the correct amount of lines for each respective section.
    count_peaks = 0
    count_spectra = 0


    ### Opens each file in the directory in read-mode. Assigns title variable to this value which is used in dataframe construction.
    f = open("TextFilesHere/" + str(directory_files[i]), "r")
    title = str(directory_files[i])


    ### Gets the number of NStates for each file. On the first pass, this will ask if all are the same which then means the user
    ### will no longer have to type in the value for each subsequent pass. If the values are not the same then the user will then be
    ### prompted in each subsequent pass.
    if same_nstates == False and asking_nstates == None:
        choice1 = str(input("Are the number of NStates used in each file the same? (y/n): "))
        while True:
            if choice1.lower() == "y":
                nstates = int(input("Enter the number of NStates used in all files: "))
                same_nstates = True
                break
            elif choice1.lower() == "n":
                nstates = int(input("Enter the number of NStates used in " + title + ": "))
                asking_nstates = True
                break
            else:
                choice1 = str(input("I'm sorry, I didn't get that. Please enter 'y' or 'n': "))
    elif same_nstates == False and asking_nstates == True:
        nstates = int(input("Enter the number of NStates used in " + title + ": "))


    ### Gets the number of Data Points for each file. On the first pass, this will ask if all are the same which then means the user
    ### will no longer have to type in the value for each subsequent pass. If the values are not the same then the user will then be
    ### prompted in each subsequent pass.
    if same_dp == False and asking_dpoints == None:
        choice2 = str(input("Are the number of Data Points used in each file the same? (y/n): "))
        while True:
            if choice2.lower() == "y":
                dpoints = int(input("Enter the number of Data Points used in all files: "))
                same_dp = True
                break
            elif choice2.lower() == "n":
                dpoints = int(input("Enter the number of Data Points used in " + title + ": "))
                asking_dpoints = True
                break
            else:
                choice2 = str(input("I'm sorry, I didn't get that. Please enter 'y' or 'n': "))
    elif same_dp == False and asking_dpoints == True:
        dpoints = int(input("Enter the number of Data Points used in " + title + ": "))
     
    
    ### Iterates over all lines to grab the requested information.
    while True:
        log_file = f.readline()


        ### Regex search for "Peak information" in string, if found returns memory address != None. The next line is then read before
        ### the for-loop is entered. Entering the for-loop advances the line to the actual data location where the data is then
        ### extracted line-by-line and appended to the df_peaks.
        if re.search("Peak information", log_file) != None:
            log_file = f.readline()
            for x in range(nstates):
                log_file = f.readline()

                ### Extracts the data values for the peak information.
                x_value = float(log_file[6:20])
                y_value = float(log_file[28:40])
                y2_value = log_file[40:]
                y2_value = float(y2_value.strip())

                ### Appends values to df_peaks.               
                df_peaks = df_peaks.append({
                    "X / nm": x_value,
                    "Y (Oscillator Strength)": y_value,
                    "Y (Maybe Epsilon?)": y2_value,
                    }, ignore_index=True)
                count_peaks += 1


        ### Regex search for "Spectra" in string, if found returns memory address != None. The next line is then read before
        ### the for-loop is entered. Entering the for-loop advances the line to the actual data location where the data is then
        ### extracted line-by-line and appended to the df_spectrum.
        if re.search("Spectra", log_file) != None:
            log_file = f.readline()
            for x in range(dpoints):
                log_file = f.readline()

                ### Extracts the data values for the spectrum information.
                x_value = log_file[4:20]
                y_value = log_file[20:40]
                y2_value = log_file[40:]

                ### Removes whitespace and converts them to float datatypes.
                x_value = float(x_value.strip())
                y_value = float(y_value.strip())
                y2_value = float(y2_value.strip())

                ### Appends spectrum values to df_spectrum.
                df_spectrum = df_spectrum.append({
                    "X / nm": x_value,
                    "Y (Epsilon)": y_value,
                    "DY/DX": y2_value,
                    }, ignore_index=True)
                count_spectra += 1


        ### If count_peaks == nstates and count_spectra == dpoints then we have extracted all of the peak information data and
        ### all of the spectrum data. This then appends an ending line before breaking the while-loop allowing for the next part
        ### of the file processing.
        if count_peaks == nstates and count_spectra == dpoints:
            df_peaks = df_peaks.append({
                "X / nm": "----------",
                "Y (Oscillator Strength)": "End of " + str(title),
                "Y (Maybe Epsilon?)": "----------",
                }, ignore_index=True)
            df_spectrum = df_spectrum.append({
                "X / nm": "----------",
                "Y (Epsilon)": "End of " + str(title),
                "DY/DX": "----------",
                }, ignore_index=True)
            print("\nCleaned " + title + "! Moving on to the next file.")
            break


### This section handles exporting the peak information to a csv file for further processing.
print("\n==================== Export Peak Information ====================\n")
print("The first 5 rows of the the peak information look like: \n")
print(df_peaks.head(), "\n")
filename = str("ProcessedFiles/" + input("Enter a filename: ")) + ".csv"
df_peaks.to_csv(filename, index=False)


### This section handles exporting the spectrum information to a csv file for further processing.
print("\n==================== Export Spectrum Data Points ====================\n")
print("The first 5 rows of the Spectrum look like: \n")
print(df_spectrum.head(), "\n")
filename = str("ProcessedFiles/" + input("Enter a filename: ")) + ".csv"
df_spectrum.to_csv(filename, index=False)
exit_choice = input("Process is complete, press ENTER to continue...")
