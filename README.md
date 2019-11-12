# SUMO-Unity3D-connection
This exapmle demonstrates real-time communication between the microscopic traffic simulator SUMO and the 3D game engine Unity 3D with Python 3.7 based TCP server. 

The project can be executed standalone. In the Executables folder start Main.exe, which stats the TCP server and SUMO. Then, start Unity_Sumo_Python_Demo.exe to start the Unity game. 

# SUMO 
A simple rectangular traffic network is constructed with 4 junctions, 4 links and 5 vehicles. 
Note: SUMO shall be installed to C:\Sumo or its path shall be modified in the Python source. 

# Python
Python establishes the communication between SUMO and Unity 3D. Python communicates with SUMO using the TRACI interface. It reads the states of vehicles within the traffic simulation and stores them as objects. The Python code also creates a TCP server (IP: localhost, Port: 4042) to communicate with Unity 3D. Vehicle states from SUMO are periodically transmitted to Unity 3D.

# Unity 3D
Unity 3D is responsible for visualisation. The received TCP messages are split into vehicle information. It serves as the base of the motion. Unity's task is positioning and rotating the vehicles, and creating animation for the wheels. The Unity project contains the virtual environment, scripts, and some packages to expand your project. 
Note: while running your project (in the editor or application), the TCP client stops just after the TCP server stops. That means, you may stop the server first.

# Software versions
SUMO 1.2
Python 3.7
Unity 2018.3.5f1

# References
If you have found the codes useful in your work, please, cite one of our papers in your publication, i.e.

Tettamanti T, Szalai M, Vass S and Tihanyi V (2018), "Vehicle-In-the-Loop Test Environment for Autonomous Driving with Microscopic Traffic Simulation", In 2018 IEEE International Conference on Vehicular Electronics and Safety (ICVES). Madrid, Spain, Sept, 2018. , pp. 1-6. 
URL: https://ieeexplore.ieee.org/document/8519486

Horváth MT, Lu Q, Tettamanti T, Török Á and Szalay Zs (2019), "Vehicle-In-The-Loop (VIL) and Scenario-In-The-Loop (SCIL) Automotive Simulation Concepts from the Perspectives of Traffic Simulation and Traffic Control", Transport and Telecommunication Journal. Vol. 2(20), pp. 153-161. 
URL: https://content.sciendo.com/view/journals/ttj/20/2/article-p153.xml
