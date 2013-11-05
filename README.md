CMSSW_Daq_SingleMachineTest
===========================

This project contains the DAQ2 F3 Single Machine Test configurations.

Follow these instructions to run the F3 single machine test.

1.  Get a terminal on a machine running SLC6 and with enough HDD

        ssh lxplus.cern.ch
        df /tmp

    The output should look something like this:

        Filesystem           1K-blocks      Used Available Use% Mounted on
        /dev/vdb             165139820  96397804  60353408  62% /tmp

    Here, 62% of the device containing the `\tmp` directory is used.  *To run this test, you need to use a device, which is less than 80% used.  If `Use%` is more than `80%` for you, logout from this node and login to a different one.*  See the item "*Setup the test*" below for more details.

    The rest of the instructions assumes that you work in Bash:

        bash

2.  Setup CMSSW

    TEST_DIR is the path to the directory that will contain the CMSSW configuration files.  Below we default to a temporary directory under `/tmp/$USER` where `$USER` stands for your user name.  This should generally work on `lxplus` but is not mandatory.  You should be able to change this to whatever path you like as long as you have permisson to write there.

        TEST_DIR=$(mktemp -d -p /tmp/$(whoami))
        cd $TEST_DIR
        export SCRAM_ARCH=slc6_amd64_gcc481
        cmsrel CMSSW_7_0_0_pre7
        cd CMSSW_7_0_0_pre7/src
        cmsenv


3.  Get the configs

        SOURCE=https://github.com/janveverka/CMSSW_Daq_SingleMachineTest.git
        DESTINATION=$CMSSW_BASE/src/Daq/SingleMachineTest
        git clone $SOURCE $DESTINATION

4.  Setup the test

    `ROOT_DIR` is the full path of the directory that will contain futher directories, data files and meta-data files created by the BU and FU processes.  Here, we default to `TEST_DIR` - the directory containing the configurations.  Similarly as for `TEST_DIR`, this should generally work but you should be able to change it.  Again, you should be able to write under that path.  Also, the corresponding disk should be **less than 80% used**.  These 80% are configured by the parameter `highWaterMark` of the `EvFBuildingThrottle` EDM Service in the [test/startBU_cfg.py](https://github.com/janveverka/CMSSW_Daq_SingleMachineTest/blob/master/test/startBU_cfg.py) configuration file.

    `RUN_NUMBER` is the run number used for both the BU and the FU processes.  You can customize this too as long as you use the same for both of them.

        ROOT_DIR=$TEST_DIR
        RUN_NUMBER=100

        ## Create $ROOT_DIR if needed
        if [[ ! -d $ROOT_DIR ]]; then
            mkdir -p $ROOT_DIR
        fi

5.  Run the BU process

        cd $DESTINATION/test
        cmsRun startBU_cfg.py runNumber=$RUN_NUMBER rootDir=$ROOT_DIR
        
    The output should look like this: 

        %MSG-i EvFDaqDirector:  (NoModuleName) 05-Nov-2013 16:52:22 CET pre-events
        creating filedesc for buwritelock 8
        %MSG
        %MSG-i EvFDaqDirector:  (NoModuleName) 05-Nov-2013 16:52:22 CET pre-events
        creating filedesc for fureadwritelock 146
        %MSG
        %MSG-i EvFDaqDirector:  (NoModuleName) 05-Nov-2013 16:52:22 CET pre-events
        Initializing FU LOCK FILE
        %MSG
        throttle thread started - throttle on 1
        DaqFakeReader begin Lumi 1
         building throttle on /tmp/veverka/tmp.U8qiZRS1vX/data is 58.3755 %full
        Begin processing the 1st record. Run 100, Event 1, LumiSection 1 at 05-Nov-2013 16:52:22.342 CET
        Begin processing the 2nd record. Run 100, Event 2, LumiSection 1 at 05-Nov-2013 16:52:22.363 CET
        Begin processing the 3rd record. Run 100, Event 3, LumiSection 1 at 05-Nov-2013 16:52:22.377 CET
        ...

    View the [full example BU output](https://github.com/janveverka/CMSSW_Daq_SingleMachineTest/blob/master/data/example_bu_output.log). 

    Kill the process with `Ctrl-C` after a while.

6.  Run the FU process

        cd $DESTINATION/test
        cmsRun startFU_cfg.py runNumber=$RUN_NUMBER rootDir=$ROOT_DIR

    The output should look like this:

        %MSG-i EvFDaqDirector:  (NoModuleName) 05-Nov-2013 16:59:06 CET pre-events
        creating filedesc for fureadwritelock 9
        %MSG
        <MON> DIR NOT FOUND!
        FastMonitoringService: initializing FastMonitor with microstate def path: /afs/cern.ch/cms/slc6_amd64_gcc481/
        cms/cmssw/CMSSW_7_0_0_pre7/src/EventFilter/Utilities/plugins/microstatedef.jsd 12 2 34
        Current states: Ms=0 ms=0 us=0
        %MSG-i FedRawDataInputSource:  FedRawDataInputSource:source@sourceConstruction  05-Nov-2013 16:59:06 CET pre-
        events
        test mode: 0, read-ahead chunk size: 16 on host lxplus0467
        %MSG
        %MSG-i FedRawDataInputSource:  FedRawDataInputSource:source@sourceConstruction  05-Nov-2013 16:59:06 CET pre-
        events
        Getting data from /tmp/veverka/tmp.U8qiZRS1vX/data/run000100
        ...
        RecoEventOutputModuleForFU : begin lumi
        Begin processing the 1st record. Run 100, Event 1, LumiSection 1 at 05-Nov-2013 16:59:12.381 CET
        %MSG-w HLT:  HLTPrescaler:filter1 05-Nov-2013 16:59:12 CET Run: 100 Event: 1
        Cannot read prescale column index from GT data: using default as defined by configuration or DAQ
        %MSG
        %MSG-w HLT:  HLTPrescaler:filter2 05-Nov-2013 16:59:12 CET Run: 100 Event: 1
        Cannot read prescale column index from GT data: using default as defined by configuration or DAQ
        %MSG
        Begin processing the 2nd record. Run 100, Event 2, LumiSection 1 at 05-Nov-2013 16:59:12.505 CET
        Begin processing the 3rd record. Run 100, Event 3, LumiSection 1 at 05-Nov-2013 16:59:12.626 CET
        Begin processing the 4th record. Run 100, Event 4, LumiSection 1 at 05-Nov-2013 16:59:12.748 CET
        ...

    View the [full example FU output](https://github.com/janveverka/CMSSW_Daq_SingleMachineTest/blob/master/data/example_fu_output.log). 

    You can kill this with `Ctrl-C` too.

7.  Clean up and exit

        cd
        rm -rf $ROOT_DIR
        rm -rf $TEST_DIR
        exit # Exits the Bash shell started above
        exit # Logs out from lxplus


