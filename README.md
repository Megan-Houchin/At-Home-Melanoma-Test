# At Home Melanoma Assessment

This project intended to allow the user to upload a photo of an area of skin and then have the program use K-Nearest Neighbor Classification to determine whether it would likely have melanoma or not. This program tests for two of the five variables used to identify signs of melanoma: asymmetry and the number of colors contained in the area of skin. 

## Instructions

In the main.py file, the user can easily run the code:

Please note: the code in main is already all written out so the user can just run the code as is to get all of information; however, if he or she wants to only print some of the code, the explanation of how to do that is displayed below.

Accuracy of K-Nearest Neighbor:

1. To see how accurate the K-Nearest Neighbor Classification is for the data provided, one can call the colors_info and get_asym_info functions in ff by inputting 20 and "bad" and "good" respectively so the function knows which files to get the images from. 

2. Since the asymmetry values are already range from 0-1, this array does not need to be normalized; however, colors do. This can be done by calling the normalize function in ff. 

3. Then, the arrays created must be put into the correct format in order to be plotted. This can be done by calling ff.createMasterArr, which takes the arrays of data for each classification and returns arrays containing 80% of the known information and the other 20% in separate arrays. This is done so that 20% of the known data can be tested using K-Nearest Neighbor and is therefore treated as unknowns. Every time this is run, the 20% of the data is randomly picked.

4. Plot the data using ff.graphData. The number of values compared is currently set to 3, but can be changed so long as the number is an odd and positive integer (no ties).

5. Finally, two arrays of 0s and 1s (different classifications) are created (total lengths = 20% of original data) and are sent to ff.compare to print the accuracy of the trial. 

Classification of an Unknown:

1. First, place an image (as a jpg) in the Unknown_stuff folder. There is already one there if the user does not want to upload there own.

2. Change the name of the image to 'U1.jpg' (again, this is already done).

3. If you have not done steps 1 and 2 from the previous instructions, please do them now. Call ff.createRegArr to use the known data from the Malignant file and the Healthy file to establish known points on the plot. 

4. Use colors_info and get_asym_info functions to get the values of the unknown (send 1 and 'unknown' as arguments to each function).

5. Normalize the unknown image color value (ff.normalize).

6. Finally, plot the results using ff.graphUnknown.

Printing an Example of the Color Segmentation Process and Asymmetry Determination Process:

1. Simply call either ff.color_example and/or ff.asym_example, and the code will print the visual results of the felzenszwalb color segmentation function from the skimage library (as well as the number of colors in that particular image) and the code will print a visual representation of the masking of the image during the asymmetry process (as well as the numerical asymmetry assignment). These functions only require the path as a string of a particular image. 
 
Note: To change example printed either change the number and letter (M = maligant file (20 options), H = healthy file (20 options) and U = unknown file (1 option)). 

## File List

main.py: driver of the code

final_functions.py: where all of the functions are stored

Maligant_stuff: where the 20 images of melanoma skin are stored

Healthy_stuff: where the 20 images of the healthy skin images are stored

Unknown_stuff: where the 1 unknown diagnoses image is stored

