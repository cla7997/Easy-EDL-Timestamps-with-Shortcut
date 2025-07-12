import os
import time
import datetime
import configparser
import keyboard
import threading

class EDLTimestampLogger:
    def __init__(self):
        self.marker_count = 0
        self.start_time = None
        self.edl_file = None
        self.config_file = "edltimestamps_config.ini"
        self.hotkey = "alt gr+f10"
        self.end_hotkey = "ctrl+delete"
        self.running = False
        
        # Load config
        self.load_config()
        
        # Create EDL file
        self.create_edl_file()
        
        # Write EDL header
        self.write_edl_header()
        
    def load_config(self):
        """Load configuration from INI file, create if doesn't exist"""
        if not os.path.exists(self.config_file):
            self.create_default_config()
        
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        try: # Default hotkeys for recording timestamps and ending program, change in edltimestamps_config.ini file
            self.hotkey = config.get('settings', 'hotkey', fallback='altf10')
            self.end_hotkey = config.get('settings', 'end_hotkey', fallback='ctrl+delete')
        except:
            self.hotkey = 'alt gr+f10'
            self.end_hotkey = 'ctrl+delete'
    
    def create_default_config(self):
        """Create default configuration file"""
        config = configparser.ConfigParser()
        config['settings'] = {
            'hotkey': 'alt gr+f10',
            'end_hotkey': 'ctrl+delete'
        }
        
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)
        
        print(f"Created default config file: {self.config_file}")
        print(f"Default hotkey: {self.hotkey}")
        print(f"Default end hotkey: {self.end_hotkey}")
    
    def create_edl_file(self):
        """Create EDL file with current timestamp"""
        now = datetime.datetime.now()
        filename = f"timestamps_{now.strftime('%Y-%m-%d_%H-%M-%S')}.edl"
        self.edl_file = filename
        self.start_time = time.time()
        
        print(f"Created EDL file: {filename}")
    
    def write_edl_header(self):
        """Write EDL header to file"""
        with open(self.edl_file, 'w') as f:
            f.write("TITLE: Timestamp Markers - github.com/cla7997/Easy-EDL-Timestamps-with-Shortcut\n")
            f.write("FCM: NON-DROP FRAME\n")
            f.write("\n")
    
    def format_timecode(self, seconds):
        """Convert seconds to timecode format HH:MM:SS:00"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:00"
    
    def format_timecode_next_frame(self, seconds):
        """Convert seconds to timecode format HH:MM:SS:01 (next frame)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:01"
    
    def add_marker(self):
        """Add a marker at current timestamp"""
        current_time = time.time()
        elapsed_seconds = current_time - self.start_time
        
        self.marker_count += 1
        
        # Format timecode (in frame at :00, out frame at :01, so that marker is one frame long)
        timecode_in = self.format_timecode(elapsed_seconds)
        timecode_out = self.format_timecode_next_frame(elapsed_seconds)
        
        # Create EDL entry
        edl_line = f"{self.marker_count:03d}  001      V     C        {timecode_in} {timecode_out} {timecode_in} {timecode_out}\n"
        metadata_line = f" |C:ResolveColorBlue |M:Marker {self.marker_count} |D:1\n"
        
        # Write to file
        with open(self.edl_file, 'a') as f:
            f.write(edl_line)
            f.write(metadata_line)
            f.write("\n")
        
        print(f"Added Marker {self.marker_count} at {timecode_in}")
    
    def on_end_hotkey(self):
        """End hotkey callback function"""
        print(f"\nEnd hotkey pressed! Stopping logger...")
        print(f"Total markers added: {self.marker_count}")
        print(f"EDL file saved: {self.edl_file}")
        self.running = False
        keyboard.unhook_all()
    
    def on_hotkey(self):
        """Hotkey callback function"""
        self.add_marker()
    
    def start_logging(self):
        """Start the logging session"""
        self.running = True
        
        print(f"\nEDL Timestamp Logger Started!")
        print(f"Press '{self.hotkey}' to add timestamps")
        print(f"Press '{self.end_hotkey}' to stop and exit")
        print(f"Logging to: {self.edl_file}")
        print("-" * 50)
        
        # Register hotkeys
        keyboard.add_hotkey(self.hotkey, self.on_hotkey)
        keyboard.add_hotkey(self.end_hotkey, self.on_end_hotkey)
        
        try:
            # Keep the program running
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print(f"\nStopping logger...")
            print(f"Total markers added: {self.marker_count}")
            print(f"EDL file saved: {self.edl_file}")
            keyboard.unhook_all()

def main():
    logger = EDLTimestampLogger()
    logger.start_logging()

if __name__ == "__main__":
    main()