
import ROOT
import PyROOTUtils
PyROOTUtils.style()

# to prevent python garbage collection of objects that still need to drawn
container = []



def content( mHBestFit=130.0, height1SigmaLabel=10.0, color=ROOT.kBlue ):
	# make mock curve
	linSpace = [ 100 + i*60.0/300.0 for i in range(300) ]
	likelihood          = [ (x, (x-mHBestFit)*(x-mHBestFit)/25.0) for x in linSpace ]
	likelihood_statOnly = [ (x, (x-mHBestFit)*(x-mHBestFit)/20.0) for x in linSpace ]
	# draw curve
	g = PyROOTUtils.Graph( likelihood, lineColor=color, lineWidth=2 )
	g.Draw()
	g_statOnly = PyROOTUtils.Graph( likelihood_statOnly, lineColor=color, lineWidth=2, lineStyle=ROOT.kDashed )
	g_statOnly.Draw()

	# find 68% CL interval from likelihood
	low,high = g.getFirstIntersectionsWithValue(1.0)
	vLineM1Sigma = PyROOTUtils.DrawVLine( low, lineStyle=ROOT.kDashed, lineWidth=1, lineColor=color )
	vLineP1Sigma = PyROOTUtils.DrawVLine( high, lineStyle=ROOT.kDashed, lineWidth=1, lineColor=color )
	hLine1Sigma = PyROOTUtils.DrawLine( low,height1SigmaLabel,high,height1SigmaLabel, lineWidth=5, lineColor=color )
	label1Sigma = PyROOTUtils.DrawText( mHBestFit,height1SigmaLabel, ("#lower[-0.5]{%.1f^{%+.1f}_{%+.1f} GeV}"%(mHBestFit,high-mHBestFit,low-mHBestFit)), NDC=False, textSize=0.025, halign="center", valign="bottom", textColor=color )

	container.append( (g,g_statOnly,vLineM1Sigma,vLineP1Sigma,hLine1Sigma,label1Sigma) )

	return (g,g_statOnly)


def main():
	canvas = ROOT.TCanvas("c","c",600,450)
	axes = canvas.DrawFrame( 105,0, 160,12 )
	axes.GetXaxis().SetTitle( "m_{H} [GeV]" )
	axes.GetYaxis().SetTitle( "-2 ln #Lambda" )

	hLine68 = PyROOTUtils.DrawHLine( 1.0, lineStyle=ROOT.kDashed, lineWidth=1 )
	hLine95 = PyROOTUtils.DrawHLine( 4.0, lineStyle=ROOT.kDotted, lineWidth=1 )

	g,g_statOnly = content()
	g2,g2_statOnly = content( 123.0, 8.0, ROOT.kRed )

	# create black line proxies for legend
	expectedLine = PyROOTUtils.DrawHLine( -10.0, lineWidth=2 )
	statOnlyLine = PyROOTUtils.DrawHLine( -10.0, lineWidth=2, lineStyle=ROOT.kDashed )

	l1 = PyROOTUtils.Legend( 0.94,0.5, textSize=0.035, valign="bottom", halign="right" )
	l1.AddEntry( expectedLine, "expected", "L" )
	l1.AddEntry( statOnlyLine, "stat only", "L" )
	l1.AddEntry( hLine95, "95% CL", "L" )
	l1.AddEntry( hLine68, "68% CL", "L" )
	l1.Draw()

	canvas.SaveAs( 'doc/example.svg' )
	canvas.SaveAs( 'doc/example.png' )
	canvas.SaveAs( 'doc/example.eps' )
	print( 'Image saved to doc/example.{svg|png|eps}.' )


if __name__ == "__main__":
	main()

