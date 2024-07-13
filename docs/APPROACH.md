### Problem statement
Given a video return a json file with labels associated with each timestamp frame.

---------

1. **Feature Matching**: This method involves extracting key features from both the reference image (LOGO) and other images (FRAMES) using algorithms like:


- SIFT (Scale-Invariant Feature Transform)
- SURF (Speeded Up Robust Features)
- ORB (Oriented FAST and Rotated BRIEF)

The algorithm then matches these features to find similarities. This technique is useful for identifying objects despite changes in scale, orientation, or illumination.

2. **Template Matching**: In this technique, the reference image is used as a template, and it is slid over another image to check for matches. The similarity is measured based on how well the pixels of the reference image align with the pixels in the target images. OpenCV, a popular computer vision library, provides functions like cv2.matchTemplate() for this purpose.


3. **Object Detection Models**: Convolutional Neural Networks (CNNs)/ Transformer based models can be trained to recognize specific objects, including logos, within images. Once trained, these models can be used to scan new images for the presence of the reference object. This method is particularly effective due to its ability to learn high-level features of the reference image.
