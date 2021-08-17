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
from ConvergenceTest import convergenceTest
from FrequencyTest import frequencyTest
from ZeroPointEnergyCorrection import zeroPointEnergyCorrection

### Reads the output directory. Make sure that all the Gaussian output files are placed in the OutputFilesHere directory
### as the files are read from here. Detects total number of files before they are processed so user knows what is being
### being processed.
directory_files = os.listdir("OutputFilesHere")
print(directory_files)
user_input = input("\n" + str(len(directory_files)) + " files were found, press ENTER to continue processing or quit the program to change the files... ")
print("\n\n==================== Beginning File Processing ====================\n")

df = pd.DataFrame(columns=["Title", "Converged?", "Real Frequencies?", "Energy / au", "ZPE-Corrected Energy / au"])
df["Title"] = directory_files
df["Converged?"] = convergenceTest(directory_files)
df["Real Frequencies?"] = frequencyTest(directory_files)
df["Energy / au"], df["ZPE-Corrected Energy / au"] = zeroPointEnergyCorrection(directory_files)


### After all the processing is done, this section handles exporting the DataFrame to a csv file for further processing.
print("\n\n==================== Export Energy Data ====================\n")
print("The first 5 rows of the DataFrame look like: \n")
print(df.head(), "\n")
filename = str(input("Enter a filename as 'example': ")) + ".csv"
df.to_csv(filename, index=False)
exit_choice = input("Process is complete, press ENTER to continue...")