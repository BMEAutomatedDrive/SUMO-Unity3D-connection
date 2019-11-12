# ======================================================
# Copyright (C) 2019 BME Automated Drive Lab
# This program and the accompanying materials
# are made available under the terms of the MIT license.
# ======================================================
# Author: Balazs Varga 
# Date: 2019. 11. 10.
# ======================================================

import time
from queue import Queue
import TrafficSimulator
import TCP_server
import Unity

class SumoUnity(object):
    def __init__(self, IP, Port, SumoNetwork):

        self.NetworkName = SumoNetwork

        # Define queues for communication
        self.UnityQueue = Queue(maxsize=1)

        #Launch SUMO
        self.TrafficSim = TrafficSimulator.TrafficSimulator(self.NetworkName)
        self.TrafficLights = self.TrafficSim.ParseTrafficLights()
        self.SumoObjects = []

        #Start TCP server
        self.ServerIP = IP
        self.ServerPort = Port

        self.Server = TCP_server.TCP_Server(self.ServerIP, self.ServerPort)
        self.Server.StartServer(self.UnityQueue)

    def main(self):

        deltaT = 0.02

        while True:

            #Get timestamp
            TiStamp1 = time.time()

            #Monitor TCP connection
            self.Server.ReopenSocket(self.UnityQueue)

            #Update SUMO
            self.SumoObjects, self.TrafficLights = self.TrafficSim.StepSumo(self.SumoObjects, self.TrafficLights)


            #Update Unity
            Unity.ToUnity(self.SumoObjects, self.TrafficLights, self.UnityQueue)

            #Synchronize time
            TiStamp2 = time.time() - TiStamp1
            if TiStamp2 > deltaT:
                pass
            else:
                time.sleep(deltaT-TiStamp2)


IP = 'localhost'
port = 4042
SumoNetwork = "Rectangle/Network_01.sumocfg"  # Name of the network to be opened

#INIT
Simulation = SumoUnity(IP, port, SumoNetwork)
#MAIN
Simulation.main()