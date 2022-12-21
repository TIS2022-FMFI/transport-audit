allow_synchronize = True

sync_URL = "http://server.nahovno.eu:5100"

api_password = "YouWontGuessThisOne"

def re_write_bool(variable,value):
    with open("config.py", 'r') as file:
        new_file = []
        for line in file:

            if variable in line:
                new_file.append(line.split(variable)[0] + f"{variable} = " + value + ""+ "\n")
            else:
                new_file.append(line)
        with open("config.py", 'w') as file:
            for line in new_file:
                file.writelines(line)

def re_write_string(variable,value):
    with open("config.py", 'r') as file:
        new_file = []
        for line in file:
            if variable in line:
                new_file.append(line.split(variable)[0] + f"{variable} = '" + value + "'"+ "\n")
            else:
                new_file.append(line)
        with open("config.py", 'w') as file:
            for line in new_file:
                file.writelines(line)
