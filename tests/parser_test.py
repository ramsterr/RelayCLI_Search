'''source venv/bin/activate && python3 -c "
from parser import scan_directory
entries = scan_directory('.')
print(f'Found {len(entries)} definitions:')
for e in entries[:5]:
    print(f'  [{e[\"kind\"]}] {e[\"name\"]} (line {e[\"line\"]})')
"'''


#the above one also includes venv and __pychace__ directories , so i have added a skip helper to skip them


source venv/bin/activate && python3 -c "
from pathlib import Path
from parser import parse_file, scan_directory

# Test with just parser.py 
entries = parse_file(Path('parser.py'))
print(f'parser.py: {len(entries)} definitions')
for e in entries:
    print(f'  [{e[\"kind\"]}] {e[\"name\"]} (line {e[\"line\"]})')
"
