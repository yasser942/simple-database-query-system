#2019510006 YASSER EL HASSAN
#2020510130 RINAT ZHULFAYEV
#2020510108 ASLAN TUYAK
import json
from operator import contains

operators = ["!=", "<=", ">=", "!<", "!>", "=", "<", ">"]
temp_dict1 = {}
temp_dict2 = {}
final_dict = {}

#Select the operator and perform operation
def selectOP(cond_1, sorted_by_key, op, temp_dict):
    if (op == "="):
        # If parameters are alphabetic
        if (cond_1[0].strip().isalpha() and (cond_1[1].strip().isalpha() or contains(cond_1[1].strip(), "@"))):
            for k in sorted_by_key:
                if (sorted_by_key[k][cond_1[0].strip()] == cond_1[1].strip()):
                    ke = sorted_by_key[k]
                    temp_dict.update({k: ke})
        # If parameters are numeric
        else:
            for k in sorted_by_key:
                if (int(sorted_by_key[k][cond_1[0].strip()]) == int(cond_1[1])):
                    ke = sorted_by_key[k]
                    temp_dict.update({k: ke})
    elif (op == "!="):
        # If parameters are alphabetic
        if (cond_1[0].strip().isalpha() and (cond_1[1].strip().isalpha() or contains(cond_1[1].strip(), "@"))):
            for k in sorted_by_key:
                if (sorted_by_key[k][cond_1[0].strip()] != cond_1[1].strip()):
                    ke = sorted_by_key[k]
                    temp_dict.update({k: ke})
        # If parameters are numeric
        else:
            for k in sorted_by_key:
                if (int(sorted_by_key[k][cond_1[0].strip()]) != int(cond_1[1])):
                    ke = sorted_by_key[k]
                    temp_dict.update({k: ke})
    elif (op == "<" or op == "!>"):
        for k in sorted_by_key:
            if (int(sorted_by_key[k][cond_1[0].strip()]) < int(cond_1[1])):
                ke = sorted_by_key[k]
                temp_dict.update({k: ke})
    elif (op == ">" or op == "!<"):
        for k in sorted_by_key:
            if (int(sorted_by_key[k][cond_1[0].strip()]) > int(cond_1[1])):
                ke = sorted_by_key[k]
                temp_dict.update({k: ke})
    elif (op == "<="):
        for k in sorted_by_key:
            if (int(sorted_by_key[k][cond_1[0].strip()]) <= int(cond_1[1])):
                ke = sorted_by_key[k]
                temp_dict.update({k: ke})
    elif (op == ">="):
        for k in sorted_by_key:
            if int(sorted_by_key[k][cond_1[0].strip()]) >= int(cond_1[1]):
                ke = sorted_by_key[k]
                temp_dict.update({k: ke})

#Sort and print by ASC or DSC order
def sort(dict, promt, select_command):
    if promt == "ASC":
        final_dict = {k: v for k, v in sorted(dict.items())}
    elif promt == "DSC":
        final_dict = {k: v for k, v in sorted(dict.items(), reverse=True)}
    else:
        print("Invalid command")

    if(len(final_dict) == 0):
        print("Not found")
    else:
        for key in final_dict:
            key_count =0;
            value = final_dict[key]
            for i in select_command:
                if(len(select_command)==1):
                    print(key + ": " + value[i.strip()])
                elif key_count == 0:
                    print(key + ": " + value[i.strip()], end=" ")
                    key_count = key_count + 1
                elif(i == select_command[-1]):
                    print(value[i.strip()])
                else:
                    print(value[i.strip()], end=" ")
    return final_dict

