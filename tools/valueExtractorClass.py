class ValueExtractor:
    """Class ValueExtractor - extract odb values on a set
    ValueExtractor(odb,set)#set can be a string or a set object
    Methods:
        setField(fieldKey) - the field to extract, default is displacement
        setComponent(componentLabel) - the field component, no default
        setInvariant(invariant) - the field invariant, no default
        setCoordSystem(sysC) - a coordinate system (sysC is a datum) in which the field is extracted, default is cartesian

        getEvolution_Nodal()
        getEvolution_ElementNodal()
        getEvolution_ElementIP()
        getFinalValue_Nodal()
        getFinalValue_ElementNodal()
        getFinalValue_ElementIP()
    """
    def __init__(self,odb,setName):
        self.odb = odb
        self.setName = setName#either a string or a set object
        self.fieldKey = 'U'
        self.componentLabel = None
        self.invariant = None
        self.sysC = None
        self.stepName = None
    #-----------------------------------------------------
    def setField(self,fieldKey):
        self.fieldKey = fieldKey
    def setComponent(self,componentLabel):
        self.componentLabel = componentLabel
    def setInvariant(self,invariant):
        self.invariant = invariant
    def setCoordSystem(self,sysC):
        self.sysC = sysC#a datum 
    def setStepName(self,stepName):
        self.stepName = stepName
    #-----------------------------------------------------
    def getEvolution_Nodal(self):
        return self.__getEvolution()
    def getEvolution_ElementNodal(self):
        return self.__getEvolution(position='EL_N')
    def getEvolution_ElementIP(self):
        return self.__getEvolution(position='EL_IP')
    def getFinalValue_Nodal(self):
        return self.__getFinalValue()
    def getFinalValue_ElementNodal(self):
        return self.__getFinalValue(position='EL_N')
    def getFinalValue_ElementIP(self):
        return self.__getFinalValue(position='EL_IP')
    #-----------------------------------------------------
    #-----------------------------------------------------
    def __getEvolution(self,position=None):
        if self.stepName is None:self.stepName = self.odb.steps.keys()[-1]
        frames = self.odb.steps[self.stepName].frames
        values = self.__getValues(frameNo=frames,position=position)
        value = list()
        for frame in range(len(frames)):
            try: value.append([ptValue.data for ptValue in values[frame]])
            except: value.append([data for data in values[frame]])
        return value
    #-----------------------------------------------------
    def __getFinalValue(self,position=None):
        if self.stepName is None:self.stepName = self.odb.steps.keys()[-1]
        values = self.__getValues(position=position)
        return values
    #-----------------------------------------------------
    def __getValues(self,frameNo=-1,position=None):
        try:
           value = [self.__getValues(frameNb,position) for frameNb in range(len(frameNo))]
        except(TypeError):
            frame = self.odb.steps[self.stepName].frames[frameNo]#
            theField = frame.fieldOutputs[self.fieldKey]
            if self.sysC is not None:
                theField = theField.getTransformedField(datumCsys=self.sysC)
            if self.componentLabel is not None:theField = theField.getScalarField(componentLabel=self.componentLabel)
            elif self.invariant is not None:theField = theField.getScalarField(invariant=self.invariant)
            try:#setName is a string
                assembly = self.odb.rootAssembly
                if 'INSTANCE'  in self.setName:#set name is a part set
                    iName = self.setName.split('.')[0]
                    iSetName = self.setName.split('.')[1]
                    try:
                        subset = assembly.instances[iName].nodeSets[iSetName]
                    except:
                        subset = assembly.instances[iName].nodeSets[iSetName.upper()]
                else:#set name is an assembly set
                    try:
                        subset = assembly.nodeSets[self.setName]
                    except:
                        subset = assembly.nodeSets[self.setName.upper()]
            except(TypeError):#setName is a set object
                subset = self.setName
            if position == 'EL_IP':
                from abaqusConstants import INTEGRATION_POINT
                theFieldOnSet = theField.getSubset(region=subset,position=INTEGRATION_POINT)
                value = [ptValue.data for ptValue in theFieldOnSet.values]
            elif position == 'EL_N':
                from abaqusConstants import ELEMENT_NODAL
                theFieldOnSet = theField.getSubset(region=subset,position=ELEMENT_NODAL)
                value = [ptValue.data for ptValue in theFieldOnSet.values]
            else:# nodal field
                value = list()
                theFieldOnSet = theField.getSubset(region=subset)
                value = [ptValue.data for ptValue in theFieldOnSet.values]
                #if len(subset.nodes) >1: value = [ptValue.data for ptValue in theFieldOnSet.values]
                #else: value.append(theFieldOnSet.values[0].data)
        return value

class ContactValueExtractor:
    """Class ContactValueExtractor - extract odb contact values on a contact pair
    ContactValueExtractor(odb,masterSurf,slaveSurf)#masterSurf,slaveSurf can be strings or a surface objects
    Methods:
        setField(fieldKey) - the field to extract (default COPEN)
        setComponent(componentLabel) - abaqus componentLabel (default None)
        setInvariant(invariant) - abaqus invariant (default None)
        setCoordSystem(sysC) - sysC is a datum coordinate system (default None)
        setStepName(name) - if None (default) then uses the last step is the last one
        
        getEvolution()
        getFinalValue()
    """
    def __init__(self,odb,masterSurf,slaveSurf):
        self.odb = odb
        self.master = masterSurf#either a string or a set object
        self.slave = slaveSurf#either a string or a set object
        self.fieldKey = 'COPEN'
        self.componentLabel = None
        self.invariant = None
        self.sysC = None
        self.stepName = None
    #-----------------------------------------------------
    def setField(self,fieldKey):
        self.fieldKey = fieldKey
    def setComponent(self,componentLabel):
        self.componentLabel = componentLabel
    def setInvariant(self,invariant):
        self.invariant = invariant
    def setCoordSystem(self,sysC):
        self.sysC = sysC#a datum 
    def setStepName(self,stepName):
        self.stepName = stepName
    #-----------------------------------------------------
    #-----------------------------------------------------
    def getEvolution(self):
        if self.stepName is None:self.stepName = self.odb.steps.keys()[-1]
        frames = self.odb.steps[self.stepName].frames
        values = self.__getContactValues(frameNo=frames)
        value = list()
        for frame in range(len(frames)):
            value.append([data for data in values[frame]])
        return value
    #-----------------------------------------------------
    def getFinalValue(self):
        if self.stepName is None:self.stepName = self.odb.steps.keys()[-1]
        values = self.__getContactValues()
        return values
#-----------------------------------------------------
    def __getContactValues(self,frameNo=-1):
        try:
            value = [self.__getContactValues(frameNb) for frameNb in range(len(frameNo))]
        except(TypeError):
            frame = self.odb.steps[self.stepName].frames[frameNo]
            fieldName = self.fieldKey+' '*(9-len(self.fieldKey))
            try:#setName is a string
                assembly = self.odb.rootAssembly
                if ('INSTANCE'  in self.master) and ('INSTANCE' in self.slave):#surface name are part surfaces
                    iName = self.master.split('.')[0]
                    iSetName = self.master.split('.')[1]
                    try:
                        masterSurf = assembly.instances[iName].surfaces[iSetName]
                        slaveSurf = assembly.instances[iName].surfaces[iSetName]
                    except:
                        masterSurf = assembly.instances[iName].nodeSets[iSetName.upper()]
                        slaveSurf = assembly.instances[iName].nodeSets[iSetName.upper()]
                else:#surfaces names are assembly surfaces
                    try:
                        masterSurf = assembly.surfaces[self.master.upper()]
                        slaveSurf = assembly.surfaces[self.slave.upper()]
                        masterName = 'ASSEMBLY_'+self.master.upper()
                        slaveName = 'ASSEMBLY_'+self.slave.upper()
                    except(KeyError):
						#print assembly.surfaces,self.master,self.slave
						raise Exception("unknown master/slave surface names")
            except(TypeError):#surfaces are object
				masterName = 'ASSEMBLY_'+self.master.name
				slaveName = 'ASSEMBLY_'+self.slave.name
            fieldName += slaveName+'/'+masterName
            theField = frame.fieldOutputs[fieldName]
            if self.sysC is not None:
                theField = theField.getTransformedField(datumCsys=self.sysC)
            if self.componentLabel is not None:theField = theField.getScalarField(componentLabel=self.componentLabel)
            elif self.invariant is not None:theField = theField.getScalarField(invariant=self.invariant)
            value = [ptValue.data for ptValue in theField.values]
        return value