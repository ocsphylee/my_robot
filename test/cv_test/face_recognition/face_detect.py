# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/13 16:07
Descriptions:
'''

import picamera
from picamera.array import PiRGBArray
import face_recognition
import cv2
import numpy as np
import os


def load_sample(path):
    known_face_encodings = []
    known_face_names = []
    img_paths = [os.path.join(path, f) for f in os.listdir(path)]
    for img in img_paths:
        sample_img = face_recognition.load_image_file(img)
        sample_encoding = face_recognition.face_encodings(sample_img)[0]
        names = os.path.split(img)[-1].split(".")[0]

        known_face_encodings.append(sample_encoding)
        known_face_names.append(names)
    return known_face_encodings, known_face_names

sample_path = 'known_people'

known_face_encodings, known_face_names = load_sample(sample_path)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = 1

resol = (320, 240)
camera = picamera.PiCamera()
camera.resolution = resol
camera.framerate = 20
raw_capture = PiRGBArray(camera, size= resol)
skrink = 0.5
emph = 2

for frame in camera.capture_continuous(
        raw_capture, format="bgr", use_video_port=True):

    # 获取图片
    frame_image = frame.array

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame_image, (0, 0), fx=skrink, fy=skrink)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame == 1:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    # check every 5 frames
    process_this_frame += 1
    if process_this_frame > 5:
        process_this_frame = 1

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= emph
        right *= emph
        bottom *= emph
        left *= emph

        # Draw a box around the face
        cv2.rectangle(frame_image, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame_image)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    raw_capture.truncate(0)
