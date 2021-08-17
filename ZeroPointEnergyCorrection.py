def zeroPointEnergyCorrection(directory_files):
    ### Imports to handle regex and csv output.
    import re

    ### Initialises empty lists which will contain all of the energy and ZPE values.
    energy_list = []
    zpe_list = []
    
    ### Starts iteration over all files in the directory to determine properties.
    for i in range(len(directory_files)):

        ### Opens each file in the directory in read-mode. Assigns title variable to this value wh
        f = open("OutputFilesHere/" + str(directory_files[i]), "r")

        ### Initialises the count variable with a value of zero. Allows access in the wider namesp
        energy = None
        zpe = None
        scf_final = False
        loop_count = 0

        ### Iterates over the entire file line-by-line to find the "HF=" regex.
        print("Finding the energy for the structure...")
        while True:
            log_file = f.readline()

            ### If no energies are found then this handles the process to break from the while-loop.
            if re.search("Proceeding to internal job step number  2", log_file) != None:
                scf_final = True
            
            ###
            if re.search("SCF Done", log_file) != None and scf_final:
                print("Found the minimum SCF energy.")
                start = log_file.find("=")
                extract_energy = log_file[start+1:start+20]
                energy = extract_energy.strip()
                energy = float(energy)
                break

            elif loop_count == 100000:
                print("I couldn't find any matches, please check this output manually :(")
                energy = "CHECK ME"
                loop_count = 0
                break
            
            ### Increments the loop counter to ensure, after 100,000 cycles the loop is broken - Stops inifinte loop.
            loop_count += 1
        
        ### Appends the correct convergence to the convergence_list which can later be used to populate the dataframe.
        energy_list.append(energy)

        ### Iterates over the entire file line-by-line to find the "Sum of electronic and zero-point Energies" regex. Regex search for
        ### "Sum of electronic and zero-point Energies" in string, if found returns memory address != None. The zero-point corrected energy
        ### is then extracted as a float. If no zero-point corrected energy is found then the output prints the error message and overwrites
        ### the variable with an error message.
        print("Finding the Zero-Point Corrected Energy...")
        while True:
            log_file = f.readline()
            
            if re.search("Sum of electronic and zero-point Energies", log_file) != None:
                print("Zero-point corrected energy was found!\n")
                zpe = log_file[45:]
                zpe = float(zpe.strip())
                break
            
            elif loop_count > 1000000:
                print("No zero-point corrected energy was found, this calculation should be checked! :(")
                zpe = "CHECK ME"
                break
            
            else:
                loop_count += 1

        ### Appends the correct convergence to the convergence_list which can later be used to populate the dataframe.
        zpe_list.append(zpe)
        
        ### Closes the open file
        f.close()

    return energy_list, zpe_list
