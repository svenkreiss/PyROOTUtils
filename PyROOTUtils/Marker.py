import ROOT
from array import array

      
class Marker( ROOT.TMarker ):
   def __init__( self, x,y, markerColor=None, markerStyle=5 ):
      ROOT.TMarker.__init__( self, x,y, markerStyle )
      if markerColor: self.SetMarkerColor( markerColor )


class CrossMarker( ROOT.TMarker ):
   """ A special class just for "cross" markers where the line-width is adjustable. """
   
   # holds drawn TLines for memory management
   container = []

   def __init__( self, x,y, markerColor=ROOT.kBlack, markerSize=1.0, lineWidth=3 ):
      ROOT.TMarker.__init__( self, x,y, 5 )
      self.SetMarkerSize( markerSize )

      self.x = x
      self.y = y
      self.markerSize = markerSize
      self.markerColor = markerColor
      self.lineWidth = lineWidth

   def Draw(self):
      """
      Standard markers have size 8px (my guess is (8px,8px) but don't know for sure).
      Convert self.x and self.y to AbsPixel coordinates and draw in pixels.
      """

      # convert x and y to AbsPixel coordinates
      u = ROOT.gPad.XtoAbsPixel( self.x )
      v = ROOT.gPad.YtoAbsPixel( self.y )

      t1 = ROOT.TLine()
      t1.SetLineWidth( self.lineWidth )
      t1.SetLineColor( self.markerColor )
      t1.DrawLine(
         ROOT.gPad.AbsPixeltoX( int(u - 4*self.markerSize) ), 
            ROOT.gPad.AbsPixeltoY( int(v - 4*self.markerSize) ),
         ROOT.gPad.AbsPixeltoX( int(u + 4*self.markerSize) ), 
            ROOT.gPad.AbsPixeltoY( int(v + 4*self.markerSize) ),
      )
      t2 = ROOT.TLine()
      t2.SetLineWidth( self.lineWidth )
      t2.SetLineColor( self.markerColor )
      t2.DrawLine(
         ROOT.gPad.AbsPixeltoX( int(u - 4*self.markerSize) ), 
            ROOT.gPad.AbsPixeltoY( int(v + 4*self.markerSize) ),
         ROOT.gPad.AbsPixeltoX( int(u + 4*self.markerSize) ), 
            ROOT.gPad.AbsPixeltoY( int(v - 4*self.markerSize) ),
      )

      self.container.append( (t1,t2) )

