CMSSW_Daq_SingleMachineTest
===========================

DAQ2 F3 Single Machine Test configurations

## Get a terminal
ssh lxplus.cern.ch
bash

## Setup CMSSW
cd $(mktemp -d -p /tmp/$(whoami))
export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_0_0_pre7
cd CMSSW_7_0_0_pre7/src
cmsenv

## Get the configs
SOURCE=https://github.com/janveverka/CMSSW_Daq_SingleMachineTest.git
DESTINATION=$CMSSW_BASE/src/Daq/SingleMachineTest
git clone $SOURCE $DESTINATION

## Setup the test
## Root of the location for the file written by the BU and FU processes.
## You can customize this.
ROOT_DIR=/tmp/$(whoami)/smtest
## Customizable run number
RUN_NUMBER=100
mkdir -p $ROOT_DIR

## Run the BU process
cd $DESTINATION/test
cmsRun startBU_cfg.py runNumber=$RUN_NUMBER rootDir=$ROOT_DIR
## Kill with Ctrl-C after a while.

# Run the FU process
cd $DESTINATION/test
cmsRun startFU_cfg.py runNumber=$RUN_NUMBER rootDir=$ROOT_DIR
## You can this with Ctrl-C too.
