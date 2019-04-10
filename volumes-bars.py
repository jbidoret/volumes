#-*- coding: utf-8 -*-

# volumes.lu
# books in chromatography
# a tribute to Karel Martens

# makes uses of scikit KMeans and misc dominantColor.py scripts found on the web
# read https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097

# config
csv_filepath = 'csv/volumes-le-havre-dominant.csv'
svg_filepath = 'svg/volumes-bars.svg'

# imports
import csv
import sys
import cv2
import numpy as np
from sklearn.cluster import KMeans

# open csv
csv_file = open(csv_filepath, 'rt')
reader = csv.reader(csv_file, delimiter=';', quotechar ='"')

file = open(svg_filepath, "w")
file.write('<svg xmlns="http://www.w3.org/2000/svg" width="8200" height="14000" viewBox="0 0 8200 14000" xmlns:xlink="http://www.w3.org/1999/xlink">\n')

# init values 
publishers = []
publisher_maximum_height = 0
publisher_y = 0
publisher_x = 0
margin = 10

def find_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist


for row_idx, row in enumerate(reader):
    
    # fetch data from csv
    publisher = row[0]
    title = row[1].replace('&', '&amp;')
    book_ref = row[5]
    width = row[7].replace(',','.') # inconsistencies with csv numbers
    height = row[8].replace(',','.') # inconsistencies with csv numbers
    dominant = row[13]
    
    # init publisher
    if not row[0] in publishers:            
        print('====')
        print(publisher)
        # reset values for each publisher
        publisher_y = publisher_y + publisher_maximum_height + margin
        publisher_x = 0
        publisher_maximum_height = 0
        # append publisher to list
        publishers.append(publisher)
    
    # start svg <g>
    file.write( "<g id=\"book_{}\">\n".format(book_ref) ) 

    px_width = float(width) * 10
    px_height = float(height) * 10 
    
    # augment row height for publisher if needed
    if publisher_maximum_height < px_height:
        publisher_maximum_height = px_height 
    
    # draw rect
    # with dominant color from csv (volumes-colors-to-csv.py has already been run)
    print('----')
    print(title)

    img_path = "./couvs/{}.jpg".format(book_ref)
    
    # Using KMeans clustering, draw an histogram of the image file
    cvimg = cv2.imread(img_path)
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)

    cvimg = cvimg.reshape((cvimg.shape[0] * cvimg.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=5) #cluster number
    clt.fit(cvimg)

    hist = find_histogram(clt)

    startY = publisher_y

    for (percent, color) in zip(hist, clt.cluster_centers_):
        h = percent * px_height
        endY = startY + h
        
        r,g,b = [str(x) for x in color.astype("uint8").tolist()]
        rgb = "rgb({},{},{})".format(r,g,b) 
        file.write('<rect x="{}" y="{}" fill="{}" width="{}" height="{}"/>\n'.format(
            publisher_x, 
            startY, 
            rgb, 
            px_width, h)
        )        
        startY = endY

    # end svg <g>
    file.write("</g>\n")
    publisher_x = publisher_x + px_width + margin
    
    
file.write('</svg>')
file.close()

print('====')

csv_file.close()

