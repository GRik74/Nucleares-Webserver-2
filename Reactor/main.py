from reactor import *
import time
# from tkinter import *

react = Reactor()

""" root = Tk()
root.geometry('450x900')
label = Label(root, text="Reactor Data\n\n\n")
StartButton = Button(root, text="Start", command=display)
PauseButton = Button(root, text="Pause", command=pause_display)
# UpdateButton = Button(root, text="Update", command=update)

TimeLabel = Label(root)
CoreLabel = Label(root)
CoreCoolantLabel = Label(root)
Pump0Label = Label(root)
Pump1Label = Label(root)
Pump2Label = Label(root)
RodsLabel = Label(CoreLabel)

label.pack()
StartButton.pack()
PauseButton.pack()
# UpdateButton.pack()

TimeLabel.pack()
CoreLabel.pack()
CoreCoolantLabel.pack()
Pump0Label.pack()
Pump1Label.pack()
Pump2Label.pack()
RodsLabel.pack() """




if __name__ == "__main__":
    statsActive = True

    while statsActive:
        react.update_vars()
        print("\n"*40)

        print("--------------------- Reactor Status -------------------------")

        # Basic Stats

        print(f"Time:                                {react.time}")
        print(f"Day:                                 {react.day}" + '\n')

        print(f"Core Reactivity Change:              {round(float(react.core.CoreDelta), 2)}" + '\n')

        # print(f"Primary Circulation Pumps Active:    {react.numPrimaryPumps}")
        # print(f"Freight Pumps Installed:             {react.numFreightPumps}")
        # print(f"External Reservoir Level:            {react.externalReservoir}")

        print("\n")
        print("---------------------  Reactor Core  -------------------------")
        print(f"Core State:                          {react.core.State}")

        if float(react.core.Integrity) < 99.5:
            print(f"Core Integrity:                      {round(float(react.core.Integrity), 1)}")

        if float(react.core.Wear) < 99.0:
            print(f"Core Wear:                           {round(float(react.core.Wear), 1)}")
        
        if react.core.State == 'REACTIVE':
            if react.core.ImminentFusion:
                print(f"********  CORE FUSION IMMINENT  ********")
            if react.core.HighSteam or react.core.SteamPresent:
                print("********* STEAM PRESENT IN CORE *********")

        if react.core.State == "REACTIVE" or float(react.core.coreCoolant.flowSpeed) > 100.0:
            print('\n')
            print(f"Core Temp:                           {round(float(react.core.TempCurrent), 1)}")
            print(f"Core Operative Temp Diff:            {round(float(react.core.TempCurrent) - float(react.core.TempOperative), 1)}" + "\n")
            
            print(f"Core Pressure:                       {round(float(react.core.PressCurrent))}")
            print(f"Core Operative Pressure Diff:        {round(float(react.core.PressCurrent) - float(react.core.PressOperative), 1)}")

        
        print('\n')
        print("---------------------  Reactor Rods  -------------------------")

        if react.core.rods.deformed:
            print("************* CONTROL RODS DEFORMED *************")
        if react.core.rods.speedDecreased:
            print("******** CONTROL RODS IMPAIRED MOVEMENT *********")

        print('\n')
        if react.core.rods.status != "" and react.core.rods.status != " ": print(f"Rods Status:                         {react.core.rods.status}")
        print(f"Rod Count:                           {react.core.rods.rodCount}")
        if react.core.rods.tempCurrent != "" and react.core.rods.tempCurrent != " ": print(f"Rods Temp:                           {react.core.rods.tempCurrent}")
        # print(f"Rods Max Temp Diff:                  {round(float(react.core.rods.tempCurrent) - float(react.core.rods.tempMax), 2)}")


        print('\n')
        print("---------------------  Reactor Coolant  ----------------------")

        print(f"Coolant State:                       {react.core.coreCoolant.state}")
        print(f"Coolant Temp:                        {round(float(react.core.coreCoolant.temp), 2)}")
        print(f"Coolant Pressure:                    {round(float(react.core.coreCoolant.pressCurrent))}" + '\n')

        # print(f"Vessel Level:                        {round(float(react.core.coreCoolant.vesselLevel), 0)}")
        if float(react.core.coreCoolant.primaryLoopLevel) < 99.0: print(f"Primary Loop Level:                  {round(float(react.core.coreCoolant.primaryLoopLevel))}" + '\n')
        
        print(f"Coolant Flow Speed:                  {round(float(react.core.coreCoolant.flowSpeed), 0)}")
        if float(react.core.coreCoolant.flowIn) != float(react.core.coreCoolant.flowOut):
            print(f"     ************ WARNING *************\n\n***** Core In-Flow <> Out-Flow Differential *****")
            print(f"\tCoolant In-Flow:                     {round(float(react.core.coreCoolant.flowIn), 0)}")
            print(f"\tCoolant Out-Flow                     {round(float(react.core.coreCoolant.flowOut), 0)}")


        print('\n')
        print("---------------------  Generator Status  ----------------------")


        time.sleep(5)
        





""" def activateDisplay():
    react.update_vars()

    TimeLabel.config(text=react.time) """


