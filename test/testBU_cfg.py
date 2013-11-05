import getpass
import os
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from os.path import join

options = VarParsing.VarParsing ('analysis')

options.register('runNumber',
                 1, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,          # string, int, or float
                 "Run Number")

options.register('rootDir',
                 '/', # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,          # string, int, or float
                 "BU base directory")

options.parseArguments()

if not os.path.isdir(options.rootDir):
    raise RuntimeError, "Illegal path `%s'!" % options.rootDir

process = cms.Process("FAKEBU")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

process.options = cms.untracked.PSet(
    multiProcesses = cms.untracked.PSet(
        maxChildProcesses = cms.untracked.int32(0)
        )
    )
process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(threshold = cms.untracked.string( "INFO" )),
    destinations = cms.untracked.vstring( 'cout' )
    )

process.source = cms.Source("EmptySource",
     firstRun = cms.untracked.uint32(101),
     numberEventsInLuminosityBlock = cms.untracked.uint32(2000),
     numberEventsInRun = cms.untracked.uint32(0)    
    )

process.EvFDaqDirector = cms.Service("EvFDaqDirector",
    baseDir = cms.untracked.string(join(options.rootDir, "data")),
    buBaseDir = cms.untracked.string(join(options.rootDir, "data")),
    smBaseDir  = cms.untracked.string(join(options.rootDir, "sm")),
    directorIsBu = cms.untracked.bool(True),
    runNumber = cms.untracked.uint32(101)
    )

process.EvFBuildingThrottle = cms.Service("EvFBuildingThrottle",
    highWaterMark = cms.untracked.double(0.80),
    lowWaterMark = cms.untracked.double(0.45)
    )

process.a = cms.EDAnalyzer("ExceptionGenerator",
    defaultAction = cms.untracked.int32(0),
    defaultQualifier = cms.untracked.int32(5)
    )

process.s = cms.EDProducer("DaqFakeReader")

process.p = cms.Path(process.a + process.s)

process.out = cms.OutputModule("RawStreamFileWriterForBU",
    ProductLabel = cms.untracked.string("s"),
    numWriters = cms.untracked.uint32(1),
    eventBufferSize = cms.untracked.uint32(100),
    numEventsPerFile= cms.untracked.uint32(20),
    jsonDefLocation = cms.untracked.string(
        os.path.join(os.environ['CMSSW_RELEASE_BASE'],
                     'src/EventFilter/Utilities/plugins/budef.jsd')
        ),
    debug = cms.untracked.bool(True)
    )

process.ep = cms.EndPath(process.out)

