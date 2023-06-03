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
            GenerateArtBlocks();
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
        public void GenerateArtBlocks()
        {
            string filepath = FindFile();
            if (filepath == "0")
            {
                goto EndofFile; // in order to avoid mistakes
            }
            StreamReader f = new StreamReader(filepath);
            int newORold = Convert.ToInt32(f.ReadLine());
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
                        int blockORwall;
                        if (newORold == 1)
                        {
                            blockORwall = Convert.ToInt32(f.ReadLine());
                        } else
                        {
                            blockORwall = 1;
                        }
                        //string blockORwallT = f.ReadLine();
                        //int blockORwall = Convert.ToInt32(blockORwallT);

                        string tileT = f.ReadLine();
                        int tile = Convert.ToInt32(tileT);

                        string paintT = f.ReadLine();
                        int paint = Convert.ToInt32(paintT);

                        if (tileT != null)
                        {
                            if (blockORwall == 1) // tile
                            {
                                Tile curtile = _generatedSchematic.Tiles[x, y];
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
                                Tile curtile = _generatedSchematic.Tiles[x, y];
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
                            // Exit the cycle so as not to put dirt on all other cells
                        }
                    }

                    catch (Exception)
                    {
                        System.Windows.Forms.MessageBox.Show($"Tile placement error on ({x},{y})");
                        _generatedSchematic.Tiles[x, y] = null;
                        goto EndofFile; // in order to avoid mistakes
                    }
                }

            }

        //_clipboard.LoadedBuffers.Add(buffer);
            // System.Windows.Forms.MessageBox.Show("Program execution completed", "Pixel-Art created");
            f.Close();

            _generatedSchematic.RenderBuffer();
            _wvm.Clipboard.LoadedBuffers.Add(_generatedSchematic);
            _wvm.ClipboardSetActiveCommand.Execute(_generatedSchematic);
        EndofFile:
            int opok;

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
