### Imports to handle regex and csv output
import re, os
import decimal
import pandas as pd

### Initialiases an empty dataframe which will later be filled with output file data.
df = pd.DataFrame(columns=["Title", "Converged?", "Real Frequencies?", "Energy / au", "Energy / kJ mol-1"])

### Initialises important global variables and conversion factor.
title = None
convergence = None
real_frequency = None
energy_au = None
energy_kjmol = None
AU_TO_KJMOL = 2625.5

### Reads the output directory. Make sure that all the Gaussian output files are placed in the OutputFilesHere directory
### as the files are read from here. Detects total number of files before they are processed so user knows what is being
### being processed.
directory_files = os.listdir("OutputFilesHere")
print(directory_files)
user_input = input("\n" + str(len(directory_files)) + " files were found, press ENTER to continue processing or quit the program to change the files... ")
print("\n\n==================== Beginning File Processing ====================\n")

### Starts iteration over all files in the directory to determine properties.
for i in range(len(directory_files)):

    ### Resets the variables to the default values.
    title = None
    convergence = False
    real_frequency = False
    energy_au = None
    energy_kjmol = None

    ### Opens each file in the directory in read-mode. Assigns title variable to this value which is used in dataframe construction.
    f = open("OutputFilesHere/" + str(directory_files[i]), "r")
    title = str(directory_files[i])

    ### Initialises the count variable with a value of zero. Allows access in the wider namespace.
    count_converge = 0
    count_freq = 0

    ### Iterates over the entire file line-by-line to find the "Converged?" regex.
    print("\nBeginning search for convergence...")
    print(directory_files[i])
    while True:
        log_file = f.readline()

        ### Regex search for "Converged?" in string, if found returns memory address != None. Initialises
        ### count_converge = 0 then iterates over the next 4 lines to determine if total convergence is achieved. If
        ### "YES" in line then count incremented else the for-loop is broken and we return to the while-loop.
        if re.search("Converged\?", log_file) != None:
            count_converge = 0
            for x in range(4):
                log_file = f.readline()
                if re.search("YES", log_file) != None: 
                    count_converge += 1
                else:
                    break
       
        elif re.search("Normal termination of Gaussian 16", log_file) != None:
           print("Total convergence was NOT achieved :(")
           break  

        elif re.search("Error termination", log_file) != None:
           print("Total convergence was NOT achieved :(")
           break       
        
        ### If count = 4 then total convergence is achieved and we print this result. We then break from the while-loop.
        if count_converge == 4:
            print("Total convergence was achieved!")
            convergence = True
            break
        
    
    ### Iterates over the entire file line-by-line to find the "Frequencies --" regex.
    print("Determining real and imaginary frequencies...")
    while True:
        log_file = f.readline()

        ### Regex search for "Frequencies --" in string, if found returns memory address != None. Initialises
        ### count_freq = 0 then extracts frequencies from the line and converts them to floats. Iterates over
        ### the floats and counts the positive values. If all values are positive
        if re.search("Frequencies --", log_file) != None:
            count_freq = 0

            ### Extracts floats. Extraction first then uses for-loop to convert frequencies to float. The count_freq
            ### variable is updated for each positive frequency. 
            extract_freqs = log_file[15:]
            freqs = extract_freqs.strip()
            freqs = ",".join(freqs.split())
            freqs = freqs.split(",")
            for item in range(len(freqs)):
                freqs[item] = float(freqs[item])
                if freqs[item] > 0:
                    count_freq += 1
            
            ### If the count_freq is 3 then this is a stationary point and the structure is optimised to a minimum. Else
            ### one or more of the frequencies are imaginary and this is therefore a transition state.
            if count_freq == 3:
                print("Lowest frequencies are real. This is a stationary point!")
                real_frequency = True
            else:
                print("Lowest frequencies are Imaginary. This is a transition state :(")
            break
        
        ### If no frequencies are found then this handles the process to break from the while-loop.
        """elif re.search("Normal termination of Gaussian 16", log_file) != None:
            print("No frequencies were found :(")
            break"""

        if re.search("Error termination", log_file) != None:
           print("No frequencies were found :(")
           break   
        
    ### Iterates over the entire file line-by-line to find the "HF=" regex.
    print("Finding the energy for the structure...")
    while True:
        log_file = f.readline()

        ### If no energies are found then this handles the process to break from the while-loop.
        if re.search("Normal termination of Gaussian 16", log_file) != None:
            print("No energies were found :(")
            energy_au = 0
            energy_kjmol = 0
            break

        elif convergence == False and real_frequency == False:
            print("Energies were not calculated. Convergence not achieved.")
            energy_au = 0
            energy_kjmol = 0
            break

        ### Regex search for "HF=" in string, if found returns memory address != None. The energy_string variable stores
        ### the output of the .findall() as a list which is then accessed via energy_au and conveted to a string. Use
        ### string conversion first so that accuracy of decimal places is preserved. This is an issue with float datatypes
        ### so we process in decimal datatypes. If initial energy string not found then test for length of the string found,
        ### actual energies should be 20 characters long so if less then proceed to grab energy across multiple lines. First
        ### finds part 1 of energy then reads in next line and gets part 2 of energy, combines them to the first index and
        ### evaluates as previous.
        try:
            if re.search("HF=", log_file) != None:
                print("Found the energy for the structure!")
                energy_string = re.findall("HF=-?[0-9]*\.[0-9]*", log_file)
                energy_string_index = log_file.find("HF=")
                for i in range(energy_string_index, len(log_file)):
                    if log_file[i] == "\\":
                        end_string_index = i 
                    else:
                        end_string_index = -1
                if len(str(energy_string)) != 20 & end_string_index == -1:
                    energy_string = re.findall("HF=-[0-9]*", log_file)
                    print(energy_string)
                    log_file = f.readline()
                    print(log_file)
                    energy_string.append(re.findall("[0-9]*\.[0-9]*", log_file)[0])
                    print(energy_string)
                    energy_string[0] = energy_string[0] + energy_string[1]
                    print(energy_string)
                energy_au = str(energy_string[0][3:])
                energy_kjmol = str(decimal.Decimal(energy_au) * decimal.Decimal(AU_TO_KJMOL))
                break
        
        except IndexError:
            print("Could not extract energy. Manual Extraction required.")
            energy_au = 0
            energy_kjmol = 0
            break

    ### Collects the data together and appends it as a row to the dataframe before starting the process again for the next file.
    df = df.append({
        "Title": title,
        "Converged?": convergence,
        "Real Frequencies?": real_frequency,
        "Energy / au": decimal.Decimal(energy_au),
        "Energy / kJ mol-1": decimal.Decimal(energy_kjmol)
        }, ignore_index=True)

