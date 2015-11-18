from .color import Color

class Palette():
    def __init__(self, rawPal):
        try:
            self.colorPixels = { Color(*col[1]):col[0] for col in rawPal }
        except TypeError:
            raise PaletteEmptyException("Raw palette None or invalid. Color limit may have been exceeded.")
        
    @property
    def colors(self):
        return [ k for (v,k) in sorted( zip( self.colorPixels.values(), self.colorPixels.keys() ), reverse=True ) ]
        
    def __iter__(self):
        return iter(self.colors)
        
    def __len__(self):
        return len(self.colors)
        
class PaletteEmptyException( Exception ):
    '''Raise when rawPal comes up as None'''