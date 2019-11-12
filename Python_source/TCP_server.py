# ======================================================
# Copyright (C) 2019 BME Automated Drive Lab
# This program and the accompanying materials
# are made available under the terms of the MIT license.
# ======================================================
# Author: Balazs Varga 
# Date: 2019. 11. 10.
# ======================================================

import socket
import time
import Unity


class TCP_Server(object):
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        self.Num_Listener = 1

        #Create socket object
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSocket.setblocking(True)
        s_adr = (self.IP, self.port)
        self.ServerSocket.bind(s_adr)
        #self.ServerSocket.settimeout(120)

        #Define clients
        self.UnityClient = []
        self.UnityAddress = []
        self.UnityRunning = False
        self.UnityThread = []

        print("Starting TCP server at ",  self.IP, ":", self.port)
    def StartServer(self, UnityQueue):

        self.ServerSocket.listen(self.Num_Listener)

        i = 0
        # Wait for all clients
        while i < self.Num_Listener:
            tmpClient, tmpAddress = self.ServerSocket.accept()
            ClientName = '00000'
            print(ClientName)
            while ClientName is '00000':
                try:
                    ClientName = tmpClient.recv(5)
                    print(ClientName)
                except:
                    time.sleep(0.01)
            # Order clients
            if ClientName == 'U3D00'.encode('utf8'):
                print("Connection from: Unity 3D")
                self.UnityClient = tmpClient
                self.UnityAddress = tmpAddress
                self.UnityRunning = True
                i = i + 1
                time.sleep(1)

                #Start transmit to Unity thread here!
                self.UnityError, self.UnityThread = Unity.StartUnity(self.UnityClient, UnityQueue)

            else:
                tmpClient.close()
                print("ERROR! Check the clients and retry!")
                # sys.exit(1)

    def ReopenSocket(self, UnityQueue):

        if self.UnityError.isSet():

            #Kill the thread if there is an error, clear the error
            self.UnityThread.join()
            self.UnityError.clear()
            self.UnityRunning = False

            #Open for 1 connection and wait for the matching client
            self.ServerSocket.listen(1)
            tmpClient, tmpAddress = self.ServerSocket.accept()
            ClientName = '00000'

            while ClientName is '00000':
                try:
                    ClientName = tmpClient.recv(5)
                    print(ClientName)
                except:
                    time.sleep(0.01)

            if ClientName == 'U3D00'.encode('utf8'):
                print("Connection from: Unity 3D")
                self.UnityClient = tmpClient
                self.UnityAddress = tmpAddress
                time.sleep(1)

                # Start transmit to Unity thread here!
                self.UnityError, self.UnityThread = Unity.StartUnity(self.UnityClient, UnityQueue)
                self.UnityRunning = True
            else:
                #Throw the connection and wait for the right one.
                tmpClient.close()

    def CloseSocket(self):
        self.ServerSocket.close()