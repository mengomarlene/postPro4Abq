import postProTools.valueExtractorClass as valueExtractor
#fieldOutputs.keys = 
# 'LE' (log eulerian strain ln(V)),'LOCALDIR1','RT','S','U','DG' (deformation gradient)
#  !!'P' = Uniformly distributed pressure load on element faces
# thisOdb = session.viewports['Viewport: 1'].displayedObject
#-----------------------------------------------------
def getTime(odb):
    stepName = odb.steps.keys()[-1]
    frames = odb.steps[stepName].frames
    time = list()
    for frame in frames: time.append(frame.frameValue)
    return time
#-----------------------------------------------------
def getNCoord(odb, setName, sysC=None):
    '''
    gives initial coordinates of nodes
    '''
    initialCoords = list()
    try:
        if 'INSTANCE'  in setName:
            iName = setName.split('.')[0]
            iSetName = setName.split('.')[1]
            try:
                set = odb.rootAssembly.instances[iName].nodeSets[iSetName]
            except:
                set = odb.rootAssembly.instances[iName].nodeSets[iSetName.upper()]
            nodes = set.nodes#??[0]
            for node in nodes:
                initialCoords.append(getNodeCoord(node, sysC=sysC))
        else:
            try:
                set = odb.rootAssembly.nodeSets[setName]#setName is a string
            except:
                set = odb.rootAssembly.nodeSets[setName.upper()]#setName is a string
            nodes = set.nodes
            for part in range(len(set.nodes)): # nb of part in the nodeSet != total nb of parts!!
                for node in nodes[part]:
                    initialCoords.append(getNodeCoord(node, sysC=sysC))
    except:
        nodes = setName.nodes[0]
        for node in nodes: initialCoords.append(getNodeCoord(node, sysC=sysC))
    return initialCoords
#-----------------------------------------------------
def getNodeCoord(node, sysC=None):  
    coord0 = node.coordinates
    if sysC is not None:#assuming z is Z
        import math
        if sysC.name == 'cylXY':
            R = math.sqrt(coord0[0]*coord0[0]+coord0[1]*coord0[1])
            theta = math.atan2(coord0[1],coord0[0])
            Z = coord0[2]
            return (R, theta, Z)
        elif sysC.name == 'cylXZ':
            R = math.sqrt(coord0[0]*coord0[0]+coord0[2]*coord0[2])
            theta = math.atan2(coord0[2],coord0[0])
            Z = coord0[1]
            return (R, theta, Z)
        else:
            origin = sysC.origin
            x = coord0[0]-origin[0]
            y = coord0[1]-origin[1]
            R = math.sqrt(x*x+y*y)
            theta = math.atan2(y,x)
            Z = coord0[2]-origin[2]
            return (R, theta, Z)
    else:
        return (coord0[0], coord0[1], coord0[2])
#-----------------------------------------------------
# DISPLACEMENTS
#-----------------------------------------------------
def getU(odb,setName,sysC=None):
    try:
        try:
            nod = odb.rootAssembly.nodeSets[setName].nodes[0]
        except:
            nod = odb.rootAssembly.nodeSets[setName.upper()].nodes[0]
    except:
        nod = setName.nodes[0]
    if len(nod) == 1: 
        values = valueExtractor.ValueExtractor(odb,setName)
        values.setField('U')
        values.setCoordSystem(sysC)
        return values.getEvolution_Nodal()
    else:raise Exception("getU to be used only if the set contains 1! node")
