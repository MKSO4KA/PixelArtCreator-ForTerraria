from PIL import Image, ImageDraw, ImageColor
import colorsys
import time
import math
import pickle
onORoff = 0
enable = int(input("Enable the script? \nAre you sure? \nWrite 1: "))
location = str('C:\\ARTs\\') # The location where all files are located
if enable == 0:
    exit()

# Open the file and enter the data into the array once
f = open(location + 'exceptions.txt', 'r')
l = [str(i[:-1]) for i in f]
i = len(l)
f.close()
f = open(location + 'exceptions.txt', 'r')
sprites = []
for item in range(0, i):
    k = f.readline()
    sprites.append(k[:-1])
f.close()

files = []
# Open the file and enter the data into the array once
f = open(location + 'tiles.txt', 'r')
l = [str(i[:-1]) for i in f]
i = len(l)
f.close()
f = open(location + 'tiles.txt', 'r')
tilesNpaint = []
for item in range(0, i//4):
    cow = f.readline()
    k = f.readline()
    y = f.readline()
    z = f.readline()
    if (k[:-1] in sprites) and int(cow[:-1])==1:
        poop = 1 + 1
    else:
        tupka = tuple((cow[:-1],k[:-1], y[:-1], z[:-1]))
        tilesNpaint.append(tupka)
        files.append(z[:-1])
f.close()

#print("\n",len(files), "len of files\n", len(tilesNpaint), "len tiles\n", len(sprites), "len sprites\n") # Debug TEST
def tileNDpaint(fline, massiv):    # 595, tilesNpaint
    line = massiv[fline]
    tileORpaint = line[0]
    tile = line[1]
    paint = line[2]
    return (tileORpaint,tile,paint)
def continueorrestart(w,h):
  poop = str(input("Do you want to continue with the file?(1 or 0)"))
  if poop == "1":
      return WndH(w,h)
  else:
      my_file = open(location + "file.txt", "w")
      my_file.write(str(w))
      my_file.write("\n")
      my_file.write(str(h))
      my_file.close()
      print(w,h,"Image dimensions\n",0,0,"Start Pixel")
      return (0,0,0)
def WndH(w,h):
    backup_file = open(location + 'backup.txt', 'r+')
    touka = int(backup_file.readline()[:-1])
    touka = (touka - 2)//3
    wstart = int(math.floor(touka/h))
    hstart = touka % h
    print(w,h,"Image dimensions\n",wstart,hstart,"Start Pixel")
    return (wstart, hstart,touka)

# HSV does not work well, so it is initially disabled at the top (OnorOFF variable, change its value to 1 if you want to enable HSV mode)


def rgb2hsv(tup):  # RGB into HSV
    (r, g, b) = (tup[0], tup[1], tup[2])
    # normalize
    (r, g, b) = (r / 255, g / 255, b / 255)
    # convert to hsv
    (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
    # expand HSV range
    (h, s, v) = (int(h * 179), int(s * 255), int(v * 255))
    return (h, s, v)


def chosecor(HSV, num, file): # Choose the most suitable color according to HSV
    site = []
    for i in range(0, len(file)):
        if HSV == 1:
            o = rgb2hsv(num)
            l = rgb2hsv(ImageColor.getrgb('#' + file[i]))
        else:
            l = ImageColor.getrgb('#' + file[i])
            o = num
        site.append((o[0] - l[0]) ** 2 + (o[1] - l[1]) ** 2 + (o[2] - l[2]) ** 2)
    return site.index(min(site))

# Looking for a suitable color in RGB (in theory)

def findnearby(color, mass): # color, colors # ((255, 58, 47), ('536', '30'))
    if color in mass:
        return mass[mass.index(color)+1]
    else:
        return 0

img = Image.open(location + "art.png")
w, h = img.size
counter = 0

# Working with the original (input) image
ilop = 1
start_time = time.time()
start_time2 = time.time()
tyolka = 0
(wstart,hstart,tyolka) = continueorrestart(w,h)
try:
  with open (location + 'colors.ob', 'rb') as fp:
    colors = pickle.load(fp)
except IOError:
    print("colors.ob not find")
    colors = []
try:
       
  for w1 in range(wstart,w):
      elapsed_time = time.time() - start_time2
      start_time2 = time.time()
      all_time = time.time() - start_time
      print(time.strftime('%H:%M:%S')+':',w1,"of", w,"in", round(elapsed_time),"sec.","All:", round(all_time/60),"min")
      for h1 in range(hstart, h):
          p = img.getpixel((w1, h1))
          my_file = open(location + "file.txt", "a+")
          if findnearby(p,colors):
              (tileORpaint, tile, paint) = findnearby(p, colors)
              my_file.write("\n")
              my_file.write(str(tileORpaint))
              my_file.write("\n")
              my_file.write(str(tile))
              my_file.write("\n")
              my_file.write(str(paint))
              tyolka += 1
          else:
              (tileORpaint, tile, paint) = tileNDpaint(chosecor(onORoff, p, files), tilesNpaint)
              my_file.write("\n")
              my_file.write(str(tileORpaint))
              my_file.write("\n")
              my_file.write(str(tile))
              my_file.write("\n")
              my_file.write(str(paint))
              tyolka += 1
          colors.append(p)
          colors.append((tileORpaint, tile, paint))
          my_file.close()
      hstart = 0

except KeyboardInterrupt:
    with open(location + 'colors.ob', 'wb+') as fp:
       pickle.dump(colors, fp)
       print("\n","The program correctly stopped at",(w1,h1),"pixel")
       f = open(location + 'file.txt', 'r')
       #print(w1,h1)
       l = [str(i[:-1]) for i in f]
       i = len(l)
       f.close()
       backup_file = open(location + 'backup.txt',"w+")
       backup_file.write(str(i) +'\n')
       backup_file.close()
       
raise SystemExit
print('END \n')