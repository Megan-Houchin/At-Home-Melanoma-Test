#Final Project
#*****************************************
# YOUR NAME: Megan Houchin
# NUMBER OF DAYS TO COMPLETE: 6 days

#import statements
from skimage import color
from skimage.segmentation import felzenszwalb
from skimage.segmentation import mark_boundaries
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import math

#functions
def color_info(n, name): 
    #takes the arguments n, the number of images in the file, and the name that indicates whether the file contains malignant photos or not
    #determines which file name should be used and traverses through the folder finding the number of colors in each image
    #returns the array containing the number of colors in each image
    colors = np.empty(n)
    for i in range(n):
        if(name == "bad"):
            c = get_color('Malignant_stuff/M' + str(i+1)+ '.jpg')
            colors[i] = c
        elif(name == "good"):
            c = get_color('Healthy_stuff/H' + str(i+1)+ '.jpg')
            colors[i] = c
        else:
            c = get_color('Unknown_stuff/U' + str(i+1)+ '.jpg')
            colors[i] = c
    return colors

def get_color(s):
    #takes the argument s which is the string name of the image in the file in question
    #determines the number of colors in an image
    #returns the integer of the number of colors
    img = Image.open(s).convert('L') #converts image to grayscale
    pic_array = (np.asarray(img))
    n, bins, patches = plt.hist(pic_array.flatten()) #creates a histogram
    plt.close()
    x_val = bins[5] #masks the values represented in the histogram so that it only focuses on the area without the skin (skin = 0)
    mask = pic_array < x_val #assigns true or false values to every point
    save = mask*pic_array #makes skin = 0
    
    image_felzenszwalb = felzenszwalb(img) 
    image_felzenszwalb_colored = color.label2rgb(image_felzenszwalb, save, kind='avg')
    
    colors = len(np.unique(image_felzenszwalb_colored)) #number of color clusters
    return colors

def color_example(name):
    #takes the variable name which is the string name of the image in the file in question
    #plots an example color clustering using Felzenwalb's method
    #returns None
    img = Image.open(name)
    pic_array = (np.asarray(img))
    
    image_felzenszwalb = felzenszwalb(img)
    image_felzenszwalb_colored = color.label2rgb(image_felzenszwalb, pic_array, kind='avg')
    plt.title('Color Distribution')
    plt.imshow(image_felzenszwalb_colored)
    
    segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
    fig, ax = plt.subplots()
    plt.imshow(mark_boundaries(img, segments_fz))
    plt.title('Marked Borders Color Distribution')
    plt.tight_layout()
    plt.show()
    print(f"Number of colors: {len(np.unique(segments_fz))}")
    
    return None

def get_asym_info(n, name):
    #takes the arguments n, the number of images in the file, and the name that indicates whether the file contains malignant photos or not
    #determines which file name should be used and traverses through the folder finding how symmetrical each image is
    #returns the array containing the float indiacting how symmetrical each image is (0 being completely asymmetrical and 1 being completely symmetrical)
    asym = np.empty(n)
    for i in range(n):
        if(name == "bad"):
            a = get_asym_arr('Malignant_stuff/M' + str(i+1)+ '.jpg')
            asym[i] = a
        elif(name == "good"):
            a = get_asym_arr('Healthy_stuff/H' + str(i+1)+ '.jpg')
            asym[i] = a
        else:
            a = get_asym_arr('Unknown_stuff/U' + str(i+1)+ '.jpg')
            asym[i] = a
    return asym

def get_asym_arr(name):
     #takes the variable name which is the string name of the image in the file in question
     #calculates how asymmetrical each image is 0 is absolutely assymmetrical 1 is totally symmetrical
     #returns an array of the symmetrical value of each image
    img = Image.open(name).convert('L')
    pic_array = (np.asarray(img))
    n, bins, patches = plt.hist(pic_array.flatten())
    plt.close()
    x_val = bins[5]
    mask = pic_array < x_val #assigns true or false values to every point
    save = mask*pic_array
    sym = calculate_correlation(save)
    return sym

def asym_example(name):
    #takes the variable name which is the string name of the image in the file in question
    #prints the image, the histogram original of the color distributuon, the masked image in gray scale, and the new histogram of the masked image data
    #returns None
    img = Image.open(name).convert('L')
    img2 = Image.open(name)
    pic_array = (np.asarray(img))
    plt.title('Original Image')
    plt.imshow(img2)
    plt.show()
    n, bins, patches = plt.hist(pic_array.flatten())
    x_val = bins[5]
    mask = pic_array < x_val 
    save = mask*pic_array
    plt.title('Original Grey Scale Color Distribution')
    plt.xlabel("Color Bins")
    plt.ylabel("Number of Pixels")
    plt.show()
    plt.title('Grey Scale Masked Image')
    plt.imshow(save, cmap = 'gray')
    plt.show()
    m, bins, patches = plt.hist((save).flatten(), bins = range(0, 200, 10))
    plt.title('Grey Scale Masked Color Distribution')
    plt.xlabel("Color Bins")
    plt.ylabel("Number of Pixels")
    plt.show()
    sym = calculate_correlation(save)
    print("Symmetrical Value:", end =" ")
    print(sym)
    return None

