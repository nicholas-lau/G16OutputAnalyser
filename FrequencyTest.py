def frequencyTest(directory_files):
    ### Imports to handle regex and csv output.
    import re

    ### Initialises empty list which will contain all of the frequency values.
    frequency_list = []

    ### Starts iteration over all files in the directory to determine properties.
    for i in range(len(directory_files)):

        ### Opens each file in the directory in read-mode. Assigns title variable to this value which is used in dataframe construction.
        f = open("OutputFilesHere/" + str(directory_files[i]), "r")

        ### Initialises the count variable with a value of zero. Allows access in the wider namespace.
        real_frequency = False
        loop_count = 0

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
                loop_count = 0
                break
            
            ### This is the failsafe code that breaks the loop if it manages to cycle through the entire file without
            ### finding anything. After 100000 searches the loop will break.
            if loop_count == 100000:
                print("I couldn't extract any frequencies, please check this output manually :(")
                real_frequency = "CHECK ME"
                loop_count = 0
                break

            if re.search("Error termination", log_file) != None:
               print("No frequencies were found :(")
               break  
            
            ### Increments the loop counter to ensure, after 100,000 cycles the loop is broken - Stops inifinte loop.
            loop_count += 1 
            
        ### Closes the open file
        f.close()

        ### Appends the correct frequency to the convergence_list which can later be used to populate the dataframe
        frequency_list.append(real_frequency)
    
    ### Returns the filled frequency_list which can then be used to populate the appropriate column.
    return frequency_list
            