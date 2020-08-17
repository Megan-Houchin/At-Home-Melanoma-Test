#Final Project
#*****************************************
# YOUR NAME: Megan Houchin
#NUMBER OF DAYS TO COMPLETE: 6 days

# IMPORT STATEMENTS
import final_functions as ff
import numpy as np

# DEMONSTRATION CODE

#Accuracy of K-Nearest Neighbor
colors_arrb = ff.color_info(20, "bad")
colors_arrh = ff.color_info(20, "good")

asym_arrb = ff.get_asym_info(20, 'bad')
asym_arrh = ff.get_asym_info(20, 'good')

colors_arrb = ff.normalize(colors_arrb)
colors_arrh = ff.normalize(colors_arrh)

color, asym, classification, badcolor, badasym, goodcolor, goodasym = ff.createMasterArr(colors_arrb, colors_arrh, asym_arrb, asym_arrh, 20)

bad, good = ff.graphData(color, asym, classification, badcolor, badasym, goodcolor, goodasym, 3)

bclass = np.ones(4)
gclass = np.zeros(4)

ff.compare(bclass, bad, gclass, good)

#Classification of an Unknown Case:
color, asym, classification = ff.createRegArr(colors_arrb, colors_arrh, asym_arrb, asym_arrh, 20)
ucolors = ff.color_info(1, "unknown")
uasym = ff.get_asym_info(1, "unknown")
ucolors = ff.normalize(ucolors)
unknown = ff.graphUnknown(color, asym, classification, ucolors, uasym, 3)

#Printing an Example of the Color Segmentation Process and Asymmetry Determination Process:
ff.color_example('Malignant_stuff/M2.jpg')
ff.asym_example('Healthy_stuff/H3.jpg')
ff.asym_example('Unknown_stuff/U1.jpg')
