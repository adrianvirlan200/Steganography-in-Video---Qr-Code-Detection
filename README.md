# Steganography in Video & Qr Code Detection
# Part 1 
1. Video Recording:
Record a 3-second video using your webcam.

2. Text Extraction from Image:
Extract text from "image.png" using Python-tesseract and save it in a .txt file.

3. Text Embedding in Video Frames:
Divide the extracted text into pieces and embed each piece into a distinct frame of a 10-frame sequence chosen from the video. Examples of frame sequences include (5, 10, 15, ...), (2, 4, 6, 8, ...), (4, 8, 9, 10, 14, 27, 33, 57, 64, 72).

4. Video Codec Selection:
Choose an appropriate codec for saving the video.

5. Encode.py File:
Create an "encode.py" file containing the code for the first three steps.

6. Decode.py File:
Write a "decode.py" file with the code necessary for decoding the message from the video. The decoded message should be printed on the screen.

# Part 2
1. ArUco Marker Detection:
Detect an ArUco marker from the frames captured by your webcam (assuming there is only one marker in the image).

2. Image Overlay on Marker:
If the detected marker's ID is 2, overlay "image2.png" on the detected marker. An example is shown in "exemplu_partea2.jpg".

3. Saving the Video Sequence:
Save a sequence of up to 10 seconds showing the detection and replacement of the marker with the image in a video file, using MPEG-4 codec.

4. Aruco.py File:
Write the necessary code in an "aruco.py" file.
 