def calculate_correlation(arr):
    #takes the array arr which is the masked image values
    #flips the array horizontally and vertically and compares this new array to the original to see how similar they are once flipped (how symmetrical)
    #returns the symmetry value (float)
    magic = np.copy(arr)
    m = np.where(magic!=0, 1, magic) 
    
    flipped_1 = np.flip(m, 0) 
    flipped_2 = np.flip(flipped_1, 1)
    
    correct = (m == flipped_2).sum()
    d = m.shape
    total = d[0] * d[1]
    sym = round(correct/total, 4)
    return sym

def normalize(arr):
    #takes the array arr which is a color array
    #normalizes the data (values 0-1, one being 120 colors 0 being 10)
    #returns the normalized array
    scaled = ((arr-10)/(120-10))
    return scaled

def createRandom(twenty, n, bcolor, hcolor, basym, hasym):
    #takes the int of 20% of the original data (amount of random values), the total int of values in one file, the original color and asymmetry arrays
    #picks 4 random healthy skin images and 4 random melanoma images and puts them in array 
    #returns the arrays of the four random healthy values and the 4 random melanoma values and their indices array
    save1 = random.sample(range(0, n-1), int(twenty/2)) #melanoma
    save2 = random.sample(range(0, n-1), int(twenty/2)) #healthy
    badcolor = np.zeros(int(twenty/2)) #4
    badasym = np.zeros(int(twenty/2))  #arrays for random values in data
    goodcolor = np.zeros(int(twenty/2)) 
    goodasym = np.zeros(int(twenty/2)) 
        
    for i in range(int(twenty/2)): #fill arrays
        space1 = int(save1[i])
        space2 = int(save2[i])
        badcolor[i] = bcolor[space1]
        badasym[i] = basym[space1]
        goodcolor[i] = hcolor[space2]
        goodasym[i] = hasym[space2]
    
    return badcolor, badasym, goodcolor, goodasym, save1, save2

def createMasterArr(bcolor, hcolor, basym, hasym, n):
    #takes the original color and asymmetry arrays and how long they each are (int)
    #uses 20% of the known data for testing how accurate the classification is
    #Therefore, it creates arrays for those 20% and puts the other 80% in arrays
    #returns the random value arrays, the known value arrays, and a classification array
    eighty = int((2*n)*.8) #32
    twenty = int((2*n)*.2) #8
    
    badcolor, badasym, goodcolor, goodasym, save1, save2 = createRandom(twenty, n, bcolor, hcolor, basym, hasym)
   
    restcolor = np.zeros(eighty) #32
    restasym = np.zeros(eighty)
    
    j = 0
    for i in range(n): #20
        if(i not in save1):
            restcolor[j] = bcolor[i]
            restasym[j] = basym[i]
            j+=1
    j = 16    
    for i in range(n):
        if(i not in save2):
            restcolor[j] = hcolor[i]
            restasym[j] = hasym[i]
            j+=1

    classificationb = np.ones(int(eighty/2)) #melanoma
    classificationh = np.zeros(int(eighty/2)) #healthy
    classification = np.concatenate((classificationb, classificationh))
    return restcolor, restasym, classification, badcolor, badasym, goodcolor, goodasym

def createRegArr(bcolor, hcolor, basym, hasym, n):
    #takes the melanoma and healthy arrays of known classification and their length
    #creates combined arrays of shared variables and a classification array
    #returns the combined arrays
    colors = np.concatenate((bcolor, hcolor))
    asym = np.concatenate((basym, hasym))
    classificationb = np.ones(n) #melanoma
    classificationh = np.zeros(n) #healthy
    classification = np.concatenate((classificationb, classificationh))
    return colors, asym, classification

def calculateDistanceArray(newcolor, newasym, color, asym):
    #takes the random color and asym values (floats) and the normalized color and asym arrays
    #creates a list of distances between the random color, asym point and every point on the plot and puts these distances into an array
    #returns the array of distances
    distances = []
    length = color.size
    for i in range(length):
        distances.append(math.sqrt((color[i]-newcolor)**2+(asym[i]-newasym)**2))
    dist_array = np.array(distances)
    return dist_array

