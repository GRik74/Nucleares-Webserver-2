import read_variables
from fnmatch import fnmatch

portnum = 8785
url = f"http://localhost:{portnum}/"


class Reactor:
    '''Object representing the reactor as a whole.'''
    def __init__(self):
        self.varList, self.translations, self.commands = read_variables.get_vars()
        self.data = {}
        self.update_vars()

        self.time = ''
        self.timeStamp = ''
        self.day = 0
        self.core = Core()

        self.Loop1 = CoolantLoop(1)

        self.maxPotentialPower = 0
        self.externalReservoir = 0


    def update_vars(self):
        '''Update all variables'''
        for var in self.varList:
            holder = read_variables.read_variable(url, var)
            if not fnmatch(holder, "*Error*"):
                self.data[var] = read_variables.translate_variable(var, holder)
            else:
                self.data[var] = holder

        data = self.data
        try:
            self.time = data['TIME']
            self.timeStamp = data['TIME_STAMP']
            self.day = data['TIME_DAY']

            self.core.State = data['CORE_STATE']
            self.core.Wear = float(data['CORE_WEAR'])
            self.core.Integrity = float(data['CORE_INTEGRITY'])

        except TypeError as e:
            print(f"Error updating {e.args[0]} - incorrect type.")
        except KeyError as e:
            print(f"Error updating {e.args[0]} - doesn't exist in reactor data.")
        


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
        self.chem = {'DoseOrd': 0, 'DoseAct': 0, 'FiltOrd': 0, 'FiltAct': 0, 'BoronPPM': 0}

    def update(self, data):
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
        self.ImminentFusion = data['CORE_IMMINENT_FUSION']
        self.ReadyStart = True if data['CORE_READY_FOR_START'] == 'TRUE' else False
        self.SteamPresent = True if data['CORE_STEAM_PRESENT'] == 'TRUE' else False
        self.HighSteam = True if data['CORE_HIGH_STEAM_PRESENT'] == 'TRUE' else False



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


class CoreCoolant:
    '''Object representing the coolant in the core of the reactor. Part of Core object.'''
    def __init__(self):
        self.state = ''
        self.pressCurrent = 0
        self.pressMax = 0
        self.temp = 0
        self.overallQuantity = 0
        self.primaryLoopLevel = 0
        self.flowSpeed = 0
        self.flowIn = 0
        self.flowOut = 0
        self.orderedSpeed = 0
        self.speedReached = False
        self.feedwaterTankLevel = 0


class SteamTurbine:
    def __init__(self, loopNum):
        self.loopNum
        self.rpm = 0
        self.temp = 0
        self.pressure = 0


class ElectricTurbine:
    def __init__(self, loopNum):
        self.loopNum = 0
        self.power = 0
        self.voltage = 0
        self.amps = 0
        self.freq = 0
        self.breaker = False


class CoolantLoop:

    def __init__(self, loopNum):
        self.loopNum = loopNum
        self.primPump = CircPump(loopNum)
        self.secPumpCapacity = 0
        self.steamGen = Evaporator(loopNum)

        self.steamTurbine = SteamTurbine(loopNum)
        self.elecTurbine = ElectricTurbine(loopNum)


class CircPump:

    def __init__(self, loopNum):
        self.loopNum = loopNum
        self.Status = ''
        self.Dry = False
        self.Overload = False
        self.OrderedSpeed = 0
        self.ActualSpeed = 0
        self.Capacity = 0

class Evaporator:
    def __init__(self, loopNum):
        self.loopNum = loopNum
        self.ReturnFlowPlusCondensed = 0










