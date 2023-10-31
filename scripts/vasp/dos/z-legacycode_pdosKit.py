#!/usr/bin/env python3


import os
import re
import sys


def translate_atomset(atom_select, atom_list):
    """
    Translate "curve_atomset" into "atom_index"
    :param atom_select: the atoms user hope to select
    :param atom_list: in [H H O] form
    :return: list of translated atom indexes
    """
    dosin_atom = atom_select.lower().replace(" ", "").split(",")
    atom_index = []
    for index in dosin_atom:
        if index[0].isalpha():
            if index == "all":
                atom_index = list(range(len(atom_list)))
                break
            else:
                for atom_list_i in list(range(len(atom_list))):
                    if atom_list[atom_list_i].lower() == index:
                        atom_index.append(atom_list_i)
        elif index[0].isdigit():  # Caution! Atom list starting from "0"!
            if "-" in index:  # if comes in the "range" form ("1-20")
                atom_index.extend(list(range(int(index.split("-")[0]) - 1, int(index.split("-")[1]))))
            else:
                atom_index.append(int(index) - 1)
        else:
            print("\033[31mPlease check your atom assignment in PDOSIN!\033[0m")
            sys.exit(1)
    # Check repeated elements in the atom index
    atom_index = [int(i) for i in atom_index]
    if not len(atom_index) == len(set(atom_index)):
        print("\033[31mDuplicative atom found in PDOSIN! Please check!\033[0m")
        sys.exit(1)

    return atom_index


