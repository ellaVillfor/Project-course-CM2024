![Two people boxing](./background_pic_github.jpeg)

# Analyzing punches with EMG and IMU sensors
The code is adjusted to be used together with acceleration data from MoveSence and EMG data collected with biosignalsplux sensors and the OpenSignals app. 
The acceleration data comes in json format and it could therefore be possible to use our pipeline if the IMU used provide data in json. 
The original EMG data came as a array with three columns, first with the index, then a column with zeros, and third with the muscle activation. 

Python version 3.12.5 is used when runnign the code. 


## Installation
```bash
git https://github.com/ellaVillfor/Project-course-CM2024
cd Project-course-CM2024
pip install -r requirements.txt
```
    