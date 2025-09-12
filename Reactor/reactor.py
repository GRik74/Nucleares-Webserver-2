import read_variables
from fnmatch import fnmatch

portnum = 8785
url = f"http://localhost:{portnum}/"


class Reactor:
    '''Object representing the reactor as a whole.'''
    def __init__(self):
        self.varList, self.translations, self.commands = read_variables.get_vars()
        self.data = {}

        self.time = ''
        self.timeStamp = ''
        self.day = 0
        self.core = Core()

        self.maxPotentialPower = 0
        self.externalReservoir = 0
        self.numPrimaryPumps = 0
        self.numFreightPumps = 0

        self.update_vars()


    def update_vars(self):
        '''Update all variables'''
        for var in self.varList:
            holder = read_variables.read_variable(url, var)
            if not fnmatch(holder, "*Error*"):
                self.data[var] = read_variables.translate_variable(var, holder, self.translations)
            else:
                self.data[var] = holder

        data = self.data
        try:
            self.time = data['TIME']
            self.timeStamp = data['TIME_STAMP']
            self.day = data['TIME_DAY']
            self.externalReservoir = data['CORE_EXTERNAL_COOLANT_RESERVOIR_VOLUME']
            self.numPrimaryPumps = data['COOLANT_CORE_QUANTITY_CIRCULATION_PUMPS_PRESENT']
            self.numFreightPumps = data['COOLANT_CORE_QUANTITY_FREIGHT_PUMPS_PRESENT']
            self.maxPotentialPower = data['POWER_MAX_THEORETICAL_FINAL_PLANT_OUTPUT_MW']

            self.core.update_core(data)
            

        except TypeError as e:
            print(f"Error updating {e.args[0]} - incorrect type. Press enter to continue.")
        except KeyError as e:
            print(f"Error updating {e.args[0]} - doesn't exist in reactor data. Press enter to continue.")



class Core:
    '''Object representing the core of the reactor.'''
    def __init__(self):
        self.TempCurrent = 0
        self.TempOperative = 0
        self.TempMax = 0
        self.TempResidual = 0

        self.PressCurrent = 0
        self.PressOperative = 0
        self.PressMax = 0

        self.State = ''
        self.Integrity = 0.0
        self.Wear = 0.0
        self.Criticality = False
        self.CritMassReached = False
        self.CriticalityCounter = 0
        self.ImminentFusion = False
        self.ReadyStart = False
        self.SteamPresent = False
        self.HighSteam = False
        self.CoreDelta = 0

        self.rods = Rods()
        self.coreCoolant = CoreCoolant()

    
    def update_core(self, data):

        self.TempCurrent = data['CORE_TEMP']
        self.TempOperative = data['CORE_TEMP_OPERATIVE']
        self.TempMax = data['CORE_TEMP_MAX']
        self.TempResidual = data['CORE_TEMP_RESIDUAL']

        self.PressCurrent = data['CORE_PRESSURE']
        self.PressOperative = data['CORE_PRESSURE_OPERATIVE']
        self.PressMax = data['CORE_PRESSURE_MAX']

        self.Integrity = data['CORE_INTEGRITY']
        self.Wear = data['CORE_WEAR']
        self.State = data['CORE_STATE']
        self.ImminentFusion = True if data['CORE_IMMINENT_FUSION'] == 'TRUE' else False
        self.ReadyStart = True if data['CORE_READY_FOR_START'] == 'TRUE' else False
        self.SteamPresent = True if data['CORE_STEAM_PRESENT'] == 'TRUE' else False
        self.HighSteam = True if data['CORE_HIGH_STEAM_PRESENT'] == 'TRUE' else False
        self.CoreDelta = data['CORE_FACTOR_CHANGE']

        self.rods.update_rods(data)
        self.coreCoolant.update_CoreCoolant(data)