def main():
    #Read CSV file and store values in dictionary
    data = {}
    with open("students.csv", "r") as f:
        next(f)
        for row in f:
            line = row.strip("\n").split(";")
            data[line[0]] = {"id": line[0], "name": line[1], "lastname": line[2], "email": line[3], "grade": line[4]}

    exit = False
    #Sort dictionary by index(id)
    sorted_by_key = {k: v for k, v in sorted(data.items())}
    #Start of the main loop
    while (not exit):
        #User query input
        user_command = input("Enter a query: \n")
        user_command = user_command.replace("’", "").replace("‘", "").replace("'", "")
        ################################################################
        #Insert Query implementation
        if user_command.startswith("INSERT INTO STUDENTS VALUES(") and user_command.endswith(")"):
            values = user_command[user_command.find("(") + 1:len(user_command) - 1]
            values = values.split(",")
            #Control the number of the values and their types
            if len(values) != 5 or not (values[0].isnumeric() and (values[1].isalpha()) and (values[2].isalpha()) and values[4].isnumeric()):
                print("Invalid input ,Please enter all attributes !")
            else:
                #Insert value to the dictionary and sort it
                sorted_by_key.update({values[0]: {"id": values[0], "name": values[1], "lastname": values[2], "email": values[3], "grade": values[4]}})
                sorted_by_key = {k: v for k, v in sorted(sorted_by_key.items())}

                print("Insertion was completed!")
        ################################################################
        # Select Query implementation
        elif (user_command.startswith("SELECT") and contains(user_command, "FROM STUDENTS WHERE") and (
                contains(user_command, "ORDER BY ASC") or contains(user_command, "ORDER BY DSC"))):

            select_command = user_command[user_command.find("T") + 2:user_command.find("F") - 1]
            #Query validation
            if (not select_command == "ALL" and not select_command.islower()) or len(select_command) == 0 or contains(select_command, " "):
                print("Wrong attributes")
            else:
                if select_command == "ALL":
                    select_command = ["name", "lastname", "email", "grade"]
                else:
                    select_command = select_command.split(",")
                conditions = user_command[user_command.find("WHERE") + 6:]
                order = conditions[len(conditions) - 3:]

                if any(c in operators for c in conditions):
                    # Control query with condition1 AND condition2
                    if conditions.count("AND") == 1:
                        cond_1 = conditions[0:conditions.index("AND") - 1]
                        cond_2 = conditions[conditions.index("AND") + 3:conditions.index("ORDER") - 1]
                        #Define used operator
                        for c in operators:
                            if contains(cond_1, c):
                                cond_1 = cond_1.split(c)
                                op = c
                            if contains(cond_2, c):
                                cond_2 = cond_2.split(c)
                                op2 = c
                        #Perform the operation depending on the operator
                        selectOP(cond_1, sorted_by_key, op, temp_dict1)
                        selectOP(cond_2, sorted_by_key, op2, temp_dict2)
                        #Dictionary that holds the result of a current query
                        final_dict = {x: temp_dict1[x] for x in temp_dict1 if x in temp_dict2}
                        #Sort and print the output of the query according to the given order
                        sorted_by_key = sort(final_dict, order, select_command)

                    ################################################################
                    # Control query with  condition1 OR condition2
                    elif conditions.count("OR") == 2: #Equals 2 because of "OR" in ORDER
                        cond_1 = conditions[0:conditions.index("OR") - 1]
                        cond_2 = conditions[conditions.index("OR") + 2:conditions.index("ORDER") - 1]

                        for c in operators:
                            if contains(cond_1, c):
                                cond_1 = cond_1.split(c)
                                op = c
                            if contains(cond_2, c):
                                cond_2 = cond_2.split(c)
                                op2 = c

                        selectOP(cond_1, sorted_by_key, op, temp_dict1)
                        selectOP(cond_2, sorted_by_key, op2, temp_dict1)
                        sorted_by_key = sort(temp_dict1, order, select_command)

                    ################################################################
                    elif conditions.count(" and ") == 1 or conditions.count(" or ") == 1:
                        print("AND, OR keywords must be capital!")

                    # Control query with one condition
                    elif conditions.count("AND") == 0 or conditions.count("OR") == 1:
                        cond_1 = conditions[0:conditions.index("ORDER") - 1]
                        op = ""
                        for c in operators:
                            if contains(cond_1, c):
                                cond_1 = cond_1.split(c)
                                op = c

                        selectOP(cond_1, sorted_by_key, op, temp_dict1)
                        sorted_by_key = sort(temp_dict1, order, select_command)

                    else:
                        print("Error!! you can only use one condition.")

        # Delete Query implementation
        elif (user_command.startswith("DELETE FROM STUDENTS WHERE")):
            conditions = user_command[user_command.find("WHERE") + 6:]

            if any(c in operators for c in conditions):
                # Delete operation in case that the query has 2 conditions with AND operator
                if conditions.count("AND") == 1:
                    cond_1 = conditions[0:conditions.index("AND") - 1].strip()
                    cond_2 = conditions[conditions.index("AND") + 3:].strip()
                    for c in operators:
                        if contains(cond_1, c):
                            cond_1 = cond_1.split(c)
                            op = c
                        if contains(cond_2, c):
                            cond_2 = cond_2.split(c)
                            op2 = c

                    selectOP(cond_1, sorted_by_key, op, temp_dict1)
                    selectOP(cond_2, sorted_by_key, op2, temp_dict2)
                    final_dict = {x: temp_dict1[x] for x in temp_dict1 if x in temp_dict2}
                    # Delete the items from main dictionary according to the query
                    for k in final_dict:
                        sorted_by_key.pop(k, None)

                    print("Successfully deleted!")
                ################################################################
                # Delete operation in case that the query has 2 conditions with OR operator
                elif conditions.count("OR") == 1:
                    cond_1 = conditions[0:conditions.index("OR") - 1]
                    cond_2 = conditions[conditions.index("OR") + 2:]

                    for c in operators:
                        if contains(cond_1, c):
                            cond_1 = cond_1.split(c)
                            op = c
                        if contains(cond_2, c):
                            cond_2 = cond_2.split(c)
                            op2 = c

                    selectOP(cond_1, sorted_by_key, op, temp_dict1)
                    selectOP(cond_2, sorted_by_key, op2, temp_dict1)
                    for k in temp_dict1:
                        sorted_by_key.pop(k, None)

                    print("Successfully deleted!")
                ################################################################
                # Delete operation in case that the query has 1 condition
                elif conditions.count("AND") == 0 or conditions.count("OR") == 0:
                    cond_1 = conditions[0:]
                    op = ""
                    for c in operators:
                        if contains(cond_1, c):
                            cond_1 = cond_1.split(c)
                            op = c

                    selectOP(cond_1, sorted_by_key, op, temp_dict1)

                    for k in temp_dict1:
                        sorted_by_key.pop(k, None)

                    print("Successfully deleted!")
        ################################################################
        elif (user_command.startswith("EXIT")):
            exit = True
        else:
            print("Please enter a valid query !")

    #Create a JSON file of the final data
    json_dict = {"students": [sorted_by_key]}
    with open("file.json", "w") as f:
        json.dump(json_dict, f, indent=5)
    print("Your data has been stored in json file.")


main()
