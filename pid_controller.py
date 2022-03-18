def give_rpm(error):
    return proportional(error, 1) + derivative(error, 1) + integral(error, 1)

def proportional(error, faktor):
    return faktor * error

def derivative(error, faktor):
    return 0

def integral(error, faktor):
    return 0