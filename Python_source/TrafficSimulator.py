# ======================================================
# Copyright (C) 2019 BME Automated Drive Lab
# This program and the accompanying materials
# are made available under the terms of the MIT license.
# ======================================================
# Author: Balazs Varga 
# Date: 2019. 11. 10.
# ======================================================

import traci
import os
import sys
import SUMO_vehicle
import TrafficLight

class TrafficSimulator(object):
    def __init__(self, NetworkName):

        self.NetworkName = NetworkName
        self.StartSumo()
        self.ParseNetwork()

    def StartSumo(self):
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        sumoBinary = "C:/Sumo/bin/sumo-gui"  # "C:/Sumo/bin/sumo-gui"
        FolderPath = "../SUMO_Networks/"
        sumoCmd = [sumoBinary, "-c",
                   FolderPath + self.NetworkName, "--start"]
        traci.start(sumoCmd)

        print("Sumo is running")

    def ParseNetwork(self):
        # Get edge IDs
        self.Edges = traci.lane.getIDList()

        # Get edge shapes
        self.LinkShapes = []
        for e in self.Edges:
            self.LinkShapes.append(traci.lane.getShape(e))

    def RestartSumo(self, SumoObjects):

        #Restart the program
        self.StartSumo()
        self.ParseNetwork()

        #Put objects back into the simulator
        for Obj in SumoObjects:
            Obj.ReinsertVehicle()

    def StepSumo(self, SumoObjects, TrafficLights):

        try:
            traci.simulationStep()  # step simulatior
        except:
            print("Restarting SUMO")
            self.RestartSumo(SumoObjects)

        SumoObjectsRaw0 = traci.vehicle.getIDList()  # get every vehicle ID
        SumoObjectNames = list(set(SumoObjectsRaw0))  # Make it unique


        # Remove SUMO objects from the list if they left the network
        for Obj in SumoObjects:
            if(not(any(ObjName == Obj.ID for ObjName in SumoObjectNames))):
                SumoObjects.remove(Obj)

        #Append new objects and update existing ones.
        for VehID in SumoObjectNames:
            if(not(any(Obj.ID == VehID for Obj in SumoObjects))):
                NewlyArrived = SUMO_vehicle.SumoObject(VehID)
                SumoObjects.append(NewlyArrived)

        #Update Sumo vehicle objects
        for Obj in SumoObjects:
            Obj.UpdateVehicle()

        #Update traffic signal phases
        TrafficLights = self.UpdateSignalPhases(TrafficLights)

        return SumoObjects, TrafficLights

    def ParseTrafficLights(self):

        TrafficLights = []

        # Get traffic lights
        self.LightIDs = traci.trafficlight.getIDList()

        #Loop through all signalized intersections
        for ID in self.LightIDs:
            LightLaneList = traci.trafficlight.getControlledLanes(ID)

            #Loop through all signal head at the intersection
            idx = 0
            for Lane in LightLaneList:
                Pos = traci.lane.getShape(Lane)

                LightPositionX = Pos[len(Pos) - 1][0]
                LightPositionY = Pos[len(Pos) - 1][1]

                #Create the traffic light object in the simulator
                TrafficLightObject = TrafficLight(ID, Lane, idx, LightPositionX, LightPositionY)
                TrafficLights.append(TrafficLightObject)

                idx = idx + 1

        return TrafficLights

    def UpdateSignalPhases(self, TrafficLights):

        i = 0
        #Loop through every signalized intersection
        for ID in self.LightIDs:
            LightPhases = traci.trafficlight.getRedYellowGreenState(ID) #string

            #Loopt through the string containing the state of each signal controller and update the traffic light objects.
            for State in LightPhases:
                TrafficLights[i].DecodeTrafficPhase(State)
                i = i+1

        return TrafficLights
