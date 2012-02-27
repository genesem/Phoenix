#---------------------------------------------------------------------------
# Name:        etg/filesys.py
# Author:      Robin Dunn
#
# Created:     25-Feb-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "filesys"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "wxFileSystem",
           "wxFSFile",
           "wxFileSystemHandler",
           "wxMemoryFSHandler",
           "wxArchiveFSHandler",
           "wxFilterFSHandler",
           "wxInternetFSHandler",
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxFileSystem')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.find('AddHandler.handler').transfer = True
    c.find('RemoveHandler').transferBack = True

    m = c.find('URLToFileName')
    m.type = 'wxString'
    m.setCppCode("""\
        wxFileName fname = wxFileSystem::URLToFileName(*url);
        return new wxString(fname.GetFullPath());       
        """)

    fileNameTypedef = etgtools.TypedefDef(type='wxString', name='wxFileName', noTypeName=True)
    module.insertItemBefore(c, fileNameTypedef)
    
    c = module.find('wxArchiveFSHandler')
    c.addPrivateCopyCtor();
    module.addPyCode('ZipFSHandler = wx.deprecated(ArchiveFSHandler)')
    
    c = module.find('wxFSFile')
    c.addPrivateCopyCtor();
    
    c = module.find('wxFilterFSHandler')
    c.addPrivateCopyCtor();
    
    c = module.find('wxInternetFSHandler')
    c.addPrivateCopyCtor();
    

    c = module.find('wxMemoryFSHandler')
    c.addPrivateCopyCtor();
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

