# Grid_arena
A bot which can teleop and can go to the user input cordinates

## Installation
### In order to use this package, go through the following steps:

Open you catkin package and go to the src
```bash
cd catkin_ws/src
```
After that clone the repo to your src
```bash
git clone https://github.com/misramrinal/grid_arena.git
```
After cloning, source and build the package
```bash
source devel/setup.bash
catkin build
```
## Launching
### In order to launch the package, first launch the gazebo simulation
```bash
roslaunch grid_arena arena_1.launch
```
After doing so, if you want to tele-operate the bot from keyboard, run the following script
```bash
rosrun grid_arena teleop_latest.py
```
This will allow you control the bot using W,A,S,D keys

However if you want to move the bot to a specific user input cordinate, run the following script
```bash
rosrun grid_arena camera.py
```
Enter the X and Y cordinates of the point you want to go to and see the magic!
