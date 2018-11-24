# sleepbot-to-sleep_as_android

This Python script convert [Sleepbot](https://www.mysleepbot.com/) records exported from the app to [Sleep as Android](http://sleep.urbandroid.org/) supported import format.

This script is written for and tested in the following enviroment:
* Python 3.5.2 64-bit on Windows 7 64-bit
* Sleepbot 3.2.8 on Android 7.1.1
* Sleep as Android 20161122 on Android 7.1.1

## Usage
1. Get a stable version of the Python script in [release page](https://github.com/VeryCrazyDog/sleepbot-to-sleep_as_android/releases).
2. In **Sleepbot**, go to the second tab for statistic, set the **From** date to the earliest record date and press the **SHARE** button at the bottom right of the screen. Take note on the exported file path.
3. Copy the exported file to a computer with Python 3.5.
4. Change the configuration in the script `sleepbot_to_sleep_as_android.py`. Refer to the below section for configurable options.
5. Run the conversion script.
6. On **Sleep as Android**, open the menu and select **Backup**, then click **Export data** from the pop up menu to backup the existing data. Take note on the exported file path.
7. Copy the **Sleep as Android** backup to the computer as backup and replace it with the converted file.
8. On **Sleep as Android**, open the menu and select **Backup**, then click **Import data** from the pop up menu to import the converted file.

## Configurable Options

There are several configuration set in the script which will need to change in order for the convertion to work.

* `PATH_IN_SLEEPBOT_EXPORT`: The path to the **Sleepbot** exported file. On Windows, please make sure that the path is using slash `/` instead of backslash `\` for the directory separator.
* `PATH_OUT_SLEEP_AS_ANDROID`: The path converted **Sleep as Android** file format for import. On Windows, please make sure that the path is using slash `/` instead of backslash `\` for the directory separator.
* `SLEEPBOT_EXPORT_DATE_FORMAT`: The date format used in the **Sleepbot** exported file. You will have to change it if the date format in the exported file not `dd/mm/yy`.
* `SLEEPBOT_EXPORT_TIME_FORMAT`: The time format used in the **Sleepbot** exported file. Most like you don't need to change it.
* `TIMEZONE`: The timezone of records in the **Sleepbot** exported file. You will have to change it if `Asia/Hong_Kong` is not your timezone. You may refer to https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for the list of timezone available.
* `NOTE_PREFIX`: A prefix to be added before your note of each sleep records. If you like to have a prefix on the note, you will have to change the value.
* `NOTE_SUFFIX`: A suffix to be added before your note of each sleep records. If you don't like suffix ` [Sleepbot Import]` to be added to each of your record, you will have to change the value.

## Sample Files

**Sleepbot** sample exported file:

```csv
Date, Sleep Time, Wake Time, Hours,Note
13/01/17,13:25,13:55,0.49,
13/01/17,00:50,07:56,7.1,
12/01/17,00:17,07:48,7.51,
09/01/17,13:13,13:54,0.69,
09/01/17,23:59,07:56,7.95,
```

Sample converted format compatible for import in **Sleep as Android**:

```csv
Id,Tz,From,To,Sched,Hours,Rating,Comment,Framerate,Snore,Noise,Cycles,DeepSleep,LenAdjust,Geo,"13:55"
"1484285100000","Asia/Hong_Kong","13. 01. 2017 13:25","13. 01. 2017 13:55","13. 01. 2017 13:55","0.490","0.0","[Sleepbot Import]","10000","-1","-1.0","-1","-2.0","0","","0.0"
Id,Tz,From,To,Sched,Hours,Rating,Comment,Framerate,Snore,Noise,Cycles,DeepSleep,LenAdjust,Geo,"07:56"
"1484239800000","Asia/Hong_Kong","13. 01. 2017 0:50","13. 01. 2017 7:56","13. 01. 2017 7:56","7.100","0.0","[Sleepbot Import]","10000","-1","-1.0","-1","-2.0","0","","0.0"
Id,Tz,From,To,Sched,Hours,Rating,Comment,Framerate,Snore,Noise,Cycles,DeepSleep,LenAdjust,Geo,"07:48"
"1484151420000","Asia/Hong_Kong","12. 01. 2017 0:17","12. 01. 2017 7:48","12. 01. 2017 7:48","7.510","0.0","[Sleepbot Import]","10000","-1","-1.0","-1","-2.0","0","","0.0"
Id,Tz,From,To,Sched,Hours,Rating,Comment,Framerate,Snore,Noise,Cycles,DeepSleep,LenAdjust,Geo,"13:54"
"1483938780000","Asia/Hong_Kong","09. 01. 2017 13:13","09. 01. 2017 13:54","09. 01. 2017 13:54","0.690","0.0","[Sleepbot Import]","10000","-1","-1.0","-1","-2.0","0","","0.0"
Id,Tz,From,To,Sched,Hours,Rating,Comment,Framerate,Snore,Noise,Cycles,DeepSleep,LenAdjust,Geo,"07:56"
"1483891140000","Asia/Hong_Kong","08. 01. 2017 23:59","09. 01. 2017 7:56","09. 01. 2017 7:56","7.950","0.0","[Sleepbot Import]","10000","-1","-1.0","-1","-2.0","0","","0.0"
```
