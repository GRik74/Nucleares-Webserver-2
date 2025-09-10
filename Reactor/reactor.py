# import read_variables


class Reactor:

    def __init__(self):
        self.time = ''
        self.timeStamp = ''
        self.day = 0
        self.core = Core()

        self.Loop1 = CoolantLoop(1)


class Core:

    def __init__(self):
        self.TempCurrent = 0
        self.TempOperative = 0
        self.TempMax = 0

        self.PressCurrent = 0
        self.PressOperative = 0
        self.PressMax = 0

        self.State = ''
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
        self.MaxPotentialPower = 0
        self.ExternalReservoir = 0


class Rods:
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