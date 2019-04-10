#-*- coding: utf-8 -*-

# volumes.lu
# books colors

# config
csv_filepath = 'csv/volumes-le-havre-dominant.csv'
svg_filepath = 'svg/volumes-colors.svg'

# imports
import csv
import sys

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

    file.write('<rect id="rect_{}" x="{}" y="{}" fill="{}" width="{}" height="{}"/>\n'.format(row_idx, publisher_x, publisher_y, dominant, px_width, px_height))

    # end svg <g>
    file.write("</g>\n")
    publisher_x = publisher_x + px_width + margin
    
    
file.write('</svg>')
file.close()

print('====')

csv_file.close()

