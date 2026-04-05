
import base64
import marshal
import zlib
import os
import sys
import time
import random
from pathlib import Path

# ANSI color codes for terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    
    # Matrix colors
    MATRIX_GREEN = '\033[38;5;46m'
    MATRIX_DARK_GREEN = '\033[38;5;22m'
    HACKER_RED = '\033[38;5;196m'
    HACKER_ORANGE = '\033[38;5;208m'
    HACKER_PURPLE = '\033[38;5;129m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_matrix_effect(text, delay=0.003):
    """Print text with matrix-style character reveal"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_hacker_banner():
    """Display a cool hacker-style banner"""
    banner = f"""
{Colors.MATRIX_GREEN}╔══════════════════════════════════════════════════════════════╗
  _  _  ___   ___  _____  ____   ___  _   _ 
 | \| |/ _ \ / _ \| _ ) \/ /\ \ / /_\| | | |
 | .` | (_) | (_) | _ \>  <  \ V / _ \ |_| |
 |_|\_|\___/ \___/|___/_/\_\  \_/_/ \_\___/ 
                                            
                                                                  ║
║              {Colors.HACKER_PURPLE}PYTHON CODE ENCRYPTOR v2.0{Colors.MATRIX_GREEN}               ║
║         {Colors.CYAN}       [ Developer NOOBXVAU ]{Colors.MATRIX_GREEN}          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

def print_status(message, status_type="info"):
    """Print formatted status messages"""
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    
    if status_type == "success":
        prefix = f"{Colors.MATRIX_GREEN}[✓]{Colors.END}"
    elif status_type == "error":
        prefix = f"{Colors.FAIL}[✗]{Colors.END}"
    elif status_type == "warning":
        prefix = f"{Colors.WARNING}[⚠]{Colors.END}"
    elif status_type == "processing":
        prefix = f"{Colors.HACKER_PURPLE}[⟳]{Colors.END}"
    else:
        prefix = f"{Colors.CYAN}[ℹ]{Colors.END}"
    
    print(f"{Colors.DIM}[{timestamp}]{Colors.END} {prefix} {message}")

def animate_processing():
    """Show a cool processing animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(20):
        for frame in frames:
            sys.stdout.write(f"\r{Colors.HACKER_PURPLE}{frame} Processing...{Colors.END}")
            sys.stdout.flush()
            time.sleep(0.05)
    sys.stdout.write("\r" + " " * 30 + "\r")

def matrix_rain_effect(lines=5):
    """Create a mini matrix rain effect"""
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    
    for _ in range(lines):
        line = ""
        for _ in range(80):
            if random.random() > 0.5:
                char = random.choice(chars)
                if random.random() > 0.7:
                    line += f"{Colors.MATRIX_GREEN}{char}{Colors.END}"
                else:
                    line += f"{Colors.MATRIX_DARK_GREEN}{char}{Colors.END}"
            else:
                line += " "
        print(line)
        time.sleep(0.1)

def get_file_with_browser():
    """Interactive file browser with hacker style"""
    current_dir = Path.cwd()
    
    while True:
        clear_screen()
        print_hacker_banner()
        
        print(f"\n{Colors.HACKER_PURPLE}═══ CURRENT DIRECTORY ═══{Colors.END}")
        print(f"{Colors.CYAN}📁 {current_dir}{Colors.END}\n")
        
        print(f"{Colors.HACKER_ORANGE}Available Python files:{Colors.END}")
        python_files = list(current_dir.glob("*.py"))
        
        if not python_files:
            print(f"{Colors.WARNING}  No Python files found in current directory{Colors.END}")
        else:
            for idx, file in enumerate(python_files, 1):
                size = file.stat().st_size
                modified = time.strftime("%Y-%m-%d %H:%M", time.localtime(file.stat().st_mtime))
                print(f"  {Colors.MATRIX_GREEN}[{idx}]{Colors.END} {Colors.BOLD}{file.name}{Colors.END} "
                      f"{Colors.DIM}({size} bytes) - {modified}{Colors.END}")
        
        print(f"\n{Colors.CYAN}Options:{Colors.END}")
        print(f"  {Colors.MATRIX_GREEN}[n]{Colors.END} New directory path")
        print(f"  {Colors.MATRIX_GREEN}[u]{Colors.END} Go up one directory")
        print(f"  {Colors.MATRIX_GREEN}[q]{Colors.END} Quit")
        
        choice = input(f"\n{Colors.HACKER_PURPLE}┌─[{Colors.MATRIX_GREEN}Select file/directory{Colors.HACKER_PURPLE}]\n└──╼ {Colors.END}").strip()
        
        if choice.lower() == 'q':
            return None
        elif choice.lower() == 'u':
            current_dir = current_dir.parent
            continue
        elif choice.lower() == 'n':
            new_path = input(f"{Colors.CYAN}Enter new directory path: {Colors.END}").strip()
            if os.path.exists(new_path) and os.path.isdir(new_path):
                current_dir = Path(new_path)
            else:
                print_status("Invalid directory path!", "error")
                time.sleep(1.5)
            continue
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(python_files):
                return str(python_files[idx])
            else:
                print_status("Invalid selection!", "error")
                time.sleep(1.5)
        except ValueError:
            print_status("Invalid input!", "error")
            time.sleep(1.5)

def encrypt_file(file_name):
    """Encrypt the Python file with multiple layers"""
    
    # Check if file exists
    if not os.path.exists(file_name):
        print_status(f"File '{file_name}' not found!", "error")
        return None
    
    # Read original code
    print_status(f"Reading target file: {Colors.BOLD}{file_name}{Colors.END}", "processing")
    with open(file_name, "r", encoding="utf-8") as f:
        source = f.read()
    
    print_status(f"Source code loaded ({len(source)} bytes)", "success")
    
    # Show encryption progress
    layers = [
        ("Compiling bytecode", Colors.HACKER_PURPLE),
        ("Marshaling objects", Colors.HACKER_ORANGE),
        ("Compressing data (zlib)", Colors.CYAN),
        ("Encoding (base64)", Colors.MATRIX_GREEN)
    ]
    
    # Compile code
    print_status(layers[0][0], "processing")
    time.sleep(0.3)
    compiled = compile(source, "<encrypted>", "exec")
    
    # Marshal layer
    print_status(layers[1][0], "processing")
    time.sleep(0.3)
    layer1 = marshal.dumps(compiled)
    
    # Zlib compression
    print_status(layers[2][0], "processing")
    time.sleep(0.3)
    layer2 = zlib.compress(layer1)
    
    # Base64 encoding
    print_status(layers[3][0], "processing")
    time.sleep(0.3)
    layer3 = base64.b64encode(layer2)
    
    encoded = layer3.decode()
    
    print_status(f"Encryption complete! ({len(encoded)} bytes encoded)", "success")
    
    # Create loader script with enhanced features
    loader = f'''#!/usr/bin/env python3
# ──[ This code is secured by NOOB HACKER BD  ]────────────────────────────────
#  This file is encrypted for protection
#  Generated by Arcane Python Encryptor v2.0
#  Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
# ────────────────────────────────────────────────────────────

import base64
import marshal
import zlib
import sys
import os

# Encrypted payload
data = "{encoded}"

# Optional: Add anti-debugging features
if __name__ == "__main__":
    try:
        # Execute the encrypted code
        exec(
            marshal.loads(
                zlib.decompress(
                    base64.b64decode(data)
                )
            )
        )
    except Exception as e:
        print(f"\\033[91m[!] Error executing encrypted code: {{e}}\\033[0m")
        sys.exit(1)
'''
    
    # Generate output filename
    output = f"encrypted_{os.path.basename(file_name)}"
    
    # Write encrypted file
    with open(output, "w", encoding="utf-8") as f:
        f.write(loader)
    
    return output

def main():
    """Main function with hacker UI"""
    try:
        while True:
            clear_screen()
            print_hacker_banner()
            
            # Show matrix rain effect
            matrix_rain_effect(3)
            
            print(f"\n{Colors.HACKER_PURPLE}[ SYSTEM MENU ]{Colors.END}")
            print(f"  {Colors.MATRIX_GREEN}[1]{Colors.END} Encrypt Python file")
            print(f"  {Colors.MATRIX_GREEN}[2]{Colors.END} Quick encrypt (enter path)")
            print(f"  {Colors.MATRIX_GREEN}[3]{Colors.END} Exit")
            
            choice = input(f"\n{Colors.HACKER_PURPLE}┌─[{Colors.MATRIX_GREEN}root@hacker{Colors.HACKER_PURPLE}]\n└──╼ {Colors.END}").strip()
            
            if choice == '1':
                file_name = get_file_with_browser()
                if file_name:
                    print_status(f"Selected: {Colors.BOLD}{file_name}{Colors.END}", "success")
                    time.sleep(0.5)
                    
                    # Animate processing
                    animate_processing()
                    
                    # Encrypt the file
                    output = encrypt_file(file_name)
                    
                    if output:
                        print_status(f"✅ Success! Encrypted file saved as: {Colors.BOLD}{output}{Colors.END}", "success")
                        
                        # Show file info
                        file_size = os.path.getsize(output)
                        print(f"\n{Colors.CYAN}📊 File Statistics:{Colors.END}")
                        print(f"  • Output file: {output}")
                        print(f"  • Size: {file_size} bytes")
                        print(f"  • Location: {os.path.abspath(output)}")
                        
                        # Offer to view the encrypted file
                        view = input(f"\n{Colors.HACKER_PURPLE}View encrypted file? (y/n): {Colors.END}").strip().lower()
                        if view == 'y':
                            print(f"\n{Colors.MATRIX_GREEN}{'='*60}{Colors.END}")
                            with open(output, 'r') as f:
                                content = f.read()
                                preview = content[:500] + "..." if len(content) > 500 else content
                                print(preview)
                            print(f"{Colors.MATRIX_GREEN}{'='*60}{Colors.END}")
                    
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")
            
            elif choice == '2':
                file_name = input(f"{Colors.CYAN}Enter Python file path: {Colors.END}").strip()
                if file_name:
                    animate_processing()
                    output = encrypt_file(file_name)
                    if output:
                        print_status(f"✅ Encrypted file saved as: {Colors.BOLD}{output}{Colors.END}", "success")
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")
            
            elif choice == '3':
                print(f"\n{Colors.HACKER_PURPLE}Exiting... Stay secure!{Colors.END}")
                time.sleep(1)
                break
            
            else:
                print_status("Invalid option!", "error")
                time.sleep(1.5)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠ Interrupted by user{Colors.END}")
        sys.exit(0)

if __name__ == "__main__":
    main()