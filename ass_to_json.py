import re
import json
import argparse
from pathlib import Path

def parse_time(time_str):
    """
    Parse ASS time format (H:MM:SS.cc) into total seconds.
    
    Args:
        time_str (str): Time in ASS format (e.g., "1:23:45.67")
        
    Returns:
        str: Original time string for JSON output
    """
    return time_str

def parse_ass_file(file_path):
    """
    Parse an ASS file and extract dialogue lines.
    
    Args:
        file_path (str): Path to the ASS file
        
    Returns:
        list: List of dictionaries containing dialogue information
    """
    dialogues = []
    dialogue_pattern = re.compile(r'Dialogue: [^,]*,([^,]*),([^,]*),([^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,)(.*)')
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('Dialogue:'):
                match = dialogue_pattern.match(line)
                if match:
                    start_time, end_time, _, text = match.groups()
                    
                    # Create dialogue entry
                    dialogue = {
                        "start_time": start_time,
                        "end_time": end_time,
                        "dialog": text.strip()
                    }
                    dialogues.append(dialogue)
    
    return dialogues

def write_json(dialogues, output_path):
    """
    Write dialogues to a JSON file.
    
    Args:
        dialogues (list): List of dialogue dictionaries
        output_path (str): Path where JSON file will be saved
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(dialogues, file, ensure_ascii=False, indent=2)

def main():
    """
    Main function to handle command line arguments and control the conversion process.
    """
    parser = argparse.ArgumentParser(description='Convert ASS subtitle files to JSON format')
    parser.add_argument('input', help='Path to input ASS file')
    parser.add_argument('-o', '--output', help='Path to output JSON file (optional)')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # Validate input file
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.")
        return
    
    if not input_path.suffix.lower() == '.ass':
        print(f"Error: Input file must be an ASS file")
        return
    
    # Determine output path
    output_path = Path(args.output) if args.output else input_path.with_suffix('.json')
    
    try:
        # Parse ASS file
        dialogues = parse_ass_file(str(input_path))
        
        # Write JSON file
        write_json(dialogues, str(output_path))
        
        print(f"Successfully converted '{input_path}' to '{output_path}'")
        print(f"Extracted {len(dialogues)} dialogue lines")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()