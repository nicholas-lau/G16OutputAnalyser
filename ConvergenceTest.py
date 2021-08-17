def convergenceTest(directory_files):
    ### Imports to handle regex and csv output.
    import re

    ### Initialises empty list which will contain all of the convergence values.
    convergence_list = []

    ### Starts iteration over all files in the directory to determine properties.
    for i in range(len(directory_files)):

        ### Opens each file in the directory in read-mode. Assigns title variable to this value which is used in dataframe construction.
        f = open("OutputFilesHere/" + str(directory_files[i]), "r")

        ### Initialises the count variable with a value of zero. Allows access in the wider namespace.
        convergence = False
        count_converge = 0
        loop_count = 0

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
           
            ### This is the failsafe code that breaks the loop if it manages to cycle through the entire file without
            ### finding anything. After 100000 searches the loop will break.
            elif loop_count == 100000:
                print("I couldn't find any matches, please check this output manually :(")
                convergence = "CHECK ME"
                loop_count = 0
                break

            ### If count = 4 then total convergence is achieved and we print this result. We then break from the while-loop.
            if count_converge == 4:
                print("Total convergence was achieved!")
                convergence = True
                loop_count = 0
                break
            
            ### This determines if the optimisation completed on the basis of negligible forces which is neither failure or
            ### success. Allows user to make informed choice by handling the option explicitly.
            if re.search("Optimization completed on the basis of negligible forces", log_file) != None:
                print("Total convergence was NOT achieved :(")
                print("Optimisation was instead completed on the basis of negligible forces.")
                convergence = "NEGLIGIBLE FORCES"
                loop_count = 0
                break

            ### Increments the loop counter to ensure, after 100,000 cycles the loop is broken - Stops inifinte loop.
            loop_count += 1
        
        ### Closes the open file
        f.close()

        ### Appends the correct convergence to the convergence_list which can later be used to populate the dataframe.
        convergence_list.append(convergence)

    ### Returns the filled convergence_list which can then be used to populate the appropriate column.
    return convergence_list

