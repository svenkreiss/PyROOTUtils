import ROOT
from array import array

      




def nonLinearSmooth(h2):
   """ Non-linear smoothing of 2D histogram. This is essentially a 2D median filter. """
   for x in range( h2.GetNbinsX()-2 ):
      for y in range( h2.GetNbinsY()-2 ):
         centerBin = x+2 + (y+2)*(h2.GetNbinsX()+2)
         surroundingBins = [
            centerBin-1, #this row
            centerBin+1,
            centerBin-1 - (h2.GetNbinsX()+2), # row above
            centerBin   - (h2.GetNbinsX()+2),
            centerBin+1 - (h2.GetNbinsX()+2),
            centerBin-1 + (h2.GetNbinsX()+2), # row below
            centerBin   + (h2.GetNbinsX()+2),
            centerBin+1 + (h2.GetNbinsX()+2),
         ]
         surroundingBinValues = [ h2.GetBinContent(b) for b in surroundingBins ]
         if h2.GetBinContent(centerBin) < min(surroundingBinValues)  or  \
            h2.GetBinContent(centerBin) > max(surroundingBinValues):
               h2.SetBinContent(centerBin, sum(surroundingBinValues)/8.0)

def subtractMinFromHist( h ):
   minVal = 1e30
   # exclude under- and overflow bins from minimum scan
   for x in range( h.GetNbinsX() ):
      for y in range( h.GetNbinsY() ):
         bin = x+1 + (y+1)*(h.GetNbinsX()+2)
         if h.GetBinContent(bin) < minVal: minVal = h.GetBinContent(bin)
   for i in range( (h.GetNbinsX()+2)*(h.GetNbinsY()+2) ):
      h.SetBinContent(i, h.GetBinContent(i)-minVal)
   return h

def interpolate( h, x, y=None, z=None, outOfRangeValue=30 ):
   """ Interpolation is valid inside the volume defined by the outer bin _centers_. """

   if x != x: return outOfRangeValue
   if x <= h.GetXaxis().GetBinCenter(1)  or  x >= h.GetXaxis().GetBinCenter(h.GetXaxis().GetNbins()): return outOfRangeValue
   
   if y != None:
      if y != y: return outOfRangeValue
      if y <= h.GetYaxis().GetBinCenter(1)  or  y >= h.GetYaxis().GetBinCenter(h.GetYaxis().GetNbins()): return outOfRangeValue
   if z != None:
      if z != z: return outOfRangeValue
      if z <= h.GetZaxis().GetBinCenter(1)  or  z >= h.GetZaxis().GetBinCenter(h.GetZaxis().GetNbins()): return outOfRangeValue
   
   if y != None and z != None: return h.Interpolate( x, y, z )
   if y != None: return h.Interpolate( x, y )
   return h.Interpolate( x )






class Band( ROOT.TGraph ):
   def __init__( self, x, yLow, yHigh, style="full", fillColor=None, lineColor=None, lineStyle=None, lineWidth=None, shiftBand=None ):
      """Possible styles: full, upperEdge, lowerEdge"""
      
      if style not in ["full", "upperEdge", "lowerEdge"]:
         print( "Style unknown. Using \"full\"." )
         style = "full"
      if len(x) != len(yLow) or len(x) != len(yHigh):
         print( "x, yLow and yHigh have to have the same length." )
         return
         
      if shiftBand:
         yLow = [y+s for y,s in zip(yLow,shiftBand)]
         yHigh = [y+s for y,s in zip(yHigh,shiftBand)]
         
      if style=="full":
         band_values =  sorted([(v[0],v[1]) for v in zip(x,yLow)])
         band_values += sorted([(v[0],v[1]) for v in zip(x,yHigh)], reverse=True)
         ROOT.TGraph.__init__( self, len(band_values), array('d',[v[0] for v in band_values]), array('d',[v[1] for v in band_values]) )
         self.SetLineWidth(0)
         
      if style=="upperEdge":
         band_values = [(v[0],v[1]) for v in zip(x,yHigh)]
         ROOT.TGraph.__init__( self, len(band_values), array('d',[v[0] for v in band_values]), array('d',[v[1] for v in band_values]) )
      
      if style=="lowerEdge":
         band_values = [(v[0],v[1]) for v in zip(x,yLow)]
         ROOT.TGraph.__init__( self, len(band_values), array('d',[v[0] for v in band_values]), array('d',[v[1] for v in band_values]) )

      if fillColor:
         self.SetFillColor( fillColor )
      if lineColor:
         self.SetLineColor( lineColor )
      if lineStyle:
         self.SetLineStyle( lineStyle )
      if lineWidth:
         self.SetLineWidth( lineWidth )
      
      

