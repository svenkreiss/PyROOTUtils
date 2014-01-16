
import ROOT
from array import array




class Legend( ROOT.TLegend ):
   def __init__( self, x1, y1, x2 = 1.1, y2 = 1.1, halign = "fixed", valign = "fixed", font=42, textSize = None ):
      """
         Either use like (x1,y1,x2,y2) or (x1,y1,halign="left",valign="top").
         If just (x1,y1) is used, halign="left" and valign="top" is assumed.
         
         Change the font with font=62 (default is 42).
      """
      if x2 == 1.1  and  halign == "fixed": halign = "left"
      if y2 == 1.1  and  valign == "fixed": valign = "top"
      self.halign = halign
      self.valign = valign
      ROOT.TLegend.__init__( self, x1, y1, x2, y2 )
      self.SetTextFont( font )
      if textSize: self.SetTextSize( textSize )

   def Draw( self ):
      # the coordinates in x1,y1 are always the corner the legend sticks to
      
      # need to set a fixed font size for the functions below to work
      if self.halign != "fixed" or self.valign != "fixed":
         if self.GetTextSize() < 0.0001:
            self.SetTextSize( 0.04 )
      
      # valign
      height = 1.3*self.GetTextSize()*self.GetNRows()
      if self.valign == "top":
         self.SetY2( self.GetY1() )
         self.SetY1( self.GetY2() - height )
      if self.valign == "bottom":
         self.SetY2( self.GetY1() + height )
      if self.valign == "center":
         center = self.GetY1()
         self.SetY2( center + height/2 )
         self.SetY1( center - height/2 )

      # halign
      width = 0.15 + self.GetTextSize()*self.GetNColumns()
      if self.halign == "left":
         self.SetX2( self.GetX1() + width )
      if self.halign == "right":
         self.SetX2( self.GetX1() )
         self.SetX1( self.GetX2() - width )
      if self.halign == "center":
         center = self.GetX1()
         self.SetX1( center - width/2 )
         self.SetX2( center + width/2 )

      self.SetFillStyle( 0 )
      self.SetBorderSize( 0 )
      ROOT.TLegend.Draw( self )
