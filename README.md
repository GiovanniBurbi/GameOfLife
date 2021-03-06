# Game Of Life
> Conway's Game of Life implementation using convolution. Based on PyQt5.

## Overview
The [Game of Life](http://ddi.cs.uni-potsdam.de/HyFISCH/Produzieren/lis_projekt/proj_gamelife/ConwayScientificAmerican.htm)
was invented in 1970 by the British mathematician **John Horton Conway**. Conway
developed an interest in a problem which was made evident in the 1940’s by mathematician John von
Neumann, who aimed to find a hypothetical machine that had the ability to create copies of itself and
was successful when he discovered a mathematical model for such a machine with very complicated
rules on a rectangular grid. Thus, the Game of Life was Conway’s way of simplifying von Neumann’s
ideas. It is the best-known example of a **cellular automaton** which is any system in which rules are
applied to cells and their neighbors in a regular grid. Martin Gardner popularized the Game of Life
by writing two articles for his column “Mathematical Games” in the journal Scientific American in
1970 and 1971. In this programming assignment has been implemented the Game of Life, along with a
complete and polished Graphical User Interface to control the simulation.

## Rules of the Game
The game is played on a two-dimensional grid (or **board**). Each grid location is either empty or
populated by a single cell. A location’s neighbors are any cells in the surrounding eight adjacent
locations. The simulation of starts from an initial state of populated locations and then progresses
through time. The evolution of the board state is governed by a few simple rules:
1. Each populated location with one or zero neighbors dies (from **loneliness**).
2. Each populated location with four or more neighbors dies (from **overpopulation**).
3. Each populated location with two or three neighbors **survives**.
4. Each unpopulated location that **becomes populated** if it has exactly three populated neighbors.
5. All updates are performed simultaneously in **parallel**.

This figure illustrates the rules for cell **death**, **survival**, and **birth**:
![](https://github.com/GiovanniBurbi/GameOfLife/blob/master/media/images/GameOfLifeRules.png)

# Getting started

## Requirements
The application has been **build** and **tested** with:
* **python** 3.8
* **PyQt5** 5.9.2
* **scipy** 1.7.1
* **numpy** 1.21.2
* **qimage2ndarray** 1.8.3

## Run the Application
* Clone this repository
* Navigate inside the root directory of the project
* Install all the dependencies:
  * with Anaconda: `conda install requirements.txt`
  * with Pip: `pip install -r requirements.txt`
  * Use your IDE, it should automatically detect the *requirements.txt* file
* Run the application:
  * From command line: `python3 AppLauncher.py`
  * From IDE: Run *AppLauncher.py* using your IDE running command

## Features
* **Start/pause/clear**: The GUI supports controls that allow the user to **start** and **pause** the
simulation, and **clear** the current state of the board.
* **Variable framerate**: The GUI supports a control that allows the user to **select the framerate** at which the simulation is run and animated.
* **Drawing/editing of state**: The GUI allows the user to **draw and edit** the state of the board (i.e. fill in or empty oyt occupied locations) with the mouse. **Left click** allows drawing alive cells, **Right click** allows delete filled cells. 
This feature is available to the user **whenever the simulation is paused or running**, allowing the user to edit the current state in realtime.
* **Loading of initial state**: The GUI provides some **classic examples** of Game of Life Patterns that the user can play with. In addition to this, the GUI supports the **loading** of a serialized version of the board
state. After the loading of the file you can find the **new pattern** listed in the combo box list.
The **file format** accepted is [RLE](https://www.conwaylife.com/wiki/Run_Length_Encoded). You can find many patterns in RLE format [here](https://www.conwaylife.com/wiki/Main_Page). **Maximum size** pattern allowed is 64x128.
It's also possible to put RLE files in the **'model/patterns' folder** of this project to find the respective patterns in the combo box at the starting of the application.
* **Zooming and panning of board**: The GUI allows the user to select the grid size (zoom) and which part of the grid is currently viewed (panning). **Holding down** the **scroll button** allows the panning of the board according to the movements of the mouse.
* **Cell history**: The GUI keeps track of **how long each cell has been alive** from the activation of the history mode. It's shown visually by changing the color from **light blue** (newborn) to **dark blue** (ancient).

## Gallery

![](https://github.com/GiovanniBurbi/GameOfLife/blob/master/media/images/Pulsar.png)
![](https://github.com/GiovanniBurbi/GameOfLife/blob/master/media/images/space-rake.png)
![](https://github.com/GiovanniBurbi/GameOfLife/blob/master/media/images/gosper-glider-gun.png)
