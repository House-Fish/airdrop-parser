import json
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
                    'timestamp': sg_dt.strftime('%Y-%m-%d %H:%M:%S.%f %z'),  # Format: YYYY-MM-DD HH:MM:SS.mmmmmm +HHMM
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
    
    # Write sorted logs to output file in a simple log format
    with open(output_file_path, 'w') as outfile:
        for log in sorted_logs:
            # Format: [timestamp] process: message
            log_line = f"[{log['timestamp']}] {log['process']}: {log['message']}\n"
            outfile.write(log_line)

# Example usage
if __name__ == "__main__":
    input_file = "airdrop.json"  # Replace with your input file path
    output_file = "airdrop.log"  # Replace with desired output file path
    parse_airdrop_logs(input_file, output_file)