def read_pdosin():
    """
    Read user settings from "PDOSIN"
    :return: settings, curve_details
    """
    # Judge if an item is a number
    def is_number(string):
        """
        Judge if a string is a number or not
        :param string:
        :return:
        """
        try:
            float(string)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(string)
            return True
        except (TypeError, ValueError):
            pass
        return False

    # Sort lines in PDOSIN into settings and curve details
    def sort_dosin_line(plot_block):
        plot_curve = {}  # plot_curve[curve_index] = (dict)curve_para
        count = 0
        for line in plot_block:
            count += 1
            line_split = re.sub(r"\s*,\s*", ",", line.strip()).split()

            # Judge if orbital assignment division in PDOSIN is rational
            if not len(line_split) == 6:
                print("\033[31mPlease read the tips in PDOSIN and check your orbital assignment!\033[0m")
                sys.exit(1)

            # sort every parameter in curve_line into the dictionary
            curve_para = {"index": int(line_split[0]), "atom": line_split[1], "orbital": line_split[2:6]}

            # convert orbital selection
            if curve_para["orbital"][0].lower() == "s":
                curve_para["orbital"][0] = "1"
            elif curve_para["orbital"][0].lower() == "nos":
                curve_para["orbital"][0] = "0"

            if curve_para["orbital"][1].lower() == "p":
                curve_para["orbital"][1] = "1,1,1"
            elif curve_para["orbital"][1].lower() == "nop":
                curve_para["orbital"][1] = "0,0,0"

            if curve_para["orbital"][2].lower() == "d":
                curve_para["orbital"][2] = "1,1,1,1,1"
            elif curve_para["orbital"][2].lower() == "nod":
                curve_para["orbital"][2] = "0,0,0,0,0"

            if curve_para["orbital"][3].lower() == "f":
                curve_para["orbital"][3] = "1,1,1,1,1,1,1"
            elif curve_para["orbital"][3].lower() == "nof":
                curve_para["orbital"][3] = "0,0,0,0,0,0,0"

            # check the number of suborbitals
            if not (len(curve_para["orbital"][0]) == 1 and len(curve_para["orbital"][1].split(",")) == 3 and len(curve_para["orbital"][2].split(",")) == 5 and len(curve_para["orbital"][3].split(",")) == 7):
                print("\033[31mPlease read the tips in PDOSIN and check your orbital assignment!\033[0m")
                sys.exit(1)

            # judge if suborbitals are 0 or 1
            for orbital in curve_para["orbital"]:
                for suborbital in orbital.split(","):
                    if suborbital not in ["0", "1"]:
                        print("\033[31mIllegal orbital assigned in PDOSIN!\033[0m")
                        sys.exit(1)

            # add data to the dictionary
            plot_curve[count] = curve_para

        return plot_curve

    if os.path.exists("PDOSIN"):
        with open("PDOSIN", mode="r", encoding="utf-8") as pdosinf:
            dosin = []
            for line in pdosinf:  # read lines not starting with "#" or empty
                if not (line.strip().startswith("#") or len(line.strip()) == 0):
                    dosin.append(line.strip())
        # Sort lines in PDOSIN into "settings" and "curve details"
        # count total number of plots
        plot_count = 0
        while True:
            try:
                dosin.index(f"plot {plot_count + 1}")  # try to locate "plot N" indexes in PDOSIN
                plot_count += 1
            except ValueError:
                break

        # Read E_fermi and SPIN
        settings = {}
        for line in dosin[:dosin.index("plot 1")]:
            settings[line.replace(" ", "").split("=")[0].lower()] = line.replace(" ", "").split("=")[1].split("#")[0]  # strings are lowered here!

        # test if "spin" is legal
        if not settings["spin"] in ["both", "up", "down"]:
            print("\033[31mSpin illegal in PDOSIN!\033[0m")
            sys.exit(1)
        if (settings["spin"] == "down" or settings["spin"] == "both") and ispin == 1:  # testline
            print("\033[31mSpin illegal in PDOSIN (ISPIN is 1, please use \"up\")!\033[0m")
            sys.exit(1)

        # test if "e_fermi" is legal
        if not len(settings["e_fermi"]) == 0:
            if not is_number(settings["e_fermi"]):
                print("\033[31mE_fermi illegal in PDOSIN!\033[0m")
                sys.exit(1)
        else:
            print(f"\033[31mYou MUST specify the Fermi level in PDOSIN!\033[0m")
            sys.exit(1)

        # Sort each plot block into dictionary
        curve_details = {}
        count = 1
        while count <= (plot_count - 1):
            block_start = dosin.index(f'plot {count}') + 1
            block_end = dosin.index(f'plot {count + 1}')
            curve_details[count] = sort_dosin_line(dosin[block_start:block_end])
            count += 1
        # last block (without an end-block indicator)
        block_start = dosin.index(f'plot {count}') + 1
        curve_details[count] = sort_dosin_line(dosin[block_start:])

    # Generate a PDOSIN template
    else:
        print('\033[33m\"PDOSIN\" not found! A template has been generated!\033[0m')
        pdosin_template = '''\
###############++++++ PDOSkit Settings ++++++###############
E_fermi                  =             # You MUST specify the Fermi level! 
Spin                     =  both       # up, down or both (up if ISPIN is 1)

###############++++++++ Plot Setting ++++++++###############
# Tips: Atom: "1-3", "5", "Fe" or combined
#       Orbital: 0/1 to exclude/include; p/d/f or nop/nod/nof to include/exclude all suborbitals
#       (Caution! suborbitals shall be separated by comma ",", while orbitals shall be spaces " ")

plot 1
 #   curve   atom   s    py  pz  px    dxy  dyz  dz2  dxz  dx2-y2    fy3x2 fxyz fyz2 fz3 fxz2 fzx2 fx3  
     1       all    1    0,  0,  0     0,   0,   0,   0,   0         0,    0,   0,   0,  0,   0,   0     
     2       all    0    1,  1,  1     0,   0,   0,   0,   0         0,    0,   0,   0,  0,   0,   0    
     3       all    0    0,  0,  0     1,   1,   1,   1,   1         0,    0,   0,   0,  0,   0,   0   
     4       all    0    0,  0,  0     0,   0,   0,   0,   0         1,    1,   1,   1,  1,   1,   1    

plot 2  
 #   curve   atom   s    py  pz  px    dxy  dyz  dz2  dxz  dx2-y2    fy3x2 fxyz fyz2 fz3 fxz2 fzx2 fx3  
     1       all    1    nop           nod                           nof     
     2       all    0    p             nod                           nof    
     3       all    0    nop           d                             nof   
     4       all    0    nop           nod                           f  
'''

        with open("PDOSIN", mode="w", encoding="utf-8") as tempf:
            tempf.write(pdosin_template)
        sys.exit(0)

    return settings, curve_details


