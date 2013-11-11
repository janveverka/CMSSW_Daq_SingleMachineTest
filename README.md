CMSSW_Daq_SingleMachineTest
===========================

This project contains the DAQ2 F3 Single Machine Test configurations.

Follow these instructions to run the F3 single machine test on the daqval at P5.

1.  Copy the test repo from github to cmsusr via lxplus
    
        ssh lxplus.cern.ch
        bash

        TEMP_DIR=$(mktemp -d -p /tmp/$(whoami))
        mkdir $TEMP_DIR/git
        cd $TEMP_DIR/git

        SOURCE=https://github.com/janveverka/CMSSW_Daq_SingleMachineTest.git
        git clone --bare $SOURCE

        cd ~
        ## Replace `$USER' with your username at P5
        rsync -a -vv $TEMP_DIR/git $USER@cmsusr:
        rm -rf $TEMP_DIR

2.  Get a terminal on a dvfu machine with CMSSW 700pre7 and enough HDD space

        ## Replace `$USER' with your username at P5
        ssh $USER@cmsusr
        wassh -h 'dvfu-c2f37-3[4,6,8]-0[1-4]' 'df /tmp' 2> /dev/null

    The output should look something like this:

        dvfu-c2f37-34-01:                                                    
           Filesystem           1K-blocks      Used Available Use% Mounted on
           /dev/sda2             75594872  26653048  45101824  38% /         
        dvfu-c2f37-34-02:                                                    
           Filesystem           1K-blocks      Used Available Use% Mounted on
           /dev/sda2             75594872  26373616  45381256  37% /         
        dvfu-c2f37-34-03:
           Filesystem           1K-blocks      Used Available Use% Mounted on
           /dev/sda2             75594872  26580640  45174232  38% /

    Here, 38%, 37%, and 38% of the device containing the `\tmp` directory on the machine dvfu-c2f37-34-01, dvfu-c2f37-34-02 and dvfu-c2f37-34-03 is used, respectively.  *To run this test, you need to use a device, which is less than 80% used.  See the item "Setup the test"* below for more details.

    Choose a machine with enough free space, for example:

        ssh dvfu-c2f37-34-01

    The rest of the instructions assumes that you work in Bash:

        bash

3.  Setup CMSSW

    `$TEST_DIR` gives the full path to the directory that will contain the CMSSW configuration files.  Below we default to a temporary directory under `/tmp/$USER` where `$USER` stands for your user name.  This should generally work on `lxplus` but is not mandatory.  You should be able to change this to whatever path you like as long as you have permisson to write there.

        MY_TEMP_DIR=/tmp/$(whoami)
        if [[ ! -d mkdir $MY_TEMP_DIR ]]; then
            mkdir $MY_TEMP_DIR
        fi
        TEST_DIR=$(mktemp -d -p $MY_TEMP_DIR)
        cd $TEST_DIR
        export SCRAM_ARCH=slc6_amd64_gcc481
        source /opt/cmssw/offline/cmsset_default.sh
        cmsrel CMSSW_7_0_0_pre7
        cd CMSSW_7_0_0_pre7/src
        cmsenv

4.  Get the configs

        SOURCE=$HOME/git/CMSSW_Daq_SingleMachineTest.git
        DESTINATION=$CMSSW_BASE/src/Daq/SingleMachineTest
        git clone $SOURCE $DESTINATION

5.  Setup the test

    `$ROOT_DIR` gives the full path of the directory that will contain futher directories, data files and meta-data files created by the BU and FU processes.  Here, we default `$ROOT_DIR` to `$TEST_DIR`, the directory containing the configurations, which in turn defaults to a directory under `/tmp`, see the item *Setup CMSSW* above.  Similarly to `$TEST_DIR`, the default should generally work but you should be able to change it if you want.  Again, you need to be able to write under the `$ROOT_DIR` path.  Also, the corresponding disk should be **less than 80% used**.  These 80% are configured by the parameter `highWaterMark` of the `EvFBuildingThrottle` EDM Service in the [test/startBU_cfg.py](https://github.com/janveverka/CMSSW_Daq_SingleMachineTest/blob/master/test/startBU_cfg.py) configuration file.

    `$RUN_NUMBER` gives the run number used for the BU process and the FU process.  The purpose of this variable is to make sure that the same run number is used for both the BU and the FU. You can customize this too.

        ROOT_DIR=$TEST_DIR
        RUN_NUMBER=100

        ## Create output directories if needed
        mkdir -p $ROOT_DIR/{BU,FU}

6.  Run the BU process

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

    View the [full output of the example BU process](https://github.com/janveverka/CMSSW_Daq_SingleMachineTest/blob/master/data/example_bu_output.log). 

    Kill the process with `Ctrl-C` after a while.

7.  Run the FU process

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

    View the [full output of the example FU process](https://github.com/janveverka/CMSSW_Daq_SingleMachineTest/blob/master/data/example_fu_output.log). 

    You can kill this with `Ctrl-C` too.

8.  Clean up and exit

        cd
        rm -rf $ROOT_DIR
        rm -rf $TEST_DIR
        exit # Exits the Bash shell started above
        exit # Logs out from the machine