#-----------------------------------------------------
def getU_Magnitude(odb,setName,sysC=None):
    from abaqusConstants import MAGNITUDE
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setInvariant(MAGNITUDE)
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getU_1(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setComponent('U1')
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getU_2(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setComponent('U2')
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getU_3(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setComponent('U3')
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getFinalU(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getFinalU_Magnitude(odb,setName,sysC=None):
    from abaqusConstants import MAGNITUDE
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setInvariant(MAGNITUDE)
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getFinalU_1(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setComponent('U1')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getFinalU_2(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setComponent('U2')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getFinalU_3(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('U')
    values.setComponent('U3')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
# REACTION FORCES
#-----------------------------------------------------
def getFinalRF(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getFinalRF_1(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setComponent('RF1')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getFinalRF_2(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setComponent('RF2')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getFinalRF_3(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setComponent('RF3')
    values.setCoordSystem(sysC)
    return values.getFinalValue_Nodal()
#-----------------------------------------------------
def getRF_Magnitude(odb,setName,sysC=None):
    from abaqusConstants import MAGNITUDE
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setInvariant(MAGNITUDE)
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getRF_1(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setComponent('RF1')
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getRF_2(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setComponent('RF2')
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getRF_3(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('RF')
    values.setComponent('RF3')
    values.setCoordSystem(sysC)
    return values.getEvolution_Nodal()
#-----------------------------------------------------
def getResF(odb,setName,sysC=None):
    r1 = getRF_1(odb, setName, sysC)
    r2 = getRF_2(odb, setName, sysC)
    r3 = getRF_3(odb, setName, sysC)
    resForce = list()
    for frame in range(len(r1)):
        resForce.append([sum(r1[frame]),sum(r2[frame]),sum(r3[frame])])
    return resForce
#-----------------------------------------------------
def getResF_1(odb,setName,sysC=None):
    r1 = getRF_1(odb, setName, sysC)
    resForce = [sum(value) for value in r1]
    return resForce
#-----------------------------------------------------
def getResF_2(odb,setName,sysC=None):
    r2 = getRF_2(odb, setName, sysC)
    resForce = [sum(value) for value in r2]
    return resForce
#-----------------------------------------------------
def getResF_3(odb,setName,sysC=None):
    r3 = getRF_3(odb, setName, sysC)
    resForce = [sum(value) for value in r3]
    return resForce
#-----------------------------------------------------
def getResF2D(odb,setName,sysC=None):
    r1 = getRF_1(odb, setName, sysC)
    r2 = getRF_2(odb, setName, sysC)
    resForce = list()
    for frame in range(len(r1)):
        resForce.append([sum(r1[frame]),sum(r2[frame])])
    return resForce
#-----------------------------------------------------
def getFinalResF(odb,setName,sysC=None):
    r1 = getFinalRF_1(odb, setName, sysC)
    r2 = getFinalRF_2(odb, setName, sysC)
    r3 = getFinalRF_3(odb, setName, sysC)
    resForce = [sum(r1),sum(r2),sum(r3)]
    return resForce
#-----------------------------------------------------
def getFinalResF_1(odb,setName,sysC=None):
    r1 = getFinalRF_1(odb, setName, sysC)
    resForce = sum(r1)
    return resForce
#-----------------------------------------------------
def getFinalResF_2(odb,setName,sysC=None):
    r2 = getFinalRF_2(odb, setName, sysC)
    resForce = sum(r2)
    return resForce
#-----------------------------------------------------
def getFinalResF_3(odb,setName,sysC=None):
    r3 = getFinalRF_3(odb, setName, sysC)
    resForce = sum(r3)
    return resForce
#-----------------------------------------------------
def getFinalResF2D(odb,setName,sysC=None):
    r1 = getFinalRF_1(odb, setName, sysC)
    r2 = getFinalRF_2(odb, setName, sysC)
    resForce [sum(r1),sum(r2)]
    return resForce
#-----------------------------------------------------
# STRESSES
#-----------------------------------------------------
def getFinalS(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('S')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalS_13(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('S')
    values.setComponent('S33')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalS_23(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('S')
    values.setComponent('S33')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalS_33(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('S')
    values.setComponent('S33')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getS_11(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('S')
    values.setComponent('S11')
    values.setCoordSystem(sysC)
    return values.getEvolution_ElementNodal()
#-----------------------------------------------------
def getS_VM(odb,setName,sysC=None):
    from abaqusConstants import MISES
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('S')
    values.setInvariant(MISES)
    values.setCoordSystem(sysC)
    return values.getEvolution_ElementNodal()
#-----------------------------------------------------
# STRAINS
#-----------------------------------------------------
def getFinalE_11(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setComponent('LE11')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalE_22(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setComponent('LE22')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalE_33(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setComponent('LE33')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalE_12(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setComponent('LE12')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalE_13(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setComponent('LE13')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getFinalE_23(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setComponent('LE23')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
#-----------------------------------------------------
def getE_11(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setComponent('LE11')
    values.setCoordSystem(sysC)
    return values.getEvolution_ElementNodal()
#-----------------------------------------------------
def getE_VM(odb,setName,sysC=None):
    from abaqusConstants import MISES
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LE')
    values.setInvariant(MISES)
    values.setCoordSystem(sysC)
    return values.getEvolution_ElementNodal()
#-----------------------------------------------------