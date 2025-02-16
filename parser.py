import json
import argparse
from datetime import datetime
import pytz

def parse_airdrop_logs(input_file_path, output_file_path):
    """
    Parse AirDrop logs from a JSON file, extract key fields, convert timestamps to
    Singapore time, sort by timestamp, and write to a .log file.
    
    Args:
        input_file_path (str): Path to the input JSON file containing AirDrop logs
        output_file_path (str): Path where the sorted logs will be written
    """
    # Get Singapore timezone
    sg_tz = pytz.timezone('Asia/Singapore')
    logs = []

    print(f"Reading from {input_file_path}")
    
    # Read and parse the JSON file
    with open(input_file_path, 'r') as file:
        for line in file:
            try:
                log_entry = json.loads(line.strip())
                # Parse UTC timestamp and convert to Singapore time
                utc_dt = datetime.fromisoformat(log_entry['timestamp'].replace('Z', '+00:00'))
                sg_dt = utc_dt.astimezone(sg_tz)
                
                # Create simplified log entry with only needed fields
                simplified_entry = {
                    'timestamp': sg_dt.strftime('%Y-%m-%d %H:%M:%S.%f %z'),
                    'process': log_entry['process'],
                    'message': log_entry['message'],
                    'datetime': sg_dt  # Keep datetime object for sorting
                }
                logs.append(simplified_entry)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON line: {e}")
            except KeyError as e:
                print(f"Missing required field: {e}")
    
    # Sort logs by timestamp
    sorted_logs = sorted(logs, key=lambda x: x['datetime'])

    print("Successfully parsed the file!")
    
    # Write sorted logs to output file in a simple log format
    with open(output_file_path, 'w') as outfile:
        for log in sorted_logs:
            # Format: [timestamp] process: message
            log_line = f"[{log['timestamp']}] {log['process']}: {log['message']}\n"
            outfile.write(log_line)

    print(f"Writing to {output_file_path}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and convert AirDrop logs to a sorted log file.")
    parser.add_argument("input_file", help="Path to the input JSON file containing AirDrop logs")
    parser.add_argument("output_file", help="Path where the sorted logs will be written")
    
    args = parser.parse_args()
    parse_airdrop_logs(args.input_file, args.output_file)
