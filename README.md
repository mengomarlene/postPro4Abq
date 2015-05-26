# postPro4Abq
Scripts to read and process an odb file.
./tools contains the python scripts and classes
./tests shows an example with a generic function (in module FSUPostPro) being called from a python script (FSU2615IsoPostpro.py)

usage
=====
example can be found in ./tests (it works with an odb file NOT commited!!)
in a python file (myPostProFile.py), define the path to an odb and call an extractor function from the extractors module or the contactExtractors module
the odbTools module contains functions to write the extracted values to files

the relative path of the folder in which the tools directory is must be available in your sys.path (as done for example in FSUPostPro.py)

in abaqus cae run the script by "File->run script" browse for myPostProFile.py
in command line run "abaqus python myPostProFile.py"

list of scripts and classes
===========================

valueExtractorClass.py: contains the main classes for generic value extractors and contact value extractors.
    
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

extractor.py: defines specific extractors using the ValueExtractor class

contactExtractors.py: defines specific extractors using the ContactValueExtractor class

odbTools.py: generic tools to open odb and write outputs

