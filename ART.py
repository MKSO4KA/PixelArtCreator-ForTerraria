from PIL import Image, ImageColor, ImageFilter
import colorsys
import time
import math
import pickle
import platform
import os
import shutil
from tkinter import filedialog as fd
from tkinter import Tk
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

root = Tk()
root.geometry("258x185")
root.configure(bg = "#E87E7E")
canvas = Canvas(
    root,
    bg = "#E87E7E",
    height = 185,
    width = 258,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    85.0,
    90.0,
    anchor="nw",
    text="SUBMIT",
    fill="#1C1616",
    font=("Pacifico Regular", 24 * -1)
)
canvas.create_text(
    50.0,
    20.0,
    anchor="nw",
    text="choose png file",
    fill="#1C1616",
    font=("Pacifico Regular", 24 * -1)
)

# figd_BnIE2DeEj5D4HUrJZseVsvYbFUiQXdBqvXW6nnty
name = fd.askopenfilename(defaultextension="png")
print(name)

root.bind("<Button-1>", lambda x: root.destroy())
root.mainloop()
class ART:
    def __init__(self,nam):
        self.location_png = nam
    #pngX = "art.png"
        self.name = str(input("What should call art?"))
        if f"{platform.system()[:3]}" == "Win":
            print(f"You are {platform.system()} user")
            self.locationX = str('C:\\ARTs\\')
            self.location_name = self.locationX + 'ARTS' + "\\" + self.name + "\\" + "backup" + "\\"
        else:
            print(f"You are {platform.system()} user")
            self.locationX = str('/storage/emulated/0/ART/')
            self.location_name = self.locationX + 'ARTS' + "/" + self.name + "/"  + "backup" + "/"
        #pngX = 'art_denoise.png'
        print("enter png-file path")
    #location_png = callback()
    #print(locationY)
        self.imgX = Image.open(self.location_png)
    #imgX.show()
        self.oldORnew = 1 # 1 == new # 0 == old #
        try:
            os.makedirs(self.location_name)
        except OSError:
            shutil.rmtree(self.location_name[:-7])
            os.makedirs(self.location_name)
        print("File will be located on this path %s " % self.location_name[:-7])
        shutil.copyfile(self.location_png, self.location_name[:-7] + self.name + '.png')



    def k(self):

        location = self.locationX
        # = self.pngX
        img = self.imgX
        #img = img.filter(ImageFilter.GaussianBlur(2))

        w, h = img.size
        massive = []
        start_time2 = time.time()
        i = 0
        t = time.time()
        cout = 0
        for x in range(0, w ): # - round(0, 8 * w)

            #start_time2 = time.time()
            #print(str(x) + ", " + str(round(elapsed_time, 2)) + "секунд" + ", " + str(i) + "\n")
            i = 0
            for y in range(0, h):  # 1000000
                p = img.getpixel((x, y))
                if time.time() - t >= 5.0:
                    t = time.time()
                    print(time.strftime('%H:%M:%S') + ':', x, "of", w)

                if p not in massive:
                    i += 1
                    massive.append(p)
        print(len(massive),round((time.time() - start_time2),2))  # 128472
        massive.sort(key=lambda x: (x[0], x[1], x[2]))
        # 1
        # 39
        # 29
        # 010101
        f = open(location + 'tiles.txt', 'r')
        l = [str(i[:-1]) for i in f]
        i = len(l)
        #print(i, i/4)
        f.close()
        f = open(location + 'tiles.txt', 'r')
        tilesNpaint = []
        files = []
        blocks = []
        count = 0
        for item in range(0, i // 4):
            count += 1
            cow = f.readline()
            k = f.readline()
            y = f.readline()
            z = f.readline()
            tupka = tuple((cow[:-1], k[:-1], y[:-1], z[:-1]))
            tilesNpaint.append(tupka)
            files.append(z[:-1])
            tupka = tuple((cow[:-1], k[:-1], y[:-1]))
            blocks.append(tupka)

        f.close()
        #print(count)


        def hexornEX(fline, massiv):  # 595, tilesNpaint (1,29,30,(HEX))
            line = massiv[fline]
            #print(line,fline)
            tileORpaint = line[0]
            tile = line[1]
            paint = line[2]
            hex = line[3]
            #print((tileORpaint, tile, paint))
            return (tileORpaint, tile, paint)

        def chosecor(HSV, num, file):  # Choose the most suitable color according to HSV
            site = []
            for i in range(0, len(file)):
                if HSV == 1:
                    print("HSV - not exists")
                else:
                    l = ImageColor.getrgb('#' + file[i])
                    o = num
                site.append((o[0] - l[0]) ** 2 + (o[1] - l[1]) ** 2 + (o[2] - l[2]) ** 2)
            #print(site.index(min(site)))
            return site.index(min(site))

        list_colors = []
        list_tiles = []
        start_time = time.time()
        start_time2 = time.time()
        start_time3 = time.time() - start_time
        l = 1
        t = time.time()
        for x, i in enumerate(massive):
            elapsed_time = time.time() - start_time2
            start_time2 = time.time()
            all_time = time.time() - start_time
            numb = chosecor(0, i, files)
            col = files[numb]
            list_colors.append(i[0:3]) #RGB
            #list_colors.append(col)
            list_tiles.append(hexornEX(numb, tilesNpaint)) # 1,29,0

            if time.time() - t >= 5.0:
                t = time.time()
                print(time.strftime('%H:%M:%S') + ':', x, "of", len(massive), "total:",round(all_time / 60), "min")
        return list_tiles,list_colors


    def g(self):
        #png = self.pngX
        location = self.locationX
        Fname = self.location_name
        def func():
            listp = art.k() #0 = tiles; #1 = colors(rgb)
            with open(self.location_name + 'massiveT.ob', 'wb+') as fp:
                pickle.dump(listp[0], fp)
            with open(self.location_name + 'massiveC.ob', 'wb+') as fp:
                pickle.dump(listp[1], fp)
            return listp

        def fonc():
            lists = []
            try:
                with open(self.location_name + 'massiveT.ob', 'rb') as fp:
                    lists.append(pickle.load(fp))
                with open(self.location_name + 'massiveC.ob', 'rb') as fp:
                    lists.append(pickle.load(fp))
                listo = tuple(lists)
            except IOError:
                print("tiles or colors not find")
                listo = func()
            return listo

        def find(color, massivT, massivC):
            return massivT[massivC.index(color)] # ('0', '153', '1')
        onORoff = 0
        enable = 1

        # The location where all files are located
        #location = str('C:\\ARTs\\')
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
        for item in range(0, i // 4):
            cow = f.readline()
            k = f.readline()
            y = f.readline()
            z = f.readline()
            if (k[:-1] in sprites) and int(cow[:-1]) == 1:
                poop = 1 + 1
            else:
                tupka = tuple((cow[:-1], k[:-1], y[:-1], z[:-1]))
                tilesNpaint.append(tupka)
                files.append(z[:-1])
        f.close()

        # print("\n",len(files), "len of files\n", len(tilesNpaint), "len tiles\n", len(sprites), "len sprites\n") # Debug TEST
        def tileNDpaint(fline, massiv):  # 595, tilesNpaint
            line = massiv[fline]
            tileORpaint = line[0]
            tile = line[1]
            paint = line[2]
            return (tileORpaint, tile, paint) #not uses

        def continueorrestart(w, h):
            poop = str(input("Do you want to continue with the file?(y or n)"))
            if poop != ("n" or "N" or "No" or "NO" or "no" or "nO"):
                return WndH(w, h)
            else:
                my_file = open(Fname[:-7] + "file.txt", "w")
                my_file.write(str(self.oldORnew) + "\n" + str(w) + "\n" + str(h))
                my_file.close()
                print(w, h, "Image dimensions\n", 0, 0, "Start Pixel")
                return (0, 0, 0)

        def continueor():
            poop = str(input("New art? - Y or N"))
            if poop != ("n" or "N" or "No" or "NO" or "no" or "nO"):
                lists = func()
            else:
                lists = fonc()
            return lists



        def WndH(w, h):
            backup_file = open(Fname + 'backup.txt', 'r+')
            touka = int(backup_file.readline()[:-1])
            touka = (touka - 2) // 3
            wstart = int(math.floor(touka / h))
            hstart = touka % h
            print(w, h, "Image dimensions\n", wstart, hstart, "Start Pixel")
            return (wstart, hstart, touka)

        # HSV does not work well, so it is initially disabled at the top (OnorOFF variable, change its value to 1 if you want to enable HSV mode)

        def rgb2hsv(tup):  # RGB into HSV # not use
            (r, g, b) = (tup[0], tup[1], tup[2])
            # normalize
            (r, g, b) = (r / 255, g / 255, b / 255)
            # convert to hsv
            (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
            # expand HSV range
            (h, s, v) = (int(h * 179), int(s * 255), int(v * 255))
            return (h, s, v)

        def chosecor(HSV, num, file):  # Choose the most suitable color according to HSV
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

        def findnearby(color, mass):  # color, colors # ((255, 58, 47), ('536', '30'))
            if color in mass:
                return mass[mass.index(color) + 1]
            else:
                return 0

        img = self.imgX
        #img = img.filter(ImageFilter.GaussianBlur(2))
        w, h = img.size
        # counter = 0

        # Working with the original (input) image
        start_time = time.time()
        start_time2 = time.time()
        (wstart, hstart, tyolka) = continueorrestart(w, h)
        lists = continueor()
        try:
            my_file = open(Fname[:-7] + "file.txt", "a+")
            for w1 in range(wstart, w):
                elapsed_time = time.time() - start_time2
                start_time2 = time.time()
                all_time = time.time() - start_time
                print(time.strftime('%H:%M:%S') + ':', w1, "of", w, "in", round(elapsed_time), "sec.", "Total:",
                      round(all_time / 60), "min")
                for h1 in range(hstart, h):
                    p = img.getpixel((w1, h1))[0:3]

                    fndnerby = find(p, lists[0], lists[1])
                    if fndnerby == fndnerby:
                        (tileORpaint, tile, paint) = fndnerby
                        my_file.write("\n" + str(tileORpaint) + "\n" + str(tile) + "\n" + str(paint))
                        tyolka += 1
                    else:
                        (tileORpaint, tile, paint) = tileNDpaint(chosecor(onORoff, p, files), tilesNpaint)
                        my_file.write("\n" + str(tileORpaint) + "\n" + str(tile) + "\n" + str(paint))
                        tyolka += 1
                    #colors.append(p)
                    #colors.append((tileORpaint, tile, paint))
                    #if len(colors) > 2000:
                        #colors = []
                    #my_file.close()
                hstart = 0
            my_file.close()

        except KeyboardInterrupt:
            print("\n", "The program correctly stopped at", (w1, h1), "pixel")
            my_file.close()

            f = open(Fname[:-7] + 'file.txt', 'r')
            # print(w1,h1)
            l = [str(i[:-1]) for i in f]
            i = len(l)
            f.close()
            backup_file = open(Fname + 'backup.txt', "w+")
            backup_file.write(str(i) + '\n')
            backup_file.close()

        raise SystemExit
        #return print(self.arg)

art = ART(name)
art.g()