class Rods:
    '''Object representing the control rods in the reactor. Part of Core object.'''
    def __init__(self):
        self.status = ''
        self.moveSpeed = 0
        self.speedDecreased = False
        self.deformed = False
        self.tempCurrent = 0
        self.tempMax = 0
        self.orderedPosition = 0
        self.actualPosition = 0
        self.positionReached = False
        self.rodCount = 0
        self.rodsAligned = False

    
    def update_rods(self, data):
        self.status = data['RODS_STATUS']
        self.moveSpeed = data['RODS_MOVEMENT_SPEED']
        self.speedDecreased = True if data['RODS_MOVEMENT_SPEED_DECREASED_HIGH_TEMPERATURE'] == 'TRUE' else False
        self.deformed = True if data['RODS_DEFORMED'] == 'TRUE' else False
        self.tempCurrent = data['RODS_TEMPERATURE']
        self.tempMax = data['RODS_MAX_TEMPERATURE']
        self.orderedPosition = data['RODS_POS_ORDERED']
        self.actualPosition = data['RODS_POS_ACTUAL']
        self.positionReached = True if data['RODS_POS_REACHED'] == 'TRUE' else False
        self.rodCount = data['RODS_QUANTITY']
        self.rodsAligned = data['RODS_ALIGNED']


class CoreCoolant:
    '''Object representing the coolant in the core of the reactor. Part of Core object.'''
    def __init__(self):
        self.state = ''
        self.pressCurrent = 0
        self.pressMax = 0
        self.temp = 0
        self.vesselLevel = 0
        self.primaryLoopLevel = 0
        self.flowSpeed = 0
        self.flowIn = 0
        self.flowOut = 0
        self.orderedSpeed = 0
        self.speedReached = False
        self.feedwaterTankLevel = 0

        self.chem = Chemical()

        self.LoopA = CoolantLoop(0)
        self.LoopB = CoolantLoop(1)
        self.LoopC = CoolantLoop(2)
        self.loops = [self.LoopA, self.LoopB, self.LoopC]

    
    def update_CoreCoolant(self, data):
        self.state = data['COOLANT_CORE_STATE']
        self.pressCurrent = data['COOLANT_CORE_PRESSURE']
        self.pressMax = data['COOLANT_CORE_MAX_PRESSURE']
        self.temp = data['COOLANT_CORE_VESSEL_TEMPERATURE']
        self.vesselLevel = data['COOLANT_CORE_QUANTITY_IN_VESSEL']
        self.primaryLoopLevel = data['COOLANT_CORE_PRIMARY_LOOP_LEVEL']
        self.flowSpeed = data['COOLANT_CORE_FLOW_SPEED']
        self.orderedSpeed = data['COOLANT_CORE_FLOW_ORDERED_SPEED']
        # self.speedReached = True if data['COOLANT_CORE_FLOW_SPEED_REACHED'] == 'TRUE' else False
        self.flowIn = data['COOLANT_CORE_FLOW_IN']
        self.flowOut = data['COOLANT_CORE_FLOW_OUT']
        self.feedwaterTankLevel = data['CORE_PRIMARY_CIRCUIT_COOLING_TANK_VOLUME']

        self.chem.update_Chemical(data)
        
        for loop in self.loops:
            loop.update_CoolantLoop(data)

        
class Chemical:
    def __init__(self):
        self.DoseOrdered = 0
        self.DoseActual = 0
        self.FilterOrdered = 0
        self.FilterActual = 0
        self.DosageOrderedRate = 0
        self.FilterOrderedSpeed = 0
        self.BoronPPM = 0

    def update_Chemical(self, data):
        self.DoseOrdered = data['CHEM_BORON_DOSAGE_ORDERED']
        self.DoseActual = data['CHEM_BORON_DOSAGE_ACTUAL']
        self.FilterOrdered = data['CHEM_BORON_FILTER_ORDERED']
        self.FilterActual = data['CHEM_BORON_FILTER_ACTUAL']
        self.DosageOrderedRate = data['CHEM_BORON_DOSAGE_ORDERED_RATE']
        self.FilterOrderedSpeed = data['CHEM_BORON_FILTER_ORDERED_SPEED']
        self.BoronPPM = data['CHEM_BORON_PPM']



