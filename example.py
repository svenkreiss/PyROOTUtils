
import ROOT
import PyROOTUtils
import PyROOTUtils.style

# to prevent python garbage collection of objects that still need to drawn
container = []

def main():
	canvas = ROOT.TCanvas("c","c",600,450)
	axes = canvas.DrawFrame( -90,-90,90,90 )
	axes.GetXaxis().SetTitle( "x [km]" )
	axes.GetYaxis().SetTitle( "y [km]" )

	hLine = PyROOTUtils.DrawHLine( 0.0, lineStyle=ROOT.kDotted, lineWidth=1 )
	v = PyROOTUtils.ModelConfigUtils.varsDictFromString('alpha=0.1')
	bla = PyROOTUtils.DrawText( 0.2, 0.7, "This is just random text\nto show how easy it can be\nto write aligned multi-line text\nand how varsDictFromString('alpha=0.1') works: "+str(v), textSize=0.035)

	l1 = PyROOTUtils.Legend( 0.2,0.2, textSize=0.035, valign="bottom" )
	l1.AddEntry( hLine, "line at y=0", "L" )
	l1.Draw()

	l2 = PyROOTUtils.Legend( 0.9,0.9, textSize=0.035, halign="right" )
	l2.AddEntry( hLine, "line at y=0", "L" )
	l2.Draw()

	container.append( (hLine,bla,l1,l2) )
	canvas.SaveAs( 'doc/example.png' )
	print( 'Image saved to doc/example.png.' )


if __name__ == "__main__":
	main()