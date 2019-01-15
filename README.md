# Webots Motion Files to Nao Converter
## Introduction
While working in a project for the NAO Robot from Softbank Robotics I realized that webots is no longer supporting controllers directly compatible with the NaoQI SDK.
This means that if you are working with webots for each simulation aspect and you decide that you want to run the same in the real robot, you can't.
Webots uses motion file to store movement sequences. The motion file contains snapshots of all the joints and angles of the robot in a specific moment. All of the these snapshots construct a movement as frames construct a video

## Prepare
The python script uses python2.7. In order for the naoqi SDK to be recognised the PYTHON_PATH needs to be adjusted. You can put this in your ```.bashrc``` file.

		PYTHON_PATH=${PYTHON_PATH}:/path/to/naoqi/sdk

> You can download the sdk from the Aldebaran website (for now)

## Run

		python2.7 motion_converter.py --motionfile motions/Shoot.motion

## Arguments explanation
By running ```python2.7 motion_converter.py --help``` you are getting a small help page
1. --ip, corresponds to the ip of the robot or the naoqi sdk (if running in virtual)
2. --port, corresponds to the port of the robot or the naoqi sdk (if running in virtual)
3. --motionfile, path to motion file to run
4. --webotstimetype, if true converter will try to read the snapshot time as 00:00:000, if false it will read it as seconds, e.g 1.2, 3.5
