# PixelArtCreator For Terraria
We will work with the files that are the result of the [PaletteAnalyzer](https://github.com/MKSO4KA/PaletteAnalyzerKey) mod. 
### Step0: Lyrical digression
Using the [RussDev7](https://github.com/RussDev7/RussDev7) [materials](https://github.com/RussDev7/Extracting-Terraria-Map-Colors#extracting-colors-from-the-terraria-map):
1. Using the source code provided in the first step of his tutorial, we have created our plugin for TEdit, which places all tiles and walls (except sprites and loose blocks) from the terraria. The name of the plugin is "PaletteCreator".
2. Using the source code of his "SortHexColors" program, and also using the source code provided in the second step of his tutorial, we created the [PaletteAnalyzyzerKey mod](https://github.com/MKSO4KA/PaletteAnalyzerKey) for TModLoader.
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
  
  ```csharp

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
  ```

</details>

## Step4:Build and Test
Once a project has been created, it can be tested. A new button will appear in the PixelArtCreator plugins, by clicking on which you can create art from pre-prepared txt files.

![20230515_223526 (1)](https://github.com/MKSO4KA/PixelArtCreator-ForTerraria/assets/88591984/f5f8ab56-a40b-44aa-89ee-5ea37e807ab5)

