#-*- coding: utf-8 -*-

# volumes.lu
# books spines

# config
csv_filepath = 'csv.csv'
svg_filepath = 'arthur.svg'
fontSize = 10

# imports
import csv

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
arthuridx = 0
bookidx = 0
for row_idx, row in enumerate(reader):
    
    
    # arthur :

    size = row[0]
    width = size.split("x")[0].replace(',','.')
    height = size.split("x")[1].replace(',','.')
    if arthuridx == 20:            
        print('====')
        
        # reset values for each publisher
        publisher_y = publisher_y + publisher_maximum_height + margin
        publisher_x = 0
        publisher_maximum_height = 0
        # append publisher to list
        arthuridx = 0

    
    # start svg <g>
    file.write( "<g id=\"book_{}\">\n".format(bookidx) ) 

    px_width = float(width) * 10
    px_height = float(height) * 10 
    
    # augment row height for publisher if needed
    if publisher_maximum_height < px_height:
        publisher_maximum_height = px_height 
    
    # draw rect
    print('----')
    # print(title)
    file.write('<rect id="rect_{}" x="{}" y="{}" fill="rgb(0,0,0)" width="{}" height="{}"/>\n'.format(row_idx, publisher_x, publisher_y, px_width, px_height))


    file.write("</g>\n")
    publisher_x = publisher_x + px_width + margin
    bookidx += 1
    
    
file.write('</svg>')
file.close()

print('====')

csv_file.close()

