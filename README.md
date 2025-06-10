# gesture-recognition-mouse
A Python-based gesture recognizing mouse with additional volume control features, all controlled by simple hand gestures.

This project stemmed from a tutorial video by Murtaza's Workshop. I used the video as a foundation to set up the initial hand tracking module and then went on to self-implement a number of features, including mouse movement by tracking the position of the index finger landmark, a click activated by the thumb and index finger tips coming together, a volume up activated by the thumb and middle finger coming together, and a volume down activated by the thumb and ringer finger coming together.

Key libraries used:
OpenCV - Webcam video capture to record the hand
MediaPipe - Identifies and tracks hand and gestures by assigning different trackable landmarks
PyAutoGUI - Used to control the cursor and click the mouse
PyCaw - Used to control volume