class SteamTurbine:
    def __init__(self, loopNum):
        self.loopNum = loopNum
        self.rpm = 0
        self.temp = 0
        self.pressure = 0

    def update_SteamTurbine(self, data):
        self.rpm = data[f"STEAM_TURBINE_{self.loopNum}_RPM"]
        self.temp = data[f"STEAM_TURBINE_{self.loopNum}_TEMPERATURE"]
        self.pressure = data[f"STEAM_TURBINE_{self.loopNum}_PRESSURE"]


class ElectricTurbine:
    def __init__(self, loopNum):
        self.loopNum = 0

        self.powerMW = 0
        self.powerKW = 0

        self.voltage = 0
        self.amps = 0
        self.freq = 0
        self.breaker = ""

    def update_ElectricTurbine(self, data):
        self.powerKW = data[f"GENERATOR_{self.loopNum}_KW"]
        self.powerMW = self.powerKW/1000
        self.voltage = data[f"GENERATOR_{self.loopNum}_V"]
        self.amps = data[f"GENERATOR_{self.loopNum}_A"]
        self.freq = data[f"GENERATOR_{self.loopNum}_HERTZ"]
        self.breaker = "Closed" if data[f"GENERATOR_{self.loopNum}_BREAKER"] == 'FALSE' else "OPEN"


class CoolantLoop:

    def __init__(self, loopNum):
        self.loopNum = loopNum
        self.PrimaryPump = CircPump(loopNum, True)
        self.SecPump = CircPump(loopNum, False)
        self.ReturnFlow = 0

        self.steamTurbine = SteamTurbine(loopNum)
        self.elecTurbine = ElectricTurbine(loopNum)

    
    def update_CoolantLoop(self, data):
        self.ReturnFlow = data[f"STEAM_GEN_{self.loopNum}_RETURN_FLOW_PLUS_CONDENSED"]

        self.PrimaryPump.update_CircPump(data)
        self.SecPump.update_CircPump(data)
        self.steamTurbine.update_SteamTurbine(data)
        self.elecTurbine.update_ElectricTurbine(data)


class CircPump:

    def __init__(self, loopNum, prim=True):
        self.PrimSec = 'PRIMARY' if prim else 'SECONDARY'
        self.loopNum = loopNum

        if prim:
            self.Status = ''
            self.Dry = False
            self.Overload = False
            self.OrderedSpeed = 0
            self.ActualSpeed = 0
            self.Capacity = 0
        else:
            self.Capacity = 0

    
    def update_CircPump(self, data):
        if self.PrimSec == 'PRIMARY':
            self.Status = data[f"COOLANT_CORE_CIRCULATION_PUMP_{self.loopNum}_STATUS"]
            self.Dry = True if data[f"COOLANT_CORE_CIRCULATION_PUMP_{self.loopNum}_DRY_STATUS"] == "ACTIVE_AND_DRY" else False
            self.Overload = True if data[f"COOLANT_CORE_CIRCULATION_PUMP_{self.loopNum}_OVERLOAD_STATUS"] == "ACTIVE_AND_OVERLOADED" else False
            self.OrderedSpeed = data[f"COOLANT_CORE_CIRCULATION_PUMP_{self.loopNum}_ORDERED_SPEED"]
            self.ActualSpeed = data[f"COOLANT_CORE_CIRCULATION_PUMP_{self.loopNum}_SPEED"]
            self.Capacity = data[f"COOLANT_CORE_CIRCULATION_PUMP_{self.loopNum}_CAPACITY"]
        else:
            self.Capacity = data[f"COOLANT_SEC_CIRCULATION_PUMP_{self.loopNum}_CAPACITY"]

