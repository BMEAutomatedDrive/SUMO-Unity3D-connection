# ======================================================
# Copyright (C) 2019 BME Automated Drive Lab
# This program and the accompanying materials
# are made available under the terms of the MIT license.
# ======================================================
# Author: Balazs Varga 
# Date: 2019. 11. 10.
# ======================================================

import traci

class TrafficLight(object):

    #Class attribute
    PhaseDict = {
        "o": 0,  # off
        "O": 0,  # off
        "g": 1,  # green
        "G": 1,  # green
        "y": 2,  # yellow
        "Y": 2,  # yellow
        "r": 3,  # red
        "R": 3,  # red
    }

    def __init__(self, ID, Lane, idx, LightPositionX, LightPositionY):

        self.ID = ID
        self.LaneID = Lane
        self.Index = idx
        self.PosX = LightPositionX
        self.PosY = LightPositionY
        #Get the Lon, Lat positions of each signal head.
        self.__TransformGPS()

        self.CurrentPhase = 0

    #Transforms SUMO X-Y coordinate system to GPS
    def __TransformGPS(self):
        self.Lon, self.Lat = traci.simulation.convertGeo(self.PosX, self.PosY)

    def DecodeTrafficPhase(self, CurrentPhaseRaw):
        self.CurrentPhase = self.PhaseDict[CurrentPhaseRaw]
