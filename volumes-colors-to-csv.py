#-*- coding: utf-8 -*-

# volumes.lu
# dominant colour from image to svg

# config
csv_filepath = 'csv/volumes-le-havre.csv'
csv_output_filepath = 'csv/volumes-le-havre-dominant.csv'

# imports
import csv
import sys

sys.path.insert(0, 'libs/dominant_image_colour')
from dominant_colour import most_frequent_colour

# pip install Pillow
from PIL import Image

# open csv
csv_file = open(csv_filepath, "rt")
csv_output_file = open(csv_output_filepath, "w+")
reader = csv.reader(csv_file, delimiter=';', quotechar ='"')
writer = csv.writer(csv_output_file, delimiter=';', quotechar ='"')


for row_idx, row in enumerate(reader):
    
    # fetch data from csv
    publisher = row[0]
    title = row[1].replace('&', '&amp;')
    book_ref = row[5]

    img_path = "./couvs/{}.jpg".format(book_ref)

    # output dominant color to csv
    im = Image.open(img_path)
    color = most_frequent_colour(im)
    rgb ='rgb{}'.format(color)
    print ("{}, {}: {}".format(publisher, title, rgb))
    row.append(rgb)
    writer.writerow(row)

    
print('====')

csv_file.close()
csv_output_file.close()
