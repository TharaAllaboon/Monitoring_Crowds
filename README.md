# Monitoring Crowds and Avoiding Stampeded at Hajj Pilgrimage

This project has been created as part of my university senior project requirements.
*Academic Advisor: Dr. Souhila Nada*

# Table of contents:

- [Problem Statment](## Problem Statment)
- [Project Scope](## Project Scope)
	- [Fact Finding Technique] (###Fact Finding Technique)
- [Proposed System](##Proposed System)
	- [Crowd Monitoring System UI] (###Corwd Monitoring System Interface (Prototype))
- [Implementation](##Implementation)
	- [System Results](###System Results)
- [Conculsion](##Conculsion)
- [References](##References)
	- [Appendix](###Appendix)


## Problem Statment
Managing the crowds in big venues and events has been an issue many decades for organizers and officials.
Crowds gathering in one place or events such as sporting even or religious like at Hajj pilgrimage gathering, can create crushes and stampedes, whether triggered by natural disaster or misguided crowd managers.

## Project Scope
In this project, machine learning technology will be implemented by developing a software system that uses the computer vision technique to understand and monitor the live footage of the crowds in the Hajj pilgrimage gathering, providing the best possible solution when a stampede happen.
The main purpose of this project is to help securing the Hajj sites and ease the rituals for all pilgrims

### Fact Finding Technique
After doing the research, the study discovered that using a crowd vision system for Hajj Pilgrimage is better than the current methods used in Hajj recently. Therefore, problems happening with the current methods such as unregistered pilgrims, able to run only in a single environment (The Holy Mosque) and the flaw in the planning in management of clearing areas may overflow the crowd stampede. However, computer vision can help in securing the Hajj when monitoring the crowds, saving time of years of planning and being to react immediately when a stampede happens.
<img src="/Images/fishbone-diagram.jpg" alt="Corwds Monitoring Fishbone Diagram" width="400" height="600">

## Proposed System
Based on the research, and the conclusion of adopting vision based solution, the system can be split into 3 phases:
* Crowd density and dynamics analysis from video streams
* Estimation of threshold value for normalization
* Gate security system for crowd flow regulation

<img src="/Images/crowd-monitoring-arch" alt="Corwds Monitoring System" width="400" height="600">

The proposed system will consist of the following component:
1.	Closed Circuit Television (CCTV) Cameras
2.	Server
3.	Monitors that processed the footage feed
4.	Smartphone application (Android)

### Corwd Monitoring System Interface (Prototype)
The below is a prototype of the interface of the Crowd Monitoring software system:
<img src="/Images/crowd-monitoring-ui.png"alt="Corwds Monitoring UI"width="400" height="600">

## Implementation
The Monitoring Crowd System is implemented using Python 2.7 
In addition, multiple packages and libraries has been used such as OpenCV and NumPy as detailed below:
* [Numpy]: https://numpy.org/
* [OpenCV]: https://opencv.org/
* [Optical Flow]: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html
* [The Lucas-Kanade Algorithm]: https://en.wikipedia.org/wiki/Lucas%E2%80%93Kanade_method

### System Results
Here’s a screenshot of a video at Mina, Makkah where a stampede is happening before running the system:
<img src="/Images/result1.png" alt="Systme 1st Result" width="400" height="600">

Following are the results when applying the parameters of the (image) criteria:
The system is detecting people with a red arrow above each person in the scene.
<img src="/Images/result2.png" alt="Systme 2nd result"width="400" height="600">

The system then will split the video into four parts to better understand the video and crowd flow density, indicating a stampede is happening when one fourth of a video pop up on the left side of the window:
<img src="/Images/result3.png" alt="System 3rd Result" width="400" height="600">

## Conculsion
The stampede at Mina, Hajj is a recent example of a terrible crowd disaster where, in spite of all precautions, many people died during a mass event. Pedestrian dynamics have been studied intensively for more than four decades. 
Multiple researches have been conducting in studying the computer vision for detection and tracking pedestrian in the crowded scenes.
In conclusion, the demonstration proves the concept of monitoring crowds using computer vision technique which allow to track people using the optical flow and to detect if there’s a stampeding situation happening. An effective proven results is shown of the algorithm implemented on different stampede scenarios.

## References
1. Incidents during Hajj https://en.wikipedia.org/wiki/Incidents_during_the_Hajj
2. 2015 Mina Stampede https://en.wikipedia.org/wiki/2015_Mina_stampede
3. Sharley Kulkarni, PG Student, Dept. of E&TC,  and S. K. Shah HOD PG, STES's Smt. Kashibai Navale College of Engineering, Pune, Maharashtra, India,  Monitoring and Safety of Pilgrims Using Stampede Detection and Pilgrim Tracking, International Journal of Advanced Research in Electrical, Electronics and Instrumentation Engineering, 2015.
4. Almoaid A. Owaidah, Thesis, Hajj Crowd Management via a Mobile Augmented Reality Application: A case of The Hajj event, Saudi Arabia, University of Glasgow 2014. 
5. Mantoro T, Hajj Locator: A Hajj pilgrimage tracking framework in crowded ubiquitous environment, Multimedia Computing and Systems (ICMCS), 2011 International Conference, April 2011. 

### Apendix
* Fishbone Diagram https://realtimeboard.com 
* Crowd Monitoring System UI (Prototype) https://www.sketch.com/