""" CORE_TEMP
CORE_TEMP_OPERATIVE
CORE_TEMP_MAX
CORE_TEMP_MIN
CORE_TEMP_RESIDUAL
CORE_PRESSURE
CORE_PRESSURE_MAX
CORE_PRESSURE_OPERATIVE
CORE_INTEGRITY
CORE_WEAR
CORE_STATE
CORE_STATE_CRITICALITY
CORE_CRITICAL_MASS_REACHED
CORE_CRITICAL_MASS_REACHED_COUNTER
CORE_IMMINENT_FUSION
CORE_READY_FOR_START
CORE_STEAM_PRESENT
CORE_HIGH_STEAM_PRESENT

TIME
TIME_STAMP
TIME_DAY

COOLANT_CORE_STATE
COOLANT_CORE_PRESSURE
COOLANT_CORE_MAX_PRESSURE
COOLANT_CORE_VESSEL_TEMPERATURE
COOLANT_CORE_QUANTITY_IN_VESSEL
COOLANT_CORE_PRIMARY_LOOP_LEVEL
COOLANT_CORE_FLOW_SPEED
COOLANT_CORE_FLOW_ORDERED_SPEED
COOLANT_CORE_FLOW_REACHED_SPEED
COOLANT_CORE_QUANTITY_CIRCULATION_PUMPS_PRESENT
COOLANT_CORE_QUANTITY_FREIGHT_PUMPS_PRESENT

COOLANT_CORE_CIRCULATION_PUMP_0_STATUS
COOLANT_CORE_CIRCULATION_PUMP_1_STATUS
COOLANT_CORE_CIRCULATION_PUMP_2_STATUS
    0: Inactive
    1: Active, no speed reached
    2: Active, speed reached
    3: Requires maintenance
    4: Not installed
    5: Insufficient energy

COOLANT_CORE_CIRCULATION_PUMP_0_DRY_STATUS
COOLANT_CORE_CIRCULATION_PUMP_1_DRY_STATUS
COOLANT_CORE_CIRCULATION_PUMP_2_DRY_STATUS
    1: Active without fluid
    4: Inactive or active with fluid

COOLANT_CORE_CIRCULATION_PUMP_0_OVERLOAD_STATUS
COOLANT_CORE_CIRCULATION_PUMP_1_OVERLOAD_STATUS
COOLANT_CORE_CIRCULATION_PUMP_2_OVERLOAD_STATUS
    1: Active and overload
    4: Inactive or active no overload

COOLANT_CORE_CIRCULATION_PUMP_0_ORDERED_SPEED
COOLANT_CORE_CIRCULATION_PUMP_1_ORDERED_SPEED
COOLANT_CORE_CIRCULATION_PUMP_2_ORDERED_SPEED

COOLANT_CORE_CIRCULATION_PUMP_0_SPEED
COOLANT_CORE_CIRCULATION_PUMP_1_SPEED
COOLANT_CORE_CIRCULATION_PUMP_2_SPEED

RODS_STATUS
RODS_MOVEMENT_SPEED
RODS_MOVEMENT_SPEED_DECREASED_HIGH_TEMPERATURE
RODS_DEFORMED
RODS_TEMPERATURE
RODS_MAX_TEMPERATURE
RODS_POS_ORDERED
RODS_POS_ACTUAL
RODS_POS_REACHED
RODS_QUANTITY
RODS_ALIGNED

GENERATOR_0_KW
GENERATOR_1_KW
GENERATOR_2_KW

GENERATOR_0_V
GENERATOR_1_V
GENERATOR_2_V

GENERATOR_0_A
GENERATOR_1_A
GENERATOR_2_A

GENERATOR_0_HERTZ
GENERATOR_1_HERTZ
GENERATOR_2_HERTZ

GENERATOR_0_BREAKER
GENERATOR_1_BREAKER
GENERATOR_2_BREAKER
    TRUE: Open
    FALSE: Close

STEAM_TURBINE_0_RPM
STEAM_TURBINE_1_RPM
STEAM_TURBINE_2_RPM

STEAM_TURBINE_0_TEMPERATURE
STEAM_TURBINE_1_TEMPERATURE
STEAM_TURBINE_2_TEMPERATURE

STEAM_TURBINE_0_PRESSURE
STEAM_TURBINE_1_PRESSURE
STEAM_TURBINE_2_PRESSURE

CORE_POOL_COOLANT_TANK_VOLUME
CORE_PRIMARY_CIRCUIT_COOLING_TANK_VOLUME
CORE_EXTERNAL_COOLANT_RESERVOIR_VOLUME
CORE_FACTOR_CHANGE
    (reactivity change)

COOLANT_CORE_FLOW_IN
COOLANT_CORE_FLOW_OUT
COOLANT_CORE_CIRCULATION_PUMP_0_CAPACITY
COOLANT_CORE_CIRCULATION_PUMP_1_CAPACITY
COOLANT_CORE_CIRCULATION_PUMP_2_CAPACITY
COOLANT_SEC_CIRCULATION_PUMP_0_CAPACITY
COOLANT_SEC_CIRCULATION_PUMP_1_CAPACITY
COOLANT_SEC_CIRCULATION_PUMP_2_CAPACITY

CHEM_BORON_DOSAGE_ORDERED
CHEM_BORON_DOSAGE_ACTUAL
CHEM_BORON_FILTER_ORDERED
CHEM_BORON_FILTER_ACTUAL
CHEM_BORON_DOSAGE_ORDERED_RATE
CHEM_BORON_FILTER_ORDERED_SPEED
CHEM_BORON_PPM

STEAM_GEN_0_RETURN_FLOW_PLUS_CONDENSED
STEAM_GEN_1_RETURN_FLOW_PLUS_CONDENSED
STEAM_GEN_2_RETURN_FLOW_PLUS_CONDENSED

POWER_MAX_THEORETICAL_FINAL_PLANT_OUTPUT_MW """