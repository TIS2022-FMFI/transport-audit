allow_synchronize = True

sync_URL = "https://wrp-audit.gefcoslovakia.sk" #bez koncoveho lomitka

api_password = "94bd18c7-91a4-4f79-b45a-7a59105631f4" # musi byt rovnake aj na strane servera

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