def DrawLine( x1,y1,x2,y2, lineWidth=None, lineStyle=None, lineColor=None, NDC=False ):
   l = ROOT.TLine( x1,y1,x2,y2 )
   if lineWidth: l.SetLineWidth( lineWidth )
   if lineStyle: l.SetLineStyle( lineStyle )
   if lineColor: l.SetLineColor( lineColor )
   
   if NDC:
      l.DrawLineNDC( x1,y1,x2,y2 )
   else:
      l.Draw()
   
   return l

def DrawHLine( y, lineWidth=None, lineStyle=None, lineColor=None ):
   ROOT.gPad.Update()
   x1,y1,x2,y2 = ( ROOT.Double(),ROOT.Double(),ROOT.Double(),ROOT.Double() )
   ROOT.gPad.GetRangeAxis( x1,y1, x2,y2 )
   return DrawLine(
      x1,y, x2,y,
      lineWidth, lineStyle, lineColor,
   )

def DrawVLine( x, lineWidth=None, lineStyle=None, lineColor=None ):
   ROOT.gPad.Update()
   x1,y1,x2,y2 = ( ROOT.Double(),ROOT.Double(),ROOT.Double(),ROOT.Double() )
   ROOT.gPad.GetRangeAxis( x1,y1, x2,y2 )
   return DrawLine(
      x,y1, x,y2,
      lineWidth, lineStyle, lineColor,
   )
   
def DrawBox( x1,y1, x2,y2, fillColor=None, lineColor=None, lineWidth=None, lineStyle=None ):
   b = ROOT.TBox( x1,y1, x2,y2 )
   if fillColor: b.SetFillColor( fillColor )
   if lineColor: b.SetLineColor( lineColor )
   if lineStyle: b.SetLineColor( lineStyle )
   if lineWidth: b.SetLineColor( lineWidth )
   b.Draw()
   return b


def DrawTextOneLine( x, y, text, textColor = 1, textSize = 0.04, NDC = True, halign = "left", valign = "bottom", skipLines = 0 ):
   """ This is just a helper. Don't use. Use DrawText instead. """
   
   halignMap = {"left":1, "center":2, "right":3}
   valignMap = {"bottom":1, "center":2, "top":3}
   
   scaleLineHeight = 1.0
   if valign == "top": scaleLineHeight = 0.8
   if skipLines: text = "#lower[%.1f]{%s}" % (skipLines*scaleLineHeight,text)
   
   # Draw the text quite simply:
   import ROOT
   l = ROOT.TLatex()
   if NDC: l.SetNDC()
   l.SetTextAlign( 10*halignMap[halign] + valignMap[valign] )
   l.SetTextColor( textColor )
   l.SetTextSize( textSize )
   l.DrawLatex( x, y, text )
   return l
   
def DrawText( x, y, text, textColor = 1, textSize = 0.04, NDC = True, halign = "left", valign = "bottom" ):
   objs = []
   skipLines = 0
   for line in text.split('\n'):
      objs.append( DrawTextOneLine( x, y, line, textColor, textSize, NDC, halign, valign, skipLines ) )
      if NDC == True: y -= 0.05 * textSize/0.04
      else:
         skipLines += 1
      
   return objs

def DrawTextAligned( x,y, textList, halignList=["right","center","left"], textColor = 1, textSize = 0.04, NDC = True, valign="bottom" ):
   """ use to write a = b and c = d under each other with the equal signs aligned """
   objs = []
   for text,halign in zip( textList, halignList ):
      objs.append( DrawText( x,y, text, textColor, textSize, NDC, halign, valign ) )
   return objs