def kNearestNeighborClassifier(k, newcolor, newasym, asym, color, classification):
    #takes the arguments k, the number of points tested closest to the point in question, the random color and asym values (floats) 
    #and the normalized color and asym arrays as well as the classification array
    #determines the classes of k number of points closest to the unknown point and determines which classification mostly surrounds the unknown point
    #returns the class the unknown point most likely is based on its surrounding points
    distAr = calculateDistanceArray(newcolor, newasym, color, asym)
    sorted_indices = np.argsort(distAr)
    k_indices = sorted_indices[:k]
    k_classifications = classification[k_indices]
    ones = 0
    zeros = 0
    for i in k_classifications:
        if(i == 1):
            ones += 1
        else:
            zeros += 1
    if(ones >= zeros):
        new_class = 1.0
    else:
        new_class = 0.0
    return new_class
    
def graphData(color, asym, classification, badcolor, badasym, goodcolor, goodasym, k):
    #takes the arrays of colors, asym, and classification as well as the random
    #points arrays and the number of cases to check using kNearestNeighbor
    #displays each arrays' data in a plot and distinguishes the data by color 
    #coding them (class 1 is black and class 0 is red)
    #returns the arrays of determined classifications of the random values
    imp = badcolor.size
    bclass_arr = np.zeros(imp)
    gclass_arr = np.zeros(imp)
    for i in range(imp):
        bclass_arr[i] = np.array(kNearestNeighborClassifier(k, badcolor[i], badasym[i], asym, color, classification))
        gclass_arr[i] = np.array(kNearestNeighborClassifier(k, goodcolor[i], goodasym[i], asym, color, classification))
    
    plt.figure()
    plt.plot(color[classification==1],asym[classification==1], "r.", label = "Melanoma")
    plt.plot(color[classification==0],asym[classification==0], "k.", label = "not Melanoma")
    
    #correct classifications
    plt.plot(badcolor[bclass_arr==1],badasym[bclass_arr==1], "r.", markersize = 20)
    plt.plot(goodcolor[gclass_arr==0],goodasym[gclass_arr==0], "k.", markersize = 20)
    
    #incorrect classifications
    plt.plot(goodcolor[gclass_arr==1],goodasym[gclass_arr==1], "r.", markersize = 20)
    plt.plot(badcolor[bclass_arr==0],badasym[bclass_arr==0], "k.", markersize = 20)
    
    plt.title('Data for Melanoma Traits')
    plt.xlabel("Number of Colors (10-120)")
    plt.ylabel("Symmetry")
    plt.legend()
    plt.show()
    return bclass_arr, gclass_arr

def graphUnknown(color, asym, classification, ucolor, uasym, k):
    #takes the known value arrays and unknown value arrays and the number of cases to check using kNearestNeighbor
    #plots the unknown values whose classes are determined using K-NearestNeighbor
    #returns the determined classes of the unknown cases
    imp = ucolor.size
    uclass_arr = np.zeros(imp)
    for i in range(imp):
        uclass_arr[i] = np.array(kNearestNeighborClassifier(k, ucolor[i], uasym[i], asym, color, classification))
    
    plt.figure()
    plt.plot(color[classification==1],asym[classification==1], "r.", label = "Melanoma")
    plt.plot(color[classification==0],asym[classification==0], "k.", label = "not Melanoma")
    
    plt.plot(ucolor[uclass_arr==1],uasym[uclass_arr==1], "r.", markersize = 20)
    plt.plot(ucolor[uclass_arr==0],uasym[uclass_arr==0], "k.", markersize = 20)
    
    plt.title('Unknown Sample')
    plt.xlabel("Number of Colors (10-120)")
    plt.ylabel("Symmetry")
    plt.legend()
    plt.show()
    return uclass_arr

def true(new_class, n):
    #takes an array of classifications of random values and the class int indicator (0 or 1)
    #based on the array (healthy or not) and n it calculates the True Positive, True Negative, False Positive, and False Negative rates
    #returns the percentage of the rate desired
    correct = 0
    count = 0
    for i in range(len(new_class)):
        if new_class[i] == n: 
                correct += 1
        count += 1
    return round((correct/count)*100, 2)

def compare(bclass, bad, gclass, good):
    #takes the arrays of random points' classifications, an array of 0s (good), and an array of 1s (bad)
    #determines the number of true positives, false positives, true negatives, and false positives and prints the results
    #returns none
    print("True Positives: " + str(true(bad, 1)) + "%")
    print("False Positives: " + str(true(good, 1)) + "%")
    print("True Negatives: " + str(true(good, 0)) + "%")
    print("False Negatives: " + str(true(bad, 0)) + "%")
    return None

