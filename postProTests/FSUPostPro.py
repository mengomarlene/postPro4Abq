import sys,os
thisDir = os.path.dirname(__file__)
toolsDir = os.path.join(os.path.dirname(thisDir), 'tools')
sys.path.append(os.path.dirname(thisDir))

def postPro(odbName):
    print 'running postPro on ',odbName
    import tools.odbTools as odbTools
    import tools.extractors as ext
    import tools.contactExtractors as cExt
    valuesToWrite = dict()
    myOdb = odbTools.openOdb(odbName)
    fileName = odbName.split('.')[0]
    valuesToWrite['axialDispl_%s'%fileName] = ext.getU_3(myOdb, 'TOPPLATE')
    valuesToWrite['force_%s'%fileName] = ext.getRF_3(myOdb,'TOPPLATE')
    
    try:
        masterName = 'CP-2-bot'
        slaveName = 'CP-2-PART-1-1'   
        valuesToWrite['cForce1_%s'%fileName] = cExt.getCNormalForce_Magnitude(myOdb,masterName,slaveName)
        
        masterName = 'CP-3-bot'
        slaveName = 'CP-3-PART-1-1'   
        valuesToWrite['cForce2_%s'%fileName] = cExt.getCNormalForce_Magnitude(myOdb,masterName,slaveName)
    except:
        masterName = 'topCartilage1'
        slaveName = 'botCartilage1'   
        valuesToWrite['cForce1_%s'%fileName] = cExt.getCNormalForce_Magnitude(myOdb,masterName,slaveName)
        
        masterName = 'topCartilage2'
        slaveName = 'botCartilage2'   
        valuesToWrite['cForce2_%s'%fileName] = cExt.getCNormalForce_Magnitude(myOdb,masterName,slaveName)

    odbTools.writeValues(valuesToWrite)
    print 'postPro on ',odbName, ': DONE'
    myOdb.close()
