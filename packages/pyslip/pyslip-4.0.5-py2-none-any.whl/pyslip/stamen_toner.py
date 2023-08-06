"""
A tile source that serves Stamen Toner tiles from the internet.

Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.
"""

import math
import pyslip.tiles_net as tiles_net


###############################################################################
# Change values below here to configure an internet tile source.
###############################################################################

# attributes used for tileset introspection
# names must be unique amongst tile modules
TilesetName = 'Stamen Toner Tiles'
TilesetShortName = 'STMT Tiles'
TilesetVersion = '1.0'

# the pool of tile servers used
TileServers = ['http://tile.stamen.com',
              ]

# the path on the server to a tile
# {} params are Z=level, X=column, Y=row, origin at map top-left
TileURLPath = '/toner/{Z}/{X}/{Y}.png'

# tile levels to be used
TileLevels = range(17)

# maximum pending requests for each tile server
MaxServerRequests = 2

# set maximum number of in-memory tiles for each level
MaxLRU = 10000

# size of tiles
TileWidth = 256
TileHeight = 256

# where earlier-cached tiles will be
# this can be overridden in the __init__ method
TilesDir = 'stamen_toner_tiles'

################################################################################
# Class for these tiles.   Builds on tiles_net.Tiles.
################################################################################

class Tiles(tiles_net.Tiles):
    """An object to source internet tiles for pySlip."""

    def __init__(self, tiles_dir=TilesDir):
        """Override the base class for these tiles.

        Basically, just fill in the BaseTiles class with values from above
        and provide the Geo2Tile() and Tile2Geo() methods.
        """

        super().__init__(TileLevels, TileWidth, TileHeight,
                         servers=TileServers, url_path=TileURLPath,
                         max_server_requests=MaxServerRequests,
                         max_lru=MaxLRU, tiles_dir=tiles_dir)

    def Geo2Tile(self, geo):
        """Convert geo to tile fractional coordinates for level in use.

        geo  tuple of geo coordinates (xgeo, ygeo)

        Note that we assume the point *is* on the map!

        Code taken from [http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames]
        """

        (xgeo, ygeo) = geo
        lat_rad = math.radians(ygeo)
        n = 2.0 ** self.level
        xtile = (xgeo + 180.0) / 360.0 * n
        ytile = ((1.0 - math.log(math.tan(lat_rad) + (1.0/math.cos(lat_rad))) / math.pi) / 2.0) * n

        return (xtile, ytile)

    def Tile2Geo(self, tile):
        """Convert tile fractional coordinates to geo for level in use.

        tile  a tupl;e (xtile,ytile) of tile fractional coordinates

        Note that we assume the point *is* on the map!

        Code taken from [http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames]
        """

        (xtile, ytile) = tile
        n = 2.0 ** self.level
        xgeo = xtile / n * 360.0 - 180.0
        yrad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        ygeo = math.degrees(yrad)

        return (xgeo, ygeo)

