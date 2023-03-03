# SisuFutureEvents
This script takes your exported .ics file from Sisu which contains all events from the start of your studies and strips it down to only contain all events from the given date forward.

## Usage
Python is needed to use this. Python 3.10 or higher is recommended. `--input_file` and `--output_file` must be given. `--date` is optional.

### Arguments
This script must take at least 2 arguments, `--input_file` and `--output_file`. Additionaly 3. argument `--date` can be given to specify the date from which date forward the events will be added.

- `-i, --input_file` File which is read by the script. Must be `.ics` file.
- `-o, --output_file` File to which the new calendar will be saved. Can be anything but final file will be `.ics` file even if other extension than `.ics` is given. NOTE: All the directories contained in the file path must exists beforehand!
- `-d, --date` Date from which point forward the events are added to new file. If this is not suplied, current date will be used. This has to be format `YYYYMMMDD` for example `-d 20221201`.