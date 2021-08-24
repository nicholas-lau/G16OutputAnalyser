"""
#################################################################################
#################################################################################
#################################################################################
############                                                         ############
############                     G16OutputAnalyser                   ############
############                       Nicholas Lau                      ############
############                                                         ############
############                          Hosted:                        ############
############    https://github.com/nicholas-lau/G16OutputAnalyser    ############
############                                                         ############
#################################################################################
#################################################################################
#################################################################################

This program was created as a simple tool to anylse many G16 output files as 
quickly as possible via an automated process. This tool can be used but is not
necessary. If an entry looks wrong, check the file manually.
"""
### Imports section, ignore this.
import os
import pandas as pd
from MiscellaneousFunctions import jobChoice
from ConvergenceTest import convergenceTest
from FrequencyTest import frequencyTest
from ZeroPointEnergyCorrection import zeroPointEnergyCorrection

### Reads the output directory. Make sure that all the required files are placed in the OutputFilesHere directory
### as the files are read from here. Detects total number of files before they are processed so user knows what is being
### being processed.
directory_files = os.listdir("OutputFilesHere")
print(directory_files)
user_input = input("\n" + str(len(directory_files)) + " files were found, press ENTER to continue processing or quit the program to change the files... ")


### Sets up the job listing so users can choose the jobs they want. This list can be expanded with new options when available.
print("\n==================== Job Choice ====================\n")
user_operations = ["Test for Convergence",
                   "Test for Positive Frequencies",
                   "Find Energy and ZPE",
                   "All (excl. UV-Vis cleaning)",
                   "Clean UV-Vis Files",
                   "View DataFrame",
                   "Exit and Export Data"]


### Prints the list of jobs alongside a counter variable for easier job selection.
for count, operation in enumerate(user_operations):
    print(count+1, operation)


### Initialises the DataFrame. The Title column is populated with the filenames.
df = pd.DataFrame(columns=["Title", "Converged?", "Real Frequencies?", "Energy / au", "ZPE-Corrected Energy / au"])
df["Title"] = directory_files


### This is the main operation window and will serve the user with the options available. This should allow easy navigation
### to allow the user to process their files how they choose.
user_choice = input("\nEnter the number corresponding to the job you wish to do: ")
while True:
    
    try:
        int(user_choice)
    
    except:
        user_choice = input("I'm sorry, I didn't catch that. Please enter the number corresponding to the job you wish to do: ")
    
    else:
        ### Searches for file convergence.
        if int(user_choice) == 1:
            print("\n\n==================== Beginning File Processing ====================\n")
            df["Converged?"] = convergenceTest(directory_files)
            jobChoice(user_operations)
            user_choice = input("\nEnter the number corresponding to the job you wish to do: ")


        ### Searches for positive frequencies.
        elif int(user_choice) == 2:
            print("\n\n==================== Beginning File Processing ====================\n")
            df["Real Frequencies?"] = frequencyTest(directory_files)
            jobChoice(user_operations)
            user_choice = input("\nEnter the number corresponding to the job you wish to do: ")


        ### Searches for SCF energy and ZPE.
        elif int(user_choice) == 3:
            print("\n\n==================== Beginning File Processing ====================\n")
            df["Energy / au"], df["ZPE-Corrected Energy / au"] = zeroPointEnergyCorrection(directory_files)
            jobChoice(user_operations)
            user_choice = input("\nEnter the number corresponding to the job you wish to do: ")


        ### Does all of the above in one job.
        elif int(user_choice) == 4:
            print("\n\n==================== Beginning File Processing ====================\n")
            df["Converged?"] = convergenceTest(directory_files)
            df["Real Frequencies?"] = frequencyTest(directory_files)
            df["Energy / au"], df["ZPE-Corrected Energy / au"] = zeroPointEnergyCorrection(directory_files)
            jobChoice(user_operations)
            user_choice = input("\nEnter the number corresponding to the job you wish to do: ")


        ### Cleans UV-Vis files for easier importing.
        elif int(user_choice) == 5:
            print("\n\n==================== Beginning File Processing ====================\n")
            import UVVisOutputCleaner
            jobChoice(user_operations)
            user_choice = input("\nEnter the number corresponding to the job you wish to do: ")


        ### Prints the DataFrame.
        elif int(user_choice) == 6:
            print("The first 5 rows of the DataFrame look like: \n")
            print(df.head(), "\n")
            jobChoice(user_operations)
            user_choice = input("\nEnter the number corresponding to the job you wish to do: ")


        ### Exits the loop and proceeds to data export.
        elif int(user_choice) == 7:
            break
        

        ### Catches all other inputs to stop the program from crashing.
        else:
            user_choice = input("I'm sorry, I didn't catch that. Please enter the number corresponding to the job you wish to do: ")


### After all the processing is done, this section handles exporting the DataFrame to a csv file for further processing.
print("\n\n==================== Export Energy Data ====================\n\n")
print("The first 5 rows of the DataFrame look like: \n")
print(df.head(), "\n")
filename = str("ProcessedFiles/" + input("Enter a filename as 'example': ")) + ".csv"
df.to_csv(filename, index=False)
exit_choice = input("Process is complete, press ENTER to continue...")