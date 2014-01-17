
import ROOT

def style():
	ROOT.gStyle.SetOptStat( 0 )
	ROOT.gStyle.SetHistLineWidth( 2 )
	ROOT.gStyle.SetTitleFontSize( 0.03 )
	# Set the paper and margin sizes:
	ROOT.gStyle.SetPaperSize( 20, 26 )
	ROOT.gStyle.SetPadTopMargin( 0.05 )
	ROOT.gStyle.SetPadRightMargin( 0.05 )
	ROOT.gStyle.SetPadBottomMargin( 0.16 )
	ROOT.gStyle.SetPadLeftMargin( 0.16 )
	# set title offsets (for axis label)
	ROOT.gStyle.SetTitleXOffset(1.4);
	ROOT.gStyle.SetTitleYOffset(1.4);
	# Put tick marks on top and rhs of the plots:
	ROOT.gStyle.SetPadTickX( 1 )
	ROOT.gStyle.SetPadTickY( 1 )

	# larger, non-boldface font:
	font_type = 42
	font_size = 0.05
	ROOT.gStyle.SetTextFont( font_type )
	ROOT.gStyle.SetTextSize( font_size )
	ROOT.gStyle.SetLabelFont( font_type, "x" )
	ROOT.gStyle.SetLabelSize( font_size, "x" )
	ROOT.gStyle.SetTitleFont( font_type, "x" )
	ROOT.gStyle.SetTitleSize( font_size, "x" )
	ROOT.gStyle.SetLabelFont( font_type, "y" )
	ROOT.gStyle.SetLabelSize( font_size, "y" )
	ROOT.gStyle.SetTitleFont( font_type, "y" )
	ROOT.gStyle.SetTitleSize( font_size, "y" )
	ROOT.gStyle.SetLabelFont( font_type, "z" )
	ROOT.gStyle.SetLabelSize( font_size, "z" )
	ROOT.gStyle.SetTitleFont( font_type, "z" )
	ROOT.gStyle.SetTitleSize( font_size, "z" )

