import pandas as pd
from helpers import *

#Instructions
#----------------------------------------
#Go into 'Helpers' and paste in the dictionary values for the capacity drivers, country capacity drivers, milestone dates and country milestone dates.
#You can find this data in any RP log. You will then have a full set of input variables for a sample workpackage.
#Next, set the rolename below for the role you want to test. You config file should be name similarly ie. {ROLENAME]-config.csv
#provide the path below to the location of your config file
#give the name of the complexity variable you wish to use in your algorithm.

rolename = 'CRA'
config_path = 'C:\\Users\\hamriia2\\OneDrive - Novartis Pharma AG\\repos\\rp-config-scripts\\config_tester\\configs\\'
complex_var = 'GMO-complexity'

#print("derived vals : " + str(derived_values))
#DO NOT EDIT ANY OF THE CODE BELOW
#-----------------------------------------------------------------------------------------------




# Check for null values
def isNaN(num):
    return num != num

# Get the Complexity value
capdrvCPX = get_capacity_driver(complex_var)

def GetCPX(cpxin):
    return cpxin[0:1]


def GetCPXCol(inval):
    options = {1: 'CPX_1',
               2: 'CPX_2',
               3: 'CPX_3',
               4: 'CPX_4',
               5: 'CPX_5',
               6: 'CPX_6'}
    return options[inval]

intCPX = int(GetCPX(capdrvCPX))
CPXColName = GetCPXCol(intCPX)

#read in the config file
config = pd.read_csv(config_path+rolename+"-config.csv")
config.columns.values[12] = 'CPX_1'
config.columns.values[13] = 'CPX_2'
config.columns.values[14] = 'CPX_3'
config.columns.values[15] = 'CPX_4'
config.columns.values[16] = 'CPX_5'
config.columns.values[17] = 'CPX_6'


print("Capacity Drivers")
print("----------------")

for key, value in capacity_drivers.items():
    print(key+": "+str(value) )

print("")
print("Derivations")
print("-----------")
#derived_values={}
errflg = False
for row in config.itertuples(index=True, name='Pandas'):
    # Check the derivations first
    try:
        if not isNaN(getattr(row, "derivation_calculation")):
            dname = getattr(row, "wp_element_id")
            x = getattr(row, "derivation_calculation")
            result = eval(x)
            if result == None:
                result = 'None'
            print(dname+":"+str(result))
            #add each derived name value pair to a dictionary for further reference
            derived_values[dname]=result
            #print(str(derived_values))

    except Exception as err:
        print("Error detected in derivations!")
        print("Cell value : " + x)
        print("Error: " + str(err))
        print("Result: " + str(result))
        errflg = True
        print(str(derived_values))

if not errflg: print("Derivations all good")

print("")
print("Start dates")
print("-----------")
errflg = False
for row in config.itertuples(index=True, name='Pandas'):
    # Now check the dates - start
    try:
        if not isNaN(getattr(row, "start_work")):
            dname = getattr(row, "wp_element_id")
            x = getattr(row, "start_work")
            result = eval(x)
            print(dname+": {:%d-%b-%y}".format(result))

    except Exception as err:
        print("Error detected in start dates!")
        print("Cell value : " + x)
        print("Error: " + str(err))
        errflg = True

if not errflg: print("Start dates all good")

print("")
print("End dates")
print("-----------")
errflg = False
for row in config.itertuples(index=True, name='Pandas'):
    # Now check the dates -end
    try:
        if not isNaN(getattr(row, "end_work")):
            dname = getattr(row, "wp_element_id")
            x = getattr(row, "end_work")
            result = eval(x)
            print(dname + ": {:%d-%b-%y}".format(result))
    except Exception as err:
        print("Error detected in end dates!")
        print("Cell value : " + x)
        print("Error: " + str(err))
        errflg = True

if not errflg: print("End dates all good")

print("")
print("Restriction clauses")
print("-----------")
errflg = False
for row in config.itertuples(index=True, name='Pandas'):
    # Restriction clauses
    try:
        if not isNaN(getattr(row, "restriction_clause")):
            dname = getattr(row, "wp_element_id")
            x = getattr(row, "restriction_clause")
            result = eval(x)
            print(dname + ": " + str(result))
    except Exception as err:
        print("Error detected!")
        print("Cell value : " + x)
        print("Error: " + str(err))
        errflg = True

if not errflg: print("Restriction clauses all good")

print("")
print("Demand effort")
print("-----------")
errflg = False
totdemand=0
for row in config.itertuples(index=True, name='Pandas'):
    # Demand effort
    complexity = getattr(row, CPXColName)
    try:
        if not isNaN(getattr(row, "demand_effort_calculation")):
            dname = getattr(row, "wp_element_id")
            x = getattr(row, "demand_effort_calculation")
            result = eval(x)
            totdemand +=result
            print(dname + ": " + str(result))
    except Exception as err:
        print("Error detected!")
        print("Cell value : " + x)
        print("Error: " + str(err))
        errflg = True

if not errflg: print("Demand effort calculations all good. Total demand = "+str(round(totdemand,2))+" working days ("+str(round(totdemand/250,2))+" FTEs)")
