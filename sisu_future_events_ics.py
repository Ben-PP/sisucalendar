from datetime import date
import re
import sys, getopt

class Errors:
    INVALID_ARGUMENTS = "Invalid arguments!"
    ARGUMENT_COUNT_ERROR = "Too many/few arguments!"
    INVALID_INPUT_FILE_FORMAT = "Invalid input_file file format!"
    INPUTFILE_DOES_NOT_EXIST = "Input file given not found!"
    COULD_NOT_WRITE_OUTPUT = "Could not write the output file!"
    INVALID_DATE = "Invalid date! Must be YYYYMMDD"

def raise_error(reason: str):
    print(f"[ERROR]: {reason}")
    send_help()
    sys.exit()

def send_help():
    print("Usage:")
    print("python sisu_future_events_ics.py -i <input_file> -o <output_file>")
    print("-i, --input_file: .ics file to be modified.")
    print("-o, --output_file: .ics file to be saved.")
    print("-d, --date: A date from which point forward the events are included. Must contain only numbers and be format <YYYYMMDD>")
    print("Also be sure that all directories exist!")

def check_date(vevent: str, date_to_start: str):
    match = re.search(r'DTSTART:(\d{8})T', vevent)
    start_date = match.group(1)
    return int(start_date) >= int(date_to_start)

def main(argv: list[str]):
    if (len(argv) != 4 and len(argv) != 6):
        print(len(argv))
        raise_error(Errors.ARGUMENT_COUNT_ERROR)
    
    try:
        opts, args = getopt.getopt(argv, "-i:o:d:", ["inputfile","outputfile","date"])
    except Exception as e:
        print(e)
        raise_error(Errors.INVALID_ARGUMENTS)

    input_file = ""
    output_file = ""
    cutoff_date = str(date.today()).replace("-","")

    for opt,arg in opts:
        if opt in ("-i", "--inputfile"):
            input_file = arg
            if (not str(input_file).endswith(".ics")):
                print(f"Inputfile given was: '{str(input_file)}'")
                raise_error(Errors.INVALID_INPUT_FILE_FORMAT)
        elif opt in ("-o", "--outputfile"):
            output_file = arg
            if (str(output_file).endswith(".ics")):
                output_file = str(output_file).replace(".ics","")
        elif opt in ("-d", "--date"):
            cutoff_date = arg
            if (len(cutoff_date) != 8 or not str(cutoff_date).isdigit()):
                raise_error(Errors.INVALID_DATE)
    newIcs = ""
    adding_event = False
    try:
        with open(input_file, "r") as f:
            event_to_add = ''
            for line in f:
                if (line.startswith("BEGIN:VEVENT")):
                    adding_event = True
                    event_to_add = f"{line}"
                    continue
                elif (adding_event and not line.startswith("END:VEVENT")):
                    event_to_add = f"{event_to_add}{line}"
                    continue
                elif (adding_event and line.startswith("END:VEVENT")):
                    event_to_add = f"{event_to_add}{line}"
                    if (not check_date(vevent=event_to_add, date_to_start=cutoff_date)):
                        continue
                    newIcs = f"{newIcs}{event_to_add}"
                    adding_event = False
                    event_to_add = ""
                    continue
                newIcs = f"{newIcs}{line}"
    except Exception as e:
        print(e)
        raise_error(Errors.INPUTFILE_DOES_NOT_EXIST)
    
    try:
        with open(f"{output_file}.ics", "w") as f:
            f.write(newIcs)
    except:
        raise_error(Errors.COULD_NOT_WRITE_OUTPUT)

if (__name__ == "__main__"):
    #string_test()
    main(sys.argv[1:])