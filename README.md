# PixelArtCreator For Terraria
We will work with the tiles and colors that are the result of the [PaletteAnalyzer](https://github.com/MKSO4KA/PaletteAnalyzerKey) mod. 
### Step0: Lyrical digression
Using the [RussDev7](https://github.com/RussDev7/RussDev7) [materials](https://github.com/RussDev7/Extracting-Terraria-Map-Colors#extracting-colors-from-the-terraria-map):
1. Using the source code provided in the first step of his tutorial, we have created our plugin for [TEdit](https://github.com/TEdit/Terraria-Map-Editor), which places all tiles and walls (except sprites and loose blocks) from the terraria. The name of the plugin is "PaletteCreator".
2. Using the source code of his "SortHexColors" program, and also using the source code provided in the second step of his tutorial, we created the [PaletteAnalyzyzerKey mod](https://github.com/MKSO4KA/PaletteAnalyzerKey) for [TModLoader](https://github.com/tModLoader/tModLoader).
### Step 1: Working with python script
The Python script is designed in such a way that it only normally closes with Ctrl+C. Normal - that is, writing the saved set of colors and pixels to a binary file. The script accepts 3 values from the user: The first is to enable or disable the script (
Y or N). The second is whether to continue working on the image (Y or N). Third, the accepted value in this clause will determine whether the palette of colors will be saved for subsequent art.

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

![20230515_223526 (1)](https://github.com/MKSO4KA/PixelArtCreator-ForTerraria/assets/88591984/f5f8ab56-a40b-44aa-89ee-5ea37e807ab5)

