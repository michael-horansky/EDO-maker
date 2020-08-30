import matplotlib.pyplot as plt
import math

log_file = open("EDO_log.txt", "w+")

def interval_to_cents(a):
    return(1200 * math.log(a, 2))

def generate_edo(edo):
    halfstep = 2**(1.0/edo)
    result = [1.0]
    for i in range(edo-1):
        result.append(result[-1]*halfstep)
    result.append(2.0)
    return result

def fraction_approximator(x, denom):
    exact_numer = x * denom
    numer = round(exact_numer)
    return(numer)

def iterate_over_denom(set_of_interest, denom):
    result = []
    for i in set_of_interest:
        result.append(fraction_approximator(i, denom)/denom)
    return(result)

def find_offset(set1, set2):
    off_set = []
    for i in range(len(set1)):
        if set1[i] == 0:
            cur_offset = 1
        else:
            cur_offset = set2[i]/set1[i]
        off_set.append(cur_offset)
    return off_set

def find_fraction(x, tolerance):
    cur_denom = 1.0
    while(True):
        cur_numer = fraction_approximator(x, cur_denom)
        val = cur_numer/cur_denom
        offset = abs(1 - val/x)
        if offset < tolerance:
            break
        cur_denom += 1
    return cur_numer, cur_denom

def find_line(x, no_of_best_results = 5, keep_all_results = True):
    results = []
    best_results = []

    cur_denom = 1
    last_denom = 1
    exp_change = 1

    cur_numer = fraction_approximator(x, cur_denom)
    cur_offset = abs(1 - (cur_numer/cur_denom)/x)
    last_offset = cur_offset
    results.append([cur_numer, cur_denom, cur_offset, 1, 1.0])
#    while(len(results) < 50):
    while((len(best_results) < no_of_best_results - 1 or cur_denom - last_denom <= exp_change) and last_offset > 0):
        cur_denom += 1
        cur_numer = fraction_approximator(x, cur_denom)
        cur_offset = abs(1 - (cur_numer/cur_denom)/x)
        if cur_offset < last_offset:
            if (cur_denom - last_denom == exp_change):
                #pokracujeme v linii, hladajme koniec
                True
            else:
                #linia sa zmenila
                exp_change = last_denom
                if (results[-1][0]/results[-1][1])/x < 1.029302237 and (results[-1][0]/results[-1][1])/x > 0.971531941:
                #if abs(interval_to_cents(results[-1][0]/results[-1][1]/x)) < 50:
                    best_results.append(results[-1])
                results.append("break")
            if cur_offset == 0:
                results.append([cur_numer, cur_denom, cur_offset, cur_denom - last_denom, 0])
                break
            results.append([cur_numer, cur_denom, cur_offset, cur_denom - last_denom, last_offset/cur_offset])
            last_offset = cur_offset
            last_denom = cur_denom
    best_results.append(results[-1])
    if keep_all_results:
        return([results, best_results])
    else:
        return(best_results)

spaces = {1 : "      ", 2 : "     ", 3 : "    ", 4 : "   ", 5 : "  ", 6 : " "}

existing_intervals = {
    1 : {1 : "perfect unison"},
    2 : {1 : "perfect octave, duplex"},
    3 : {2 : "perfect fifth, sesquialterum"},
    4 : {3 : "perfect fourth, sesquitertium"},
    5 : {
        3 : "major sixth",
        4 : "major third, sesquiquartum"
    },
    6 : {5 : "minor third, sesquiquintum"},
    8 : {5 : "minor sixth"},
    9 : {
        8 : "major second, sesquioctavum",
        5 : "alternate minor seventh"
    },
    10 : {9 : "alternate major second"},
    15 : {8 : "major seventh"},
    16 : {
        15 : "minor second",
        9 : "minor seventh"
    },
    25 : {18 : "diminished fifth"},
    27 : {
        16 : "major sixth",
        20 : "alternate perfect fourth",
        25 : "alternate minor second"
    },
    32 : {27 : "alternate minor third, semiditone"},
    40 : {27 : "alternate perfect fifth"},
    45 : {32 : "augmented fourth"},
    50 : {27 : "alternate major seventh"},
    81 : {64 : "ditone"},
    128 : {125 : "diesis"},
    256 : {243 : "limma"},
    729 : {512 : "tritone"},
    2187 : {2048 : "apotome"},
    524288 : {531441 : "pythagorean comma"}
}