### Finds the minimum energy across all structures then calculates the relative energy for each other structure. Values are then
### converted to string representation to preserve full accuracy. Values are appended to a list and the list then added as a new
### column to the DataFrame.
minimum_energy = str(df["Energy / kJ mol-1"].min())
energy_comparison = []
structure_checker = []
for i in range(len(directory_files)):
    if str(df.iloc[i, 4]) == minimum_energy:
        energy_comparison.append(str(0))
    else:
        relative_energy = str(decimal.Decimal(df.iloc[i, 4]) - decimal.Decimal(minimum_energy))
        energy_comparison.append(relative_energy)
        if float(relative_energy) > 100:
            structure_checker.append(i)
df["Energy Difference / kJ mol-1"] = energy_comparison

### Prints the record for the lowest energy structure found.
print("\n\n==================== Lowest Energy Structure ====================\n")
print("The lowest energy value is:\n")
print(df[df["Energy / kJ mol-1"] == df["Energy / kJ mol-1"].min()])

### Prints the records where there may be problematic structures.
print("\n\n==================== Problematic Structures ====================\n")
print("The entries may need your attention:\n")
print(df.iloc[structure_checker])    

### After all the processing is done, this section handles exporting the DataFrame to a csv file for further processing.
print("\n\n==================== Export Energy Data ====================\n")
print("The first 5 rows of the DataFrame look like: \n")
print(df.head(), "\n")
filename = str(input("Enter a filename as 'example.csv': "))
df.to_csv(filename, index=False)
exit_choice = input("Process is complete, press ENTER to continue...")
