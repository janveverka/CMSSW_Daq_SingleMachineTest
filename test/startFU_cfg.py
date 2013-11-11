# -*- coding: utf-8 -*-
## Inspired by dvfu-c2f37-32-02:/opt/hltd/python/testFU_cfg1.py
import os
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from os.path import join

release_base = os.environ['CMSSW_RELEASE_BASE']

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
                 "Root of other used directories, which are relative to this")

options.parseArguments()

process = cms.Process("TESTFU")
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

process.FastMonitoringService = cms.Service("FastMonitoringService",
    sleepTime = cms.untracked.int32(1),
    microstateDefPath = cms.untracked.string(
        join(release_base, 
             'src/EventFilter/Utilities/plugins/microstatedef.jsd')
        ),
    outputDefPath = cms.untracked.string(
        join(release_base,
             'src/EventFilter/Utilities/plugins/output.jsd' )
        ),
    fastName = cms.untracked.string('fastmoni'),
    slowName = cms.untracked.string('slowmoni')
    )

process.EvFDaqDirector = cms.Service("EvFDaqDirector",
    baseDir = cms.untracked.string(join(options.rootDir, "FU/data")),
    buBaseDir = cms.untracked.string(join(options.rootDir, "BU/data")),
    smBaseDir  = cms.untracked.string(join(options.rootDir, "sm")),
    directorIsBu = cms.untracked.bool(False),
    runNumber = cms.untracked.uint32(options.runNumber)
    )

process.PrescaleService = cms.Service("PrescaleService",
    lvl1DefaultLabel = cms.string( "B" ),
    lvl1Labels = cms.vstring('A', 'B'),
    prescaleTable = cms.VPSet(
        cms.PSet(pathName = cms.string( "p1" ),
                 prescales = cms.vuint32( 0, 10)),
        cms.PSet(pathName = cms.string( "p2" ),
                 prescales = cms.vuint32( 0, 100)),
        )
    )


process.source = cms.Source("FedRawDataInputSource",
    getLSFromFilename = cms.untracked.bool(True),
    eventChunkSize = cms.untracked.uint32(16),
    runNumber = cms.untracked.uint32(options.runNumber)
    )


process.filter1 = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag( "hltGtDigis" )
    )

process.filter2 = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag( "hltGtDigis" )
    )

process.a = cms.EDAnalyzer("ExceptionGenerator",
    defaultAction = cms.untracked.int32(0),
    defaultQualifier = cms.untracked.int32(60)
    )

process.b = cms.EDAnalyzer("ExceptionGenerator",
    defaultAction = cms.untracked.int32(0),
    defaultQualifier = cms.untracked.int32(60)
    )

process.p1 = cms.Path(process.a * process.filter1)
process.p2 = cms.Path(process.b * process.filter2)


process.streamA = cms.OutputModule("Stream",
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p1'))
    )

process.streamB = cms.OutputModule("Stream",
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p2'))
    )
                                   
process.ep = cms.EndPath(process.streamA + process.streamB)



