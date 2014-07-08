#!/usr/bin/env python


import sys
import os
from os import sep
from os.path import *
import subprocess


"""
1. Download Landsat
2. Unzip archive
3. Move extracted directory to Validation space and rename: ~/Documents/Capstone/Validation/{NEW_NAME}
4. Open a terminal window and 'cd' to the Validation direcotry: cd ~/Documents/Capstone/Validation
5. Set image directory path RELATIVE to script
6. Define file names for red/green/blue and output file (these are NOT relative - just the actual file name)
"""

image_directory = 'Landsat5_2009'

red_band1 = ''
green_band2 = ''
blue_band3 = ''
final_outfile = ''

print_mode = False  # If true, all commmands are only printed, NOT executed

merge_outfile = 'merge_output.tif'
temp_vrt = 'temp_vrt.vrt'





# ==== DO NOT EDIT BELOW THIS LINE ==== #





# Assemble file paths
image_directory = abspath(image_directory)
merge_outfile = image_directory + sep + merge_outfile
temp_vrt = image_directory + sep + temp_vrt
red_band1 = image_directory + sep + red_band1
green_band2 = image_directory + sep + green_band2
blue_band3 = image_directory + sep + blue_band3
final_outfile = image_directory + sep + final_outfile


# Make sure all parameters are supplied and can be found
bail = False
if not isdir(image_directory):
    bail = True
    print("ERROR: Can't find image_directory: %s" % str(image_directory))
if isfile(merge_outfile):
    bail = True
    print("ERROR: merge_outfile already exists: %s" % str(merge_outfile))
if isfile(temp_vrt):
    bail = True
    print("ERROR: temp_vrt already exists: %s" % str(temp_vrt))
if isfile(final_outfile):
    bail = True
    print("ERROR: final_outfile already exists: %s" % str(final_outfile))
if not isfile(red_band1):
    bail = True
    print("ERROR: Can't find red_band1: %s" % str(red_band1))
if not isfile(green_band2):
    bail = True
    print("ERROR: Can't find green_band2: %s" % str(green_band2))
if not isfile(blue_band3):
    bail = True
    print("ERROR: Can't find blue_band3: %s" % str(blue_band3))
if print_mode not in (True, False):
    bail = True
    print("ERROR: print_mode must be the actual python True or False type NOT a string")
if bail:
    sys.exit()


# Make sure there aren't any spaces or quotes in file paths
bail = False
for item in (temp_vrt, merge_outfile, final_outfile, red_band1, green_band2, blue_band3):
    if ' ' in item or '"' in item or "'" in item:
        bail = True
        print("ERROR: No spaces or quotes allowed in file paths")
        print("       %s" % str(item))
if bail:
    sys.exit()


# Merge bands into 1 file
merge_command = 'gdal_merge.py -v -separate -o %merge_outfile %blue_band3 %green_band2 %red_band1'
merge_command = merge_command.replace('%merge_outfile', merge_outfile).replace('%red_band1', red_band1).replace('%green_band2', green_band2).replace('%blue_band3', blue_band3)
if print_mode:
    print(merge_command)
else:
    subprocess.call(merge_command.split())


# Set a sane nodata value
warp_command = 'gdalwarp -of VRT -srcnodata -inf -dstnodata -9999 %merge_outfile %temp_vrt'
warp_command = warp_command.replace('%merge_outfile', merge_outfile).replace('%temp_vrt', temp_vrt)
if print_mode:
    print(warp_command)
else:
    subprocess.call(warp_command.split())


# Create final output file
translate_command = 'gdal_translate -ot Byte -scale 0 1 0 255 -co INTERLEAVE=BAND -co BIGTIFF=YES -co COMPRESS=DEFLATE -co PREDICTOR=2 -co TILED=YES -co PHOTOMETRIC=RGB %temp_vrt %final_outfile'
translate_command = translate_command.replace('%temp_vrt', temp_vrt).replace('%final_outfile', final_outfile)
if print_mode:
    print(translate_command)
else:
    subprocess.call(translate_command.split())


# Delete the temporary VRT file
if isfile(temp_vrt):
    os.remove(temp_vrt)


# Delete the merge file
if isfile(merge_outfile):
    os.remove(merge_outfile)


# Done
sys.exit()
