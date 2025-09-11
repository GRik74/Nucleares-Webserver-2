import requests



def get_vars():
    varFile = "Reactor/variables.txt"
    vars = []
    commands = []
    lines = []
    found_commands = False

    with open(varFile, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line[0] != " " and line != "\n":
            if found_commands:
                commands.append(line.strip("\n"))
            else:
                vars.append(line.strip("\n"))
        elif line.strip(" ")[0] == "#":
            print("Found commands")
            found_commands = True

    translations = {
        "CORE_STATE": {
            "NOREACTIVO": "NOT_REACTIVE",
            "REACTIVO": "REACTIVE"
        },
        "CORE_STATE_CRITICALITY": {
            "SUBCRITICO": "SUBCRITICAL",
            "CRITICO": "CRITICAL"
        },
        "COOLANT_CORE_STATE": {
            "INMOVIL": "IMMOBILE",
            "CIRCULANDO": "CIRCULATING"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_0_STATUS": {
            "0": "NOT_ACTIVE",
            "1": "ACTIVE_AND_NOT_REACHED_SET_VELOCITY",
            "2": "ACTIVE_AND_REACHED_SET_VELOCITY",
            "3": "ACTIVE_AND_REQUIRES_MAINTENANCE",
            "4": "INACTIVE_OR_NOT_OPERATIONAL",
            "5": "ACTIVATION_REQUESTED_BUT_INSUFFICIENT_POWER"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_1_STATUS": {
            "0": "NOT_ACTIVE",
            "1": "ACTIVE_AND_NOT_REACHED_SET_VELOCITY",
            "2": "ACTIVE_AND_REACHED_SET_VELOCITY",
            "3": "ACTIVE_AND_REQUIRES_MAINTENANCE",
            "4": "INACTIVE_OR_NOT_OPERATIONAL",
            "5": "ACTIVATION_REQUESTED_BUT_INSUFFICIENT_POWER"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_2_STATUS": {
            "0": "NOT_ACTIVE",
            "1": "ACTIVE_AND_NOT_REACHED_SET_VELOCITY",
            "2": "ACTIVE_AND_REACHED_SET_VELOCITY",
            "3": "ACTIVE_AND_REQUIRES_MAINTENANCE",
            "4": "INACTIVE_OR_NOT_OPERATIONAL",
            "5": "ACTIVATION_REQUESTED_BUT_INSUFFICIENT_POWER"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_0_DRY_STATUS": {
            "1": "ACTIVE_AND_DRY",
            "4": "INACTIVE_OR_NOT_OPERATIONAL_OR_MAINTENANCE_REQUIRED"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_1_DRY_STATUS": {
            "1": "ACTIVE_AND_DRY",
            "4": "INACTIVE_OR_NOT_OPERATIONAL_OR_MAINTENANCE_REQUIRED"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_2_DRY_STATUS": {
            "1": "ACTIVE_AND_DRY",
            "4": "INACTIVE_OR_NOT_OPERATIONAL_OR_MAINTENANCE_REQUIRED"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_0_OVERLOAD_STATUS": {
            "1": "ACTIVE_AND_OVERLOADED",
            "4": "INACTIVE_OR_NOT_OPERATIONAL_OR_MAINTENANCE_REQUIRED"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_1_OVERLOAD_STATUS": {
            "1": "ACTIVE_AND_OVERLOADED",
            "4": "INACTIVE_OR_NOT_OPERATIONAL_OR_MAINTENANCE_REQUIRED"
        },
        "COOLANT_CORE_CIRCULATION_PUMP_2_OVERLOAD_STATUS": {
            "1": "ACTIVE_AND_OVERLOADED",
            "4": "INACTIVE_OR_NOT_OPERATIONAL_OR_MAINTENANCE_REQUIRED"
        },
        "RODS_STATUS": {
            "INMOVIL": "IMMOBILE",
            "AJUSTANDO": "ADJUSTING"
        }
    }

    return vars, translations, commands


def read_variable(url, variable):
    try:
        response = requests.get(url, params={'variable': variable})
        if response.status_code == 200:
            return response.text
        else:
            return f"Error - Server responded with status code {response.status_code}"
    except requests.RequestException as e:
        return f"Request Error - {e}"

def translate_variable(var, result, translations):
    if var in translations.keys():
        try:
            return translations[var][result]
        except KeyError as e:
            # print(f"Error translating variable: {var} with value: {result}")
            return result
    else:
        return result