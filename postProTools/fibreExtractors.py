import postProTools.extractors as ext
import postProTools.odbTools as odbTools
import postProTools.valueExtractorClass as valueExtractor
import math
import numpy as np
import numpy.linalg as linalg
#
#-----------------------------------------------------
# LOCAL DIRECTIONS
#-----------------------------------------------------
def getFinalLD_1(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LOCALDIR1')
    values.setComponent('LOCALDIR1_1')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
def getFinalLD_2(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LOCALDIR1')
    values.setComponent('LOCALDIR1_2')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
def getFinalLD_3(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LOCALDIR1')
    values.setComponent('LOCALDIR1_3')
    values.setCoordSystem(sysC)
    return values.getFinalValue_ElementNodal()
def getLD_1(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LOCALDIR1')
    values.setComponent('LOCALDIR1_1')
    values.setCoordSystem(sysC)
    return values.getEvolution_ElementNodal()
def getLD_2(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LOCALDIR1')
    values.setComponent('LOCALDIR1_2')
    values.setCoordSystem(sysC)
    return values.getEvolution_ElementNodal()
def getLD_3(odb,setName,sysC=None):
    values = valueExtractor.ValueExtractor(odb,setName)
    values.setField('LOCALDIR1')
    values.setComponent('LOCALDIR1_3')
    values.setCoordSystem(sysC)
    return values.getEvolution_ElementNodal()
#-----------------------------------------------------
def getFinalFiberDirection(odb,setName,sysC,tetMesh=False):
    if tetMesh:
        LD1 = getFinalLD_1(odb,setName,sysC)
        LD2 = getFinalLD_2(odb,setName,sysC)
        LD3 = getFinalLD_3(odb,setName,sysC)
    else:
        LD1 = odbTools.computeMeanOverElement(getFinalLD_1(odb,setName,sysC))
        LD2 = odbTools.computeMeanOverElement(getFinalLD_2(odb,setName,sysC))
        LD3 = odbTools.computeMeanOverElement(getFinalLD_3(odb,setName,sysC))
    nbNodes = len(LD3)
    fiberDirectionVector = np.empty((3,nbNodes))
    fiberDirectionVector[0,:] = LD1
    fiberDirectionVector[1,:] = LD2
    fiberDirectionVector[2,:] = LD3
    return fiberDirectionVector
#-----------------------------------------------------
def getFinalLogStrain(odb,setName,sysC,tetMesh=False):
    if tetMesh:
        E11 = ext.getFinalE_11(odb,setName,sysC)
        E22 = ext.getFinalE_22(odb,setName,sysC)
        E33 = ext.getFinalE_33(odb,setName,sysC)
        E12 = ext.getFinalE_12(odb,setName,sysC)
        E13 = ext.getFinalE_13(odb,setName,sysC)
        E23 = ext.getFinalE_23(odb,setName,sysC)
    else:
        E11 = odbTools.computeMeanOverElement(ext.getFinalE_11(odb,setName,sysC))
        E22 = odbTools.computeMeanOverElement(ext.getFinalE_22(odb,setName,sysC))
        E33 = odbTools.computeMeanOverElement(ext.getFinalE_33(odb,setName,sysC))
        E12 = odbTools.computeMeanOverElement(ext.getFinalE_12(odb,setName,sysC))
        E13 = odbTools.computeMeanOverElement(ext.getFinalE_13(odb,setName,sysC))
        E23 = odbTools.computeMeanOverElement(ext.getFinalE_23(odb,setName,sysC))
    nbNodes = len(E23)
    strainTensor = np.empty((3,3,nbNodes))
    strainTensor[0,0,] = E11
    strainTensor[1,1,] = E22
    strainTensor[2,2,] = E33
    strainTensor[0,1,] = E12
    strainTensor[0,2,] = E13
    strainTensor[1,2,] = E23
    strainTensor[1,0,] = E12
    strainTensor[2,0,] = E13
    strainTensor[2,1,] = E23
    return strainTensor
#-----------------------------------------------------
def getInvLeftCauchyGreen(strainTensorV):
    '''
    return B-1=V^-2 from V
    '''
    Bm1 = np.empty((3,3,int(strainTensorV.shape[2])))
    for node in range(int(strainTensorV.shape[2])):
        B = np.dot(strainTensorV[:,:,node],strainTensorV[:,:,node]) 
        Bm1[:,:,node] = linalg.inv(B)
    return Bm1
#-----------------------------------------------------
def getStrainV(logStrainV):
    '''
    return V from logV
    '''
    V = np.empty((3,3,int(logStrainV.shape[2])))
    for node in range(int(logStrainV.shape[2])):
        w,v = linalg.eig(logStrainV[:,:,node])
        ew = np.exp(w)
        V[:,:,node] = ew*np.inner(v,v)
    return V
#-----------------------------------------------------
#-----------------------------------------------------
def computeFiberStretchQuadMesh(odb,setName,sysC):
    direction = getFinalFiberDirection(odb,setName,sysC)#a vector (for each node)
    logVstrain = getFinalLogStrain(odb,setName,sysC)# a tensor (for each node)
    strainV = getStrainV(logVstrain)
    invLCG = getInvLeftCauchyGreen(strainV)
    stretch = list()
    for node in range(int(direction.shape[1])):
        invSquareStretch = np.dot(direction[:,node],np.dot(invLCG[:,:,node],direction[:,node]))
        stretch.append(math.sqrt(1./invSquareStretch))
    return stretch
#-----------------------------------------------------
def computeFiberStretchTetMesh(odb,setName,sysC):
    direction = getFinalFiberDirection(odb,setName,sysC,tetMesh=True)#a vector (for each node)
    logVstrain = getFinalLogStrain(odb,setName,sysC,tetMesh=True)# a tensor (for each node)
    strainV = getStrainV(logVstrain)
    invLCG = getInvLeftCauchyGreen(strainV)
    stretch = list()
    for node in range(int(direction.shape[1])):
        invSquareStretch = np.dot(direction[:,node],np.dot(invLCG[:,:,node],direction[:,node]))
        stretch.append(math.sqrt(1./invSquareStretch))
    return stretch