CMSSW_Daq_SingleMachineTest
===========================

DAQ2 F3 Single Machine Test configurations

## Get a terminal
ssh lxplus.cern.ch
bash

## Setup CMSSW
## Customizable location of the code for the test
TEST_DIR=$(mktemp -d -p /tmp/$(whoami))
cd $TEST_DIR
export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_0_0_pre7
cd CMSSW_7_0_0_pre7/src
cmsenv

## Get the configs
SOURCE=https://github.com/janveverka/CMSSW_Daq_SingleMachineTest.git
DESTINATION=$CMSSW_BASE/src/Daq/SingleMachineTest
git clone $SOURCE $DESTINATION

## Setup the test
## Root of the location for the files written by the BU and FU processes.
## You can customize this.
ROOT_DIR=$TEST_DIR
## Customizable run number
RUN_NUMBER=100
if [[ ! -d $ROOT_DIR ]]; then
	mkdir -p $ROOT_DIR
fi

## Run the BU process
cd $DESTINATION/test
cmsRun startBU_cfg.py runNumber=$RUN_NUMBER rootDir=$ROOT_DIR
## Kill with Ctrl-C after a while.

# Run the FU process
cd $DESTINATION/test
cmsRun startFU_cfg.py runNumber=$RUN_NUMBER rootDir=$ROOT_DIR
## You can this with Ctrl-C too.

# Clean up
cd
rm -rf $ROOT_DIR
rm -rf $TEST_DIR