def read_vasprun():
    """
    Read atom-info and PDOS data from "vasprun.xml" file
    :return: vasprun_dos[atom_index][spin][line][column], atom_list, nedos, ispin
    """
    if os.path.exists("vasprun.xml"):
        with open("vasprun.xml", mode="r", encoding="iso-8859-1") as datafile:
            vasprun_input = []
            for line in datafile:
                vasprun_input.append(line.strip())  # remove spaces

        # Get NEDOS from vasprun.xml
        for line in vasprun_input:
            if "NEDOS" in line:
                nedos = int(re.findall("\\d+", line)[0])
                break  # escape from loop upon "NEDOS" found

        # Get ISPIN from vasprun.xml
        for line in vasprun_input:
            if "ISPIN" in line:
                ispin = int(re.findall("\\d+", line)[0])
                break  # escape from loop upon "ISPIN" found

        # Organise atoms into list
        atom_list = []  # containing the list of all atoms, like "C H H O O N"
        atominfo_s = vasprun_input.index('<atominfo>') + 8  # atom info starts
        atominfo_e = vasprun_input.index('<array name="atomtypes" >') - 2  # atom info ends
        for line in vasprun_input[atominfo_s:atominfo_e]:  # read atom info in vasprun.xml to the list
            atom_list.append(line.lstrip("<rc><c>").rstrip("</c></rc>").replace("</c><c>", "").split()[0])

        # Organise PDOS for each atom (spin up and down)
        vasprun_dos = {}
        for atom in range(len(atom_list)):  # Atom index starting from "0" !!!
            up_start = vasprun_input.index(f'<set comment=\"ion {atom + 1}\">') + 2  # PDOS data starts
            down_start = up_start + nedos + 2  # PDOS data ends
            dos_atom_up = vasprun_input[up_start:up_start + nedos]
            dos_atom_down = vasprun_input[down_start:down_start + nedos]
            # Remove "<r>" and "</r>" from data in "vasprun.xml"
            dos_atom_up = [line.lstrip("<r>").rstrip("</r>").strip().split() for line in dos_atom_up]
            dos_atom_down = [line.lstrip("<r>").rstrip("</r>").strip().split() for line in dos_atom_down]
            vasprun_dos[atom] = [dos_atom_up, dos_atom_down]

        # vasprun_dos[atom_index][spin][line][column]
        return vasprun_dos, atom_list, nedos, ispin

    # No "vasprun.xml" file found
    else:
        print("\033[31m\"vasprun.xml\" file not found at working directory!\033[0m")
        sys.exit(1)


def prepare_curve_data(dos_data, nedos, atom_index, orbital):
    """
    Prepare PDOS data for each curve (up and down)
    :param dos_data: all DOS data for each atom and for each suborbital
    :param nedos:
    :param atom_index: atom index list
    :param orbital: orbital info (9 or 17 * 0/1)
    :return: curve_data = (y_up, y_down)
    """
    # Judge if f suborbitals are present
    num_of_suborbitals = len(dos_data[0][0][0])
    if num_of_suborbitals == 17:  # energy*1, s*1, p*3, d*5, f*7
        f_included = True
    elif num_of_suborbitals == 10:  # energy*1, s*1, p*3, d*5
        f_included = False
    else:
        print("\033[33mSuborbital condition unknown. Please contact the author.\033[0m")
        sys.exit(2)

    # Organise PDOS data for each atom in atom_index
    pdos_up = [[0.0] * (num_of_suborbitals - 1) for row in range(nedos)]  # create an empty spin_up sheet
    pdos_down = [[0.0] * (num_of_suborbitals - 1) for row in range(nedos)]  # create an empty spin_down sheet
    for atom in atom_index:  # atom index starts from 0
        for row in range(nedos):
            for column in range(num_of_suborbitals - 1):  # dos_data has one more column !!!
                pdos_up[row][column] += float(dos_data[atom][0][row][column + 1])
                if ispin == 2:  # spin_down info available only when ISPIN == 2
                    pdos_down[row][column] += float(dos_data[atom][1][row][column + 1])

    # Prepare y-coordinate lists
    y_up_list = []
    y_down_list = []
    for row in range(nedos):
        y_up = 0
        y_down = 0

        # Adding s/p/d/f suborbitals information
        # s orbital
        y_up += pdos_up[row][0] * int(orbital[0])
        y_down -= pdos_down[row][0] * int(orbital[0])  # Caution! Minus sign assigned here!
        # p suborbitals
        p_suborbital_info = orbital[1].split(",")
        for col in range(0, 3):
            y_up += pdos_up[row][col + 1] * int(p_suborbital_info[col])
            y_down -= pdos_down[row][col + 1] * int(p_suborbital_info[col])
        # d suborbitals
        d_suborbital_info = orbital[2].split(",")
        for col in range(0, 5):
            y_up += pdos_up[row][col + 4] * int(d_suborbital_info[col])
            y_down -= pdos_down[row][col + 4] * int(d_suborbital_info[col])
        # f suborbitals
        if f_included:  # if f suborbitals are present
            f_suborbital_info = orbital[3].split(",")
            for col in range(0, 7):
                y_up += pdos_up[row][col + 9] * int(f_suborbital_info[col])
                y_down -= pdos_down[row][col + 9] * int(f_suborbital_info[col])

        y_up_list.append("%.4f" % y_up)
        y_down_list.append("%.4f" % y_down)

    curve_data = (y_up_list, y_down_list)
    return curve_data  # [y_up, y_down]


