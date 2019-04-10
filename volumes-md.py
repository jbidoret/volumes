#-*- coding: utf-8 -*-

# volumes.lu
# md file for each publisher and each book, kirby flavoured

# config
csv_filepath = 'csv/volumes-le-havre-dominant.csv'

# imports
import os
import csv
import sys
from shutil import copyfile

# hifi slugification
sys.path.insert(0, 'libs')
from slughifi import slughifi



# open csv
csv_file = open(csv_filepath, "rt")
reader = csv.reader(csv_file, delimiter=';', quotechar ='"')

publishers = []
publisher_idx = 0

for row_idx, row in enumerate(reader):
    
    publisher = row[0]
    title = row[1]
    author = row[2]
    book_url = row[3]
    collection = row[4]
    book_ref = row[5]
    width = row[7].replace(',','.')
    height = row[8].replace(',','.')
    depth = row[6].replace(',','.')
    credits = row[9]
    price = row[10]
    idx = row[11]
    canonical = row[12]
    clr = row[13]
    
    # store publisher
    if not row[0] in publishers:
        publisher_idx += 1
        print('====')
        print(publisher)
        book_index = 0
        publishers.append(publisher)

    # create publisher dir
    publisher_path = 'publishers/{}_{}'.format(publisher_idx, slughifi(publisher))
    if not os.path.exists(publisher_path):
        os.makedirs(publisher_path)
        # create txt file for publisher
    publisher_filename=os.path.join(publisher_path, 'publisher.txt')
    publisher_file = open(publisher_filename, "w")
    publisher_file.write('Title: {}'.format(publisher))
    publisher_file.write("\n\n----\n\n")
    publisher_file.write('Publisher_url: {}'.format( "/".join(book_url.split('/')[0:3]) ))
    publisher_file.write("\n\n----\n\n")
    publisher_file.close()

    print('----')
    print(title)
    book_slug = slughifi(title)
    book_path = os.path.join(publisher_path, '{}_{}'.format(book_index, book_slug))
    if not os.path.exists(book_path):
        os.makedirs(book_path)

    book_filename=os.path.join(book_path, 'book.txt')
    book_file = open(book_filename, "w")
    if "¶" in title :
        title, subtitle = [t.strip() for t in title.split("¶")]
        
    book_file.write('Title: {}'.format(title))
    book_file.write("\n\n----\n\n")
    
    try:
        book_file.write('Subtitle: {}'.format(subtitle))
        book_file.write("\n\n----\n\n")
    except Exception as e:
        pass

    book_file.write('Publisher: {}'.format(publisher))
    book_file.write("\n\n----\n\n")

    book_file.write('Author: {}'.format(author))
    book_file.write("\n\n----\n\n")

    book_file.write('Credits: {}'.format(credits))
    book_file.write("\n\n----\n\n")

    book_file.write('Book_url: {}'.format(book_url))
    book_file.write("\n\n----\n\n")

    book_file.write('Price: {}'.format(price))
    book_file.write("\n\n----\n\n")

    book_file.write('Ref: {}'.format(book_ref))
    book_file.write("\n\n----\n\n")

    book_file.write('Width: {}'.format(width))
    book_file.write("\n\n----\n\n")

    book_file.write('Height: {}'.format(height))
    book_file.write("\n\n----\n\n")

    book_file.write('Depth: {}'.format(depth))
    book_file.write("\n\n----\n\n")

    book_file.write('Idx: {}'.format(idx))
    book_file.write("\n\n----\n\n")
    
    img_path = "./couvs/{}.jpg".format(book_ref)

    # copy file
    img_filename=os.path.join(book_path, '{}.jpg'.format(book_ref))
    copyfile(img_path, img_filename)
    
    # color
    book_file.write('Color: {}'.format(clr))
    book_file.write("\n\n----\n\n")

    book_index += 1 
    book_file.close()

print('====')
csv_file.close()