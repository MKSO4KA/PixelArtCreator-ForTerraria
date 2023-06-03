using System;
using System.Linq;
using TEdit.ViewModel;
using System.IO;
using System.Windows;
using TEdit.Terraria;

namespace TEdit.Editor.Plugins
{
    internal class PaletteCreator : BasePlugin
    {
        public PaletteCreator(WorldViewModel worldViewModel) : base(worldViewModel)
        {
            Name = "Palette Creator";
        }
        public override void Execute()
        {
            PaletteSetter();
        }

        public void PaletteSetter()
        {
            // Stage World Vars
            int minx = 100;
            int maxx = this._wvm.CurrentWorld.TilesWide - 100;
            int miny = 100;
            int maxy = this._wvm.CurrentWorld.TilesHigh - 100;

            // Reset Vars
            int tile = 0;
            int paint = 0;
            //bool useGlass = false;

            string path = @"C:\ARTs\exceptions.txt";
            string[] readText = File.ReadAllLines(path);
            // First Do Tiles
            for (int x = minx; x < maxx; x++)
            {
                for (int y = miny; y < maxy; y++)
                {
                    try
                    {
                        Tile curTile = this._wvm.CurrentWorld.Tiles[x, y];
                        curTile.Type = (ushort)tile;
                        World.GetTileProperties(tile);
                        if (!readText.Contains(Convert.ToString(tile)) )
                        {
                            curTile.IsActive = true;
                            curTile.TileColor = (byte)paint;
                            curTile.InActive = true;
                            _wvm.UpdateRenderPixel(x, y);
                        }
                        /*
                        foreach (string s in readText)
                        {
                            Console.WriteLine(s);
                        } 
                        */

                        /*
                        if (World.TileProperties.Count == curTile.Type)
                        {
                            goto LeaveTileLoop;
                        }
                        */


                        if (tile == World.TileCount && paint == 30)
                        {
                            // Define New Vars
                            minx = (x + 2);
                            goto LeaveTileLoop;
                        }

                        if (paint == 30)
                        {
                            tile++;
                            paint = 0;
                        }
                        else
                        {
                            paint++;
                        }

                    }
                    catch (Exception)
                    {
                        System.Windows.Forms.MessageBox.Show($"Tile placement error on ({x},{y}) tile - ({tile})");
                        goto LeaveTileLoop;
                    }
                }

                // Offset Right
                x++;
            }

        LeaveTileLoop:

            // Reset Vars
            tile = 1;
            paint = 0;

            // Next Do Walls
            for (int x = minx; x < maxx; x++)
            {
                for (int y = miny; y < maxy; y++)
                {
                    try
                    {
                        this._wvm.CurrentWorld.Tiles[x, y].Wall = (ushort)tile;
                        this._wvm.CurrentWorld.Tiles[x, y].WallColor = (byte)paint;
                        _wvm.UpdateRenderPixel(x, y);

                        if (tile == World.WallCount && paint == 30)
                        {
                            // Define New Vars
                            minx = x;
                            goto LeaveWallLoop;
                        }

                        if (paint == 30)
                        {
                            tile++;
                            paint = 0;
                        }
                        else
                        {
                            paint++;
                        }
                    }
                    catch (Exception)
                    {
                        //MessageBox.Show("Error.");
                    }
                }
            }

        LeaveWallLoop:
            System.Windows.Forms.MessageBox.Show("Finished.");

        }
        // */

    }
}