def output_pdos_data():  # Generate datasheet for output

    # Count total number of columns in output datasheet
    num_of_columns = 1
    for plot_index in range(1, len(pdosin_curves) + 1):  # plot index starting from "1"
        num_of_columns += len(
            pdosin_curves[plot_index]) * 2 + 1  # separator (for each plot), and up/down for each curve
    pdos_datasheet = [[0.0] * num_of_columns for row in range(nedos)]  # generate an empty sheet

    # Add x-coordinates into the first column
    for row in range(nedos):
        x_coord = float(dos_data[0][0][row][0]) - float(pdosin_settings["e_fermi"])
        pdos_datasheet[row][0] = ("%.4f" % x_coord)  # keep 4 digits after decimal

    # Add y-coordinates to datasheet for each curve
    col_count = 1  # positioning column while appending data
    for plot_index in range(1, len(pdosin_curves) + 1):  # work by each plot
        # add plot_index to datasheet
        for row in range(nedos):
            pdos_datasheet[row][col_count] = f"plot_{plot_index}"
        col_count += 1  # add one: plot_index column

        # add data for each curve
        for curve_index in pdosin_curves[plot_index]:  # curve index starts from "1"
            # prepare data
            curve_atom_select = pdosin_curves[plot_index][curve_index]["atom"]  # atom selection info
            atom_index = translate_atomset(curve_atom_select, atom_list)  # translate selected atoms into atom index list
            curve_orbital = pdosin_curves[plot_index][curve_index]["orbital"]  # orbital selection info
            curve_data = prepare_curve_data(dos_data, nedos, atom_index, curve_orbital)  # curve_data = [y_up, y_down]

            # add data to datasheet[nedos]
            for row in range(nedos):
                pdos_datasheet[row][col_count] = curve_data[0][row]  # spin up
                pdos_datasheet[row][col_count + 1] = curve_data[1][row]  # spin down
            col_count += 2  # add one: up and down columns

    # Output data into "PDOS.dat" file
    with open("PDOS.dat", mode="w", encoding="utf-8") as outputf:
        # Add title to the output file (first row)
        pdos_file_title = "E-Efermi  "
        for plot_index in range(1, len(pdosin_curves) + 1):
            pdos_file_title += f"plot_{plot_index}  "
            num_of_curve = len(pdosin_curves[plot_index])

            if pdosin_settings["spin"].lower() == "both":
                pdos_file_title += "up      down    " * num_of_curve
            elif pdosin_settings["spin"].lower() == "up":
                pdos_file_title += "up      " * num_of_curve
            elif pdosin_settings["spin"].lower() == "down":
                pdos_file_title += "down    " * num_of_curve
        pdos_file_title += "\n"
        outputf.write(pdos_file_title)

        # Choose columns to output according to spin info in PDOSIN
        column_to_output = [0, ]  # collect the columns to output
        plot_col = 1  # help locate where the "plot_N" column lies (start of data block for each plot)

        for plot in range(1, len(pdosin_curves) + 1):  # add "plot" columns
            column_to_output.append(plot_col)  # plot_N column
            # add PDOS data columns
            for curve in range(1, len(pdosin_curves[plot]) + 1):
                if pdosin_settings["spin"] == "up":
                    column_to_output.append(plot_col + (2 * curve - 1))
                elif pdosin_settings["spin"] == "down":
                    column_to_output.append(plot_col + 2 * curve)
                else:  # both
                    column_to_output.extend([plot_col + (2 * curve - 1), plot_col + 2 * curve])
            plot_col += len(pdosin_curves[plot]) * 2 + 1

        # Write datasheet into output file
        for line in pdos_datasheet:  # convert float to string
            line = [str(line[i]) for i in column_to_output]
            outputf.write("  ".join(line) + "\n")  # space between each


# Main Loop
if __name__ == "__main__":
    # Start indicator
    print("PDOS data possessing initialized.\nReading vasprun.xml and PDOSIN......")

    # Read "vasprun.xml" and "PDOSIN"
    dos_data, atom_list, nedos, ispin = read_vasprun()
    pdosin_settings, pdosin_curves = read_pdosin()
    # remove empty plot
    for plot_index in list(pdosin_curves.keys()):
        if len(pdosin_curves[plot_index]) == 0:
            pdosin_curves.pop(plot_index)

    # Output PDOS data
    output_pdos_data()
    print("\033[32mDone! Datasheet exported as \"PDOS.dat\".\033[0m")
