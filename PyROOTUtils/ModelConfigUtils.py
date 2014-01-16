
import ROOT

def addOptionsToOptParse( parser ):
   # standard options for ModelConfig
   parser.add_option("-i", "--input", help="root file", type="string", dest="input", default="results/example_combined_GaussExample_model.root")
   parser.add_option("-w", "--wsName", help="Workspace name", type="string", dest="wsName", default="combined")
   parser.add_option("-m", "--mcName", help="ModelConfig name", type="string", dest="mcName", default="ModelConfig")
   parser.add_option("-d", "--dataName", help="data name", type="string", dest="dataName", default="obsData")
   
   # for example for asimov data runs
   parser.add_option(      "--loadSnapshots", help="loads this comma separated list of snapshots", dest="loadSnapshots", default=None )

   # for modifications
   parser.add_option(      "--setConstant", help="Set comma separated list of parameters to constant. Example: \"mu=1,mH=125\".", dest="setConstant", default=False )   
   parser.add_option(      "--setFloating", help="Set comma separated list of parameters to floating. Example: \"mu=1,mH=125\".", dest="setFloating", default=False )   
   parser.add_option(      "--overwritePOI", help="Force to take comma separated list of parameters with value for poi. Example: \"mu=1,mH=125\" will make these two the poi.", dest="overwritePOI", default=False )
   parser.add_option(      "--overwriteRange", help="Overwrite range. Example: \"mu=[-5:10],mH=[120:130]\".", dest="overwriteRange", default=False )
   parser.add_option(      "--overwriteBins", help="Overwrite bins. Example: \"mu=5,mH=100\".", dest="overwriteBins", default=False )
   
   # for plugins
   parser.add_option(      "--plugins", help="comma separated list of plugins", dest="plugins", default=None )



def varsDictFromString( str ):
   """ Helper function to make a dictionary from an options string. """
   
   vars = str.split(",")
   vars = dict(   (v.split("=")[0].strip(), v.split("=")[1]) for v in vars   )
   for name,valErr in vars.iteritems():
      if "+/-" in valErr:
         vars[ name ] = (   float( valErr.split("+/-")[0] ),float( valErr.split("+/-")[1] )   )
      else:
         vars[ name ] = (   float( valErr ), None    )
   return vars


def callHooks( options, f,w,mc,data, type ):
   if not options.plugins: return (f,w,mc,data)
   
   print( "" )

   for pName in options.plugins.split(","):
      try:
         plugin = __import__( pName )
         if hasattr( plugin,type ):
            print( '--- Plugin "'+pName+'": '+type+'() ---' )
            r = getattr( plugin,type )( f,w,mc,data )
            if r: f,w,mc,data = r
         else:
            print( '--- Plugin "'+pName+'" does not contain '+type+'() ---' )
      except ImportError:
         print( "ERROR: Did not find plugin: "+str(pName) )

   print( "" )
   return (f,w,mc,data)



def apply( options, f,w,mc,data ):
   """ Todo: use varsDictFromString() here. """

   f,w,mc,data = callHooks( options, f,w,mc,data, type="preprocess" )

   if options.overwriteRange:
      parAndRange = options.overwriteRange.split(",")
      for pr in parAndRange:
         p,r = pr.split("=")
         r = r.split(":")
         rMin = float( r[0][1:] )
         rMax = float( r[1][:-1] )
         
         print( "Setting range for "+p+"=["+str(rMin)+","+str(rMax)+"]" )
         w.var( p ).setRange( rMin, rMax )

   if options.overwriteBins:
      parAndBins = options.overwriteBins.split(",")
      for pb in parAndBins:
         p,b = pb.split("=")
         print( "Setting number of bins for "+p+"="+str(b) )
         w.var( p ).setBins( int(b) )

   if options.setConstant:
      parAndValue = options.setConstant.split(",")
      for pv in parAndValue:
         name,value = pv.split("=")
         if w.var(name):
            w.var(name).setVal( float(value) )
            w.var(name).setConstant()
            print( "Variable "+name+" set constant at value "+str(value)+"." )
         else:
            print( "Variable "+name+" not found and not set constant." )

   if options.setFloating:
      parAndValue = options.setFloating.split(",")
      for pv in parAndValue:
         name,value = pv.split("=")
         if w.var(name):
            w.var(name).setVal( float(value) )
            w.var(name).setConstant(False)
            print( "Variable "+name+" set floating with initial value "+str(value)+"." )
         else:
            print( "Variable "+name+" not found and not set floating." )

   if options.overwritePOI:
      print( "" )
      print( "=== Using given set for POI ===" )
      poiAndValue = {}
      pvs = options.overwritePOI.split(",")
      for pv in pvs:
         name,value = pv.split("=")
         poiAndValue[ name ] = float( value )
      
      remove = []
      poiL = ROOT.RooArgList( mc.GetParametersOfInterest() )
      for p in range( poiL.getSize() ):
         name = poiL.at(p).GetName()
         if name not in poiAndValue.keys():
            print( "Adding "+name+"["+str(poiL.at(p).getMin())+","+str(poiL.at(p).getMax())+"]="+str(poiL.at(p).getVal())+{True:' C', False:''}[poiL.at(p).isConstant()]+" to nuisance parameters." )
            w.set( mc.GetName()+"_NuisParams" ).add( poiL.at(p) )
            remove.append( name )
#          else:
#             print( "Setting value of POI "+name+"="+str(poiAndValue[name])+"." )

      for r in remove: poiL.remove( w.var(r) )
            
      for p,v in poiAndValue.iteritems():
         if not poiL.contains( w.var(p) ):
            print( "Adding "+p+"="+str(v)+" to POI." )
            poiL.add( w.var(p) )
            w.var(p).setVal( v )
         else:
            print( "Setting value of POI "+p+"="+str(v)+"." )
            w.var(p).setVal( v )
         
         if mc.GetNuisanceParameters().contains( w.var(p) ):
            print( "Removing "+w.var(p).GetName()+" from the list of nuisance parameters." )
            mc.GetNuisanceParameters().remove( w.var(p) )
            
      print( "Setting new POI and new snapshot for ModelConfig: " )
      mc.SetParametersOfInterest( ROOT.RooArgSet(poiL) )
      mc.SetSnapshot( ROOT.RooArgSet(poiL) )
      mc.GetSnapshot().Print("V")
      print( "" )
      print( "" )
      
   if options.loadSnapshots:
      sn = options.loadSnapshots.split(",")
      for s in sn:
         print( "Loading snapshot "+s+" ..." )
         w.loadSnapshot( s )
         print( "done." )
               
   return (f,w,mc,data)
      

