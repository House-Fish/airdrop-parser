# Airdrop-Parser
A small utility used to parse logs created by mandiant/macos-unifiedlogs, displaying them in Singapore Time. 


## Requirements 
- pytz

## Set-up
``` bash
# on linux
git clone <this_repository>

python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
```
## Example
I want to parse AirDrop logs from system_logs.logarchive, I will extract out all the logs using mandiant/macos-unifiedlogs (p.s. there are many logs that it does not recognize, but from my testing, it has been able to identify AirDrop logs), then I will grep for the logs that are in the "category":"AirDrop", storing them in a new .json file. Finally I will run this tool, to generate a airdrop.log file. 

``` bash
unifiedlog_iterator -m log-archive -i ./system_logs.logarchive/ -o system_logs.json
grep -i ‘”category”:”AirDrop”’ system_logs.json > airdrop.json
python parser.py
```

## Considerations
THis project is actually really simple, all it does is parse the unified logs in a .json format, extract out the timestamp, process and message, sort it according to SGT and writes it to a .log file. In theory, this could work with any logs, not just AirDrop logs. Just change the input_file and output_file names to the names of the files that you want, and it can parse any logs. The main extraction is being done in the grep step, so bababoey! 
Maybe I'll clean this up a bit more so that it runs the grep for you based on a parameter you pass into the parser, but uh, created this for a DF Assignment, may not come back to it HAHAHA! 