<p align = "center">
    <img src = "GitHub visuals./background_pic_github.jpeg" alt = "Two people boxing">
</p>

<h1 align = "center"> Analyzing punches with EMG and IMU sensors </h1>

# About the project
Combat sports have a rich history dating back thousands of years, with roots in ancient civilizations. Initially combat sports were developed for self-defense and military training but have since evolved into many
different sports and subbranches that focus on physical fitness, mental discipline and philosophical teachings. Throughout the 20th century, martial arts became much more popular. Millions of people worldwide participate in some form of combat sport today. One aspect that many of these combat sports share is the fact that they use a form of punching. Force plates hold the gold standard for measuring force in different aspects. However, there are limitations in using force plates, including things such as high cost and bulkier in use. We hope to show that by using EMG and IMU sensors we can attain similar information as if using force plates for measuring power of a punch and with good accuracy. The analysis is expected to help beginner athletes track their improvements and make adjustments to their techniques in order to improve the efficiency of their punch. By combining data collected from the muscle activity and the motion tracking, we gathered measurements on the speed of punches and the activation of a muscle. The data w

## Collecting the data
The code is adjusted to be used together with acceleration data from MoveSence and EMG data collected with biosignalsplux sensors and the OpenSignals app. 
The acceleration data comes in json format and it could therefore be possible to use our pipeline if the IMU used provide data in json. 
The original EMG data came as a array with three columns, first with the index, then a column with zeros, and third with the muscle activation. 

Python version 3.12.5 is used when runnign the code. 

## Functions

- Generate visual graphs of muscle activation and acceleration
- Diffirent filters that can be applied on graphs
- Supports json-format for acceleration data


## Installation
```bash
git clone https://github.com/ellaVillfor/Project-course-CM2024
cd Project-course-CM2024
pip install -r requirements.txt
```

### Contribution
We are open to contributions! If you want to contribute, please follow these steps:

1. Fork respitory
2. Create a new branch with your changes
3. Send in pull request

### License
This project is licenced under the MIT-licence. See [LICENSE](LICENSE) for more information.
