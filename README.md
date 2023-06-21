# The project is frozen. 
I am planning to remake the main script from python to c#. This will take some time, so don't expect any updates just yet. 
# PixelArtCreator For Terraria
We will work with the tiles and colors that are the result of the [PaletteAnalyzer](https://github.com/MKSO4KA/PaletteAnalyzerKey) mod. 
### Step0: Lyrical digression
Using the [RussDev7](https://github.com/RussDev7/RussDev7) [materials](https://github.com/RussDev7/Extracting-Terraria-Map-Colors#extracting-colors-from-the-terraria-map):
1. Using the source code provided in the first step of his tutorial, we have created our plugin for [TEdit](https://github.com/TEdit/Terraria-Map-Editor), which places all tiles and walls (except sprites and loose blocks) from the terraria. The name of the plugin is **"PaletteCreator"**.
2. Using the source code of his "SortHexColors" program, and also using the source code provided in the second step of his tutorial, we created the **[PaletteAnalyzyzerKey mod](https://github.com/MKSO4KA/PaletteAnalyzerKey) for [TModLoader](https://github.com/tModLoader/tModLoader)**.  
 Check Vided on YT - [VIDEO](https://youtu.be/H4xKAvQ9Yr8) 
### Step 1: Preparation before using all programs created by us
First things first, you **should have a "C:\ARTs\" directory**. **In this directory there should be an exceptions.txt(and torchs.txt)** file, in exceptions you should write **blocks that are better not to use** when creating art (In my file, all those blocks that, in my opinion, can cause some errors when developing art on the map).   
Blocks occupying more than one cell on the map should be registered in the exception file (Interior items for example)  
The torch file must contain blocks that can cling to walls. (like torches)(The torch file means substituting the wall for the blocks whose number is written in the file.)  
Exceptions and torch files are interconnected, if you want to use a torch (as a tile) in your art, then you need to put it in the torch file, and remove it from the exception file.  
In the folder **"C:\ARTs\colors" you should create a file maxtileXndY.txt**, in which on the first and second line you should write the maximum X and Y where the program(TEdit PaletteCreator) stopped(default: x = 200; y = 1100).

### Step 2: Working with python script
The Python script is designed in such a way that it only normally closes with **Ctrl+C**. Normal - **that is, writing the saved set of colors and pixels to a binary file** to be able to continue later. The script accepts 3 values from the user: The first is to The first is the directory to the png file. The second is whether to continue working on the image (Y or N)(If you started earlier and ended with ctrl + c). The third is the question of whether the previous palette should be used. (Analysis of the entire image, which occurs at the very beginning, during this process it is impossible to stop the program) The analyzed palette allows, in some cases, to speed up the transformation of the image into textures.  
All this script written by me works as follows: First, the image palette is analyzed. Then the selected palette is compared with the colors of the terraria palette. Subsequently, the resulting new palette is used to find tiles from it.

<details>
  <summary>From image to terraria pixels</summary>

  ![Image](https://github.com/MKSO4KA/PixelArtCreator-ForTerraria/assets/88591984/18c961aa-9ea3-474e-85c3-c3e2df66ff76) - Source
1. 1
2. 50
3. 50
4. 0
5. 153
6. 26
7. 0
8. 153
9. 26
10. 0
11. ...

  The file created as a result of the program ( file.txt in C:\ARTs) will later be used to create art using the PixelArtCreator plugin.
</details>

## Step3:Reworking functions in TEdit
To do this, I use an open source application called [TEdit](https://github.com/TEdit/Terraria-Map-Editor) and replace and add new features. 
<details>
  <summary>ViewModelLocator</summary>
The function is in this path : ..src\TEdit\ViewModel\ViewModelLocator.cs
We have to add the line written under the spoiler. (Add line after line 49 of file)

  
  ```csharp

            wvm.Plugins.Add(new PixelArtCreator(wvm)); // this
            wvm.Plugins.Add(new PaletteCreator(wvm));  // and this
            

  ```
  
</details>
<details>
<summary>WorldViewModel.Editor</summary>
The function is in this path : ..src\TEdit\ViewModel\WorldViewModel.Editor.cs
We need to change line 828 to make the function public.

  
```csharp

            public void SetPixelAutomatic(Tile curTile,
                                       int? tile = null,
                                       int? wall = null,
                                       byte? liquid = null,
                                       LiquidType? liquidType = null,
                                       bool? wireRed = null,
                                       short? u = null,
                                       short? v = null,
                                       bool? wireBlue = null,
                                       bool? wireGreen = null,
                                       bool? wireYellow = null,
                                       BrickStyle? brickStyle = null,
                                       bool? actuator = null, bool? actuatorInActive = null,
                                       int? tileColor = null,
                                       int? wallColor = null,
                                       bool? wallEchoCoating = null,
                                       bool? wallIlluminantCoating = null,
                                       bool? tileEchoCoating = null,
                                       bool? tileIlluminantCoating = null)
  ```

  
</details>

<details>
  <summary>Plugins</summary>
 Adding a new plugin along this path -..src\TEdit\Editor\Plugins\PixelArtCreator.cs
  
 Adding a new plugin along this path -..src\TEdit\Editor\Plugins\PaletteCreator.cs
 
</details>

## Step4:Build and Test
Once a project has been created, it can be tested. A new button will appear in the PixelArtCreator plugins, by clicking on which you can create art from pre-prepared txt files.

