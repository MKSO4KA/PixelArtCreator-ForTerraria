# PixelArtCreator For Terraria
To begin with, I would like to clarify that I only worked with the tiles and colors that  [RussDev7](https://github.com/RussDev7/RussDev7) provide.  [Extracting Colors From The Terraria Map](https://github.com/RussDev7/Extracting-Terraria-Map-Colors#extracting-colors-from-the-terraria-map). 
### Step0: Lyrical digression
[RussDev7](https://github.com/RussDev7/RussDev7) has figured out the extraction of colors, however, not all of these colors are suitable for us, because most of them are either sprites or loose blocks. And we also adhered to this position: The more colors are used, the more time it will take to process the photo. **On version 1.4.3.6 of the terraria, I counted 438 blocks that are better not to be placed**, because something can break or spoil them. (blocks of rope, cobwebs, sand and others have also been removed from the list of used blocks). In total, we have +- 250 blocks left that we can use (that's +- 8000 colors). 
### Step1: Sort and choose colors
Next, with the color sorting program provided by RussDev, we sort only the tiles. The tiles are copied to an empty txt file.Then the so-called "dancing with a tambourine" will begin. We have to replace None with 0, Red with 1 and so on. Below is a list of colors:



<details>
  <summary>Paint-Number</summary>

Paint | number
-- | --
None | 0
Red | 1
Orange | 2
Yellow (Attention, the main list says it's Red) | 3
Lime | 4
Green | 5
Teal | 6
Cyan | 7
SkyBlue | 8
Blue | 9
Purple | 10
Violet | 11
Pink | 12
DeepRed | 13
DeepOrange | 14
DeepYellow | 15
DeepLime | 16
DeepGreen | 17
DeepTeal | 18
DeepCyan | 19
DeepSkyBlue | 20
DeepBlue | 21
DeepPurple | 22
DeepViolet | 23
DeepPink | 24
Black | 25
White | 26
Gray | 27
Brown | 28
Shadow | 29
Negative | 30
Illuminant | 31


</details>




Next, using Notepad ++ and macros in it, we create a macro that will add a space and the number 1 to all the tiles on the left (we will need it a little later)


TorW | tile | paint | color | time
-- | -- | -- | -- | --
  | 0 | 0 | 976B4B | Was
1 | 0 | 0 | 976B4B | Became


Next, we sort only the walls, after sorting, we throw them into a txt file. In the same txt, following the same scheme, using a macro, add 0 at the beginning of the line.

TorW | tile | paint | color | time
-- | -- | -- | -- | --
  | 1 | 0 | 343434 | Was
0 | 1 | 0 | 343434 | Became

After sorting and adding zeros and ones, either we merge both of these files together to get a certain mixture of tiles and walls, or we throw it all into the sorting program (RussDev) and only then, after removing duplicates, throw it into a separate file. Later we work only with this file. As you can understand, the units at the beginning of the lines are the designations of the tiles, the zeros are the walls. This is necessary for subsequent manipulations with PyCharm. But first, you need to remake this file into a suitable one for my file: Using the same macros in Notepad ++, we separate numbers, tiles, paint and colors (Block = line) by removing extra spaces before and after a block of numbers.

<details>
  <summary>Block = Line</summary>

0 | 1 | 0 | 343434 | Was
-- | -- | -- | -- | -- 


Became
-- |
0 | 
1 | 
0 | 
343434

</details>

Strictly speaking, this completes the preparation of colors.

## Step 2: Working with python script
The Python script is designed in such a way that it only normally closes with Ctrl+C. Normal - that is, writing the saved set of colors and pixels to a binary file. I just started to understand python, so the code can definitely be shortened and made smarter. But for now, that's the best I can do. The script converts the input image into a file, where each line contains information about the placed block.
<details>
  <summary>From image to terraria pixels</summary>

  ![Image](https://user-images.githubusercontent.com/88591984/238437609-5dfa5c0b-def3-4e72-90af-331f8a846741.png) - Source

file.txt
--
6
7
1
342
30
1
536
30
1
536
30
1
536
30
1
7
29
1
7
29
1
371
3
1
536
30
1
536
30
1
536
30
1
195
0
1
7
29
1
7
29
1
340
3
1
342
30
1
536
30
1
195
0
1
7
29
1
7
29
1
7
29
1
340
3
1
7
29
1
7
29
1
7
29
1
7
29
1
7
29
1
223
3
1
340
3
0
63
1
1
344
30
1
507
3
1
408
3
1
162
3
1
340
3
1
340
3
1
344
30
1
536
30
1
162
3
1
340
3
1
340
3
1
340
3
1
340
3

</details>


## Step3:Reworking functions in TEdit
To do this, I use an open source application called [TEdit](https://github.com/TEdit/Terraria-Map-Editor) and replace and add new features. 
<details>
  <summary>ViewModelLocator</summary>
The function is in this path : ..src\TEdit\ViewModel\ViewModelLocator.cs
We have to add the line written under the spoiler. (Add line after line 49 of file)

  
  ```csharp

            wvm.Plugins.Add(new PixelArtCreator(wvm)); // this

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
  <summary>PixelArtCreator</summary>
 Adding a new function along this path -..src\TEdit\Editor\Plugins\PixelArtCreator.cs
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Windows;
using System.Windows.Media.Imaging;
using TEdit.Editor.Clipboard;
using TEdit.Geometry.Primitives;
using TEdit.Terraria;
using TEdit.Terraria.Objects;
using TEdit.ViewModel;
using Microsoft.Win32;
using SharpDX.Direct3D11;
using System.Runtime.Remoting.Lifetime;
using TEdit.Editor.Tools;
//using SharpDX.Direct2D1.Effects;

using static Microsoft.ApplicationInsights.MetricDimensionNames.TelemetryContext;
using System.Windows.Input;
using TEdit.UI.Xaml.XnaContentHost;

namespace TEdit.Editor.Plugins
{
    
    public class PixelArtCreator : BasePlugin, INotifyPropertyChanged
    {
        public PixelArtCreator(WorldViewModel worldViewModel) : base(worldViewModel)
        {
            Name = "Pixel-Art's Creator";
        }

        private ClipboardBuffer _generatedSchematic;
        public ClipboardBuffer GeneratredSchematic
        {
            get { return _generatedSchematic; }
            set { _generatedSchematic = value; OnPropertyChanged(); }
        }

        private WriteableBitmap _preview;
        public WriteableBitmap Preview
        {
            get { return _preview ??= _generatedSchematic?.Preview; }
            set { _preview = value; OnPropertyChanged(); }
        }

        public override void Execute()
        {
            GenerateTextStatues();
        }

        private bool guessAnActive()
        {
            // Initializes the variables to pass to the MessageBox.Show method.
            string message = "Disabling blocks when creating \"art\" will allow all blocks to be displayed on the map. This is convenient if the \"art\" is large, or if it is created in a new undeveloped area.";
            string caption = "Turn off blocks in art?";
            System.Windows.Forms.MessageBoxButtons buttons = System.Windows.Forms.MessageBoxButtons.YesNo;
            System.Windows.Forms.DialogResult result;

            // Displays the MessageBox.
            result = System.Windows.Forms.MessageBox.Show(message, caption, buttons);
            if (result == System.Windows.Forms.DialogResult.Yes)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        private string FindFile()
        {
            try
            {
                var ofd = new OpenFileDialog();
                ofd.Filter = "Pixel Art default file|*.txt";
                ofd.DefaultExt = "Pixel Art default file|*.txt";
                ofd.Title = "Import TXT file with tiles nd paint";
                ofd.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                if (!Directory.Exists(ofd.InitialDirectory)) { Directory.CreateDirectory(ofd.InitialDirectory); }
                ofd.Multiselect = false;
                if ((bool)ofd.ShowDialog())
                {
                    string filename = Path.GetFullPath(ofd.FileName);
                    // MessageBox.Show(filename, "debug for me", MessageBoxButton.OK, MessageBoxImage.Error);
                    return filename;
                }
                else
                {
                    string filename = "0";
                    return filename;
                }

            }
            catch (Exception)
            {
                string filename = "0";
                //MessageBox.Show(ex.Message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return filename;
            }


        }
        // /*
        public void GenerateTextStatues()
        {
        EdofStr:
            string filepath = FindFile();
            if (filepath == "0")
            {
                goto EdofStr; // in order to avoid mistakes
            }
            StreamReader f = new StreamReader(filepath);

            int width = Convert.ToInt32(f.ReadLine());
            int height = Convert.ToInt32(f.ReadLine());
            bool TActive = guessAnActive();

            Vector2Int32 _generatedSchematicSize = new Vector2Int32(width, height);
            _generatedSchematic = new(_generatedSchematicSize, true);

            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    try
                    {
                        string blockORwallT = f.ReadLine();
                        string tileT = f.ReadLine();
                        string paintT = f.ReadLine();
                        int blockORwall = Convert.ToInt32(blockORwallT);
                        int tile = Convert.ToInt32(tileT);
                        int paint = Convert.ToInt32(paintT);

                        if (tileT != null)
                        {
                            if (blockORwall == 1) // tile
                            {
                                Tile curtile = _wvm.CurrentWorld.Tiles[x, y];
                                //_wvm.UndoManager.SaveTile(x, y); // Add tile to the undo buffer.
                                curtile.Type = (ushort)tile;
                                curtile.IsActive = true; // Turn on tile
                                curtile.InActive = TActive;
                                curtile.TileColor = (byte)paint; // Set necessary paint
                                                                 //_wvm.UpdateRenderPixel(new Vector2Int32(x, y)); // Update pixel(show on map)
                                _generatedSchematic.Tiles[x, y] = curtile;
                            }
                            else //wall
                            {
                                Tile curtile = _wvm.CurrentWorld.Tiles[x, y];
                                //_wvm.UndoManager.SaveTile(x, y); // Add tile to the undo buffer.
                                curtile.Wall = (ushort)tile;
                                //curtile.Type = (ushort)erase;
                                //WorldViewModel.SetPixel(curile, isErase);
                                curtile.IsActive = true; // Turn on tile
                                //curtile.InActive = TActive;
                                curtile.WallColor = (byte)paint;
                                //_wvm.UpdateRenderPixel(new Vector2Int32(x, y)); // Update pixel(show on map)
                                _wvm.SetPixelAutomatic(curtile, tile: -1, u: 0, v: 0);
                                _generatedSchematic.Tiles[x, y] = curtile;
                            }
                        }
                        else
                        {
                            _generatedSchematic.Tiles[x, y] = null;
                            goto LeaveTileLoop;
                            // Exit the cycle so as not to put dirt on all other cells
                        }
                    }

                    catch (Exception)
                    {
                        System.Windows.Forms.MessageBox.Show($"Tile placement error on ({x},{y})");
                        _generatedSchematic.Tiles[x, y] = null;
                    }
                }

            }

        //_clipboard.LoadedBuffers.Add(buffer);
        LeaveTileLoop:
            // System.Windows.Forms.MessageBox.Show("Program execution completed", "Pixel-Art created");
            f.Close();

            _generatedSchematic.RenderBuffer();
            _wvm.Clipboard.LoadedBuffers.Add(_generatedSchematic);
            _wvm.ClipboardSetActiveCommand.Execute(_generatedSchematic);
        }
// */
        
        public new event PropertyChangedEventHandler PropertyChanged;
        // Create the OnPropertyChanged method to raise the event
        // The calling member's name will be used as the parameter.
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }
}

</details>
