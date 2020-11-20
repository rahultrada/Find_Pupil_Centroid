# find_pupil_centroid

This repo consists of work done as part of the TeleMedC pupil (and its centroid) detection algorithm challenge. 

Below are a list of files in this repo and their purposes:
1. pupil_detection.pdf - A written explanation of my approach to solving the challenge, including image processing steps etc.
2. pupil_detection.py - The pupil (and its centroid) detection algorithm
3. sample.mkv - The video file used to develop, and to run, the algorithm

# Instructions to run the algorithm
1. Clone this repository
2. Create a python3 venv
3. Activate the venv
4. Install package dependencies, namely 'opencv-python'
5. Execute the script: 'python3 pupil_detection.py'. This will run the algorithm on the sample.mkv video file provided with this repo and output the result on a video frame. The controls of the frame are as follows: press key 'p' to pause and resume the frame, and while the frames are running, press key 'q' to quit. If you don't quit manually, the frame will close itself automatically at the end of the video. Also note that there is an overlay in the top left of the video displaying the current frame number, and the fps i.e. the fps for the computation between each frame. 





