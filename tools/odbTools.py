
def getNodeSetFromSurface(odb,surface):
    if odb.rootAssembly.nodeSets.has_key(surface.name):newSet = odb.rootAssembly.nodeSets[surface.name]
    else:
        elements = surface.elements[0]
        nodes = list()
        for ele in elements:
            for label in ele.connectivity: 
                if label not in nodes:nodes.append(label)
        myNodes = tuple(nodes)
        newSet = odb.rootAssembly.NodeSetFromNodeLabels(name = surface.name, nodeLabels = ((elements[0].instanceName,myNodes),))
    return newSet
#-----------------------------------------------------
def computeMeanOverElement(fieldValues):
    if (len(fieldValues)%4):
        print 'wrong field value or nb of IP/nodes per element'
        return
    newFieldValue = list()
    for n in range(0,len(fieldValues)-1,4):
        newFieldValue.append(sum(fieldValues[n:n+4])/4.)
    return newFieldValue
#-----------------------------------------------------
def openOdb(odbName):
    if not odbName.endswith('.odb'):odbName+='.odb'
    import odbAccess
    return odbAccess.openOdb(path=odbName)
#-----------------------------------------------------
def writeValuesOpti(valueList):
    import os
    datFile = open('output.ascii', 'w')
    try:
        for x,y in valueList:
            datFile.write( "%f %f\n" % (x,y) )
    except(TypeError): #there is shorter than that but can't be bothered!!!
        try:
            for value in valueList:
                datFile.write( "%f\n" % value)
        except(TypeError):datFile.write( "%f\n" % valueList)
    datFile.close()
#-----------------------------------------------------
def writeValues(listDict):
    import os
    for key in listDict.keys():
        datFile = open(key+'.ascii', 'w')
        try:
            for value in listDict[key]:
                try:
                    datFile.writelines( "%f " % item for item in value )
                    datFile.writelines( "\n" )
                except(TypeError):
                    datFile.writelines( "%f\n" % value ) 
        except(TypeError):
            value = listDict[key]
            try:
                datFile.writelines( "%f " % item for item in value )
                datFile.writelines( "\n" )
            except(TypeError):
                datFile.writelines( "%f\n" % value ) 
        datFile.close()