def print_result_line(orig_number, result_line, my_offset = 0, denom_change = False, offset_change = False, try_matching = False):

    #numerator ; denominator ; offset ; denominator change ; offset change
    global spaces

    my_offset_string = ""
    for i in range(my_offset):
        my_offset_string += " "

    len1 = len(str(result_line[0]))
    len2 = len(str(result_line[1]))
    if len1 < 7:
        spaces1 = spaces[len1]
    else:
        spaces1 = ""
    if len2 < 7:
        spaces2 = spaces[len2]
    else:
        spaces2 = ""
    denom_string = ""
    offset_string = ""
    if denom_change:
        denom_string = " ; denom_change = " + str(result_line[3])
    if offset_change:
        offset_string = " ; offset_change = " + str.format("{0:.3E}",result_line[4])

    try:
        match_string = " | " + existing_intervals[result_line[0]][result_line[1]]
    except KeyError:
        match_string = ""

    return(my_offset_string + str(result_line[0]) + spaces1 + " : " + str(result_line[1]) + spaces2 + " || offset = " + str.format("{0:.3E}",result_line[2]) + " ; cent difference = " + str.format("{0:.3f}",interval_to_cents(result_line[0]/result_line[1]/orig_number)) + denom_string + offset_string + match_string)

def print_line(x, my_line, highlight_significant_results = True):

    global spaces

    print("Approximating the value " + str(x) + ":")
    for i in my_line[0]:
        if i == "break":
            print("     -----------------------------------------")
        else:
            print(print_result_line(x, i, 4, True))
    if highlight_significant_results:
        print("The significant results obtained:")
        for i in my_line[1]:
            print(print_result_line(x, i, 4, False, False, True))

def analyze_set(set_of_interest, no_of_best_results = 5):
    log_file.write("Set analysis begins\n")
    best_result_set = []
    for i in range(len(set_of_interest)):
        best_result_set.append(find_line(set_of_interest[i], no_of_best_results, False))
        set_item_string = "Analyzing item no. " + str(i) + "; cents = " + str(interval_to_cents(set_of_interest[i])) + "; value = " + str(set_of_interest[i])
        print(set_item_string)
        log_file.write(set_item_string + "\n")
        for j in best_result_set[-1]:
            result_line_string = print_result_line(set_of_interest[i], j, 4, False, False, True)
            print(result_line_string)
            log_file.write(result_line_string + "\n")
    return(best_result_set)

def UI():
    exit = False
    while(not exit):
        cmd = input("> ")
        if cmd == "analyze":
            print("  Specify the value of divisions in your EDO")
            while(True):
                choice = input("  > ")
                try:
                    val = int(choice)
                    if val >= 1:
                        break
                    else:
                        print("  Please type an integer greater than 0")
                except ValueError:
                    print("  Please enter the number of your choice.")
            base_set = generate_edo(val)
            print("  Specify the number of significant approximations per pitch")
            while(True):
                choice = input("  > ")
                try:
                    val = int(choice)
                    if val >= 1:
                        break
                    else:
                        print("  Please type an integer greater than 0")
                except ValueError:
                    print("  Please enter the number of your choice.")
            analyze_set(base_set, val)
        elif cmd == "approx":
            print("  Specify the number you want to approximate")
            while(True):
                choice = input("  > ")
                try:
                    val = float(choice)
                    if val >= 0:
                        break
                    else:
                        print("  Please type a non-negative number")
                except ValueError:
                    print("  Please enter the number of your choice.")
            x = val
            print("  Specify the number of significant approximations")
            while(True):
                choice = input("  > ")
                try:
                    val = int(choice)
                    if val >= 1:
                        break
                    else:
                        print("  Please type an integer greater than 0")
                except ValueError:
                    print("  Please enter the number of your choice.")
            significant_approximations = val
            print("  Do you want to display only significant results? (Y/N)")
            while(True):
                choice = input("  > ")
                try:
                    val = str(choice)
                    if val.upper() == "Y":
                        val = False
                        break
                    elif val.upper() == "N":
                        val = True
                        break
                    else:
                        print("  Please type either 'Y' or 'N'")
                except ValueError:
                    print("  Please type either 'Y' or 'N'")
            
            my_best_results = find_line(x, significant_approximations, val)
            #print(my_best_results)
            if val:
                print_line(x, my_best_results, False)
            else:
                print_line(x, [my_best_results, 0], False)
            #print("  Best fit for given denominator: " + str(fraction_approximator(x, val)))
        elif cmd == "help":
            print("EDO Maker currently supports these commands:")
            print("  'analyze': Specify a number of divisions of the octave and obtain a list of rational approximations of pitches present in your EDO.")
            print("  'approx': Obtain a list of progressively more accurate rational approximations of specified number.")
            print("  'help': Obtain a list of available commands.")
            print("  'exit': Exit the program.")
            print("This project is open-source.")
        elif cmd == "exit":
            exit = True
        else:
            print("Type 'help' to list all the possible options or 'exit' to exit the program")

#evaluate the set of interest

#base_set = generate_edo(12)
#analyze_set(base_set, 5)
UI()

#print(interval_to_cents(16/15))

#print(find_fraction(base_set[6], 0.05))
#for i in base_set:

#result_set = iterate_over_denom(base_set, my_denominator)
#offsets = find_offset(base_set, result_set)

#my_line = find_line(2**(5/12))
#print_line(2**(5/12), my_line)
#print(len(str(26465)))

#plt.plot(base_set, result_set, label="approximations")
#plt.plot(base_set, offsets, label="offsets")
#plt.legend()
#plt.show()
#plt.close()
