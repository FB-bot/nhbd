import requests
import time
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

class BioscopeOTPSender:
    def __init__(self):
        self.base_url = "https://api-dynamic.bioscopelive.com/v2/auth/login"
        self.params = {
            "country": "BD",
            "platform": "web",
            "language": "en"
        }
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def clear_screen(self):
        """Clear screen function"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Print banner function"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════╗
║     Bioscope OTP Tool v2.0           ║
║       Created with {Fore.RED}❤️{Fore.CYAN}                   ║
║     {Fore.YELLOW}Multi OTP on Single Number{Fore.CYAN}        ║
╚══════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def format_number(self, phone_number):
        """Format phone number function"""
        phone_number = phone_number.strip()
        
        if not phone_number.startswith('+880'):
            if phone_number.startswith('01'):
                phone_number = '+88' + phone_number
            elif phone_number.startswith('1'):
                phone_number = '+880' + phone_number
            else:
                phone_number = '+880' + phone_number.lstrip('0')
        
        return phone_number
    
    def send_otp(self, phone_number, count=1, delay=2):
        """Send multiple OTPs to a single number"""
        
        formatted_number = self.format_number(phone_number)
        success_count = 0
        fail_count = 0
        
        print(f"\n{Fore.YELLOW}Sending {count} OTP(s) to {formatted_number}{Style.RESET_ALL}\n")
        
        for i in range(1, count + 1):
            payload = {"number": formatted_number}
            
            try:
                print(f"{Fore.WHITE}[{i}/{count}] Sending OTP...{Style.RESET_ALL}", end=" ")
                
                response = requests.post(
                    self.base_url,
                    params=self.params,
                    headers=self.headers,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"{Fore.GREEN}✓ Success{Style.RESET_ALL}")
                    success_count += 1
                else:
                    print(f"{Fore.RED}✗ Failed (Status: {response.status_code}){Style.RESET_ALL}")
                    fail_count += 1
                    
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}")
                fail_count += 1
            
            # Delay between requests (except last one)
            if i < count:
                time.sleep(delay)
        
        # Show report
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════╗")
        print(f"║           Final Report               ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ Total Sent: {count}                          ║")
        print(f"║ {Fore.GREEN}Successful: {success_count}{Fore.CYAN}                      ║")
        print(f"║ {Fore.RED}Failed: {fail_count}{Fore.CYAN}                            ║")
        print(f"╚══════════════════════════════════════╝{Style.RESET_ALL}")
        
        return success_count, fail_count
    
    def single_mode(self):
        """Single number single OTP mode"""
        self.clear_screen()
        self.print_banner()
        
        print(f"{Fore.YELLOW}[Single Mode - One OTP to one number]{Style.RESET_ALL}")
        phone = input(f"{Fore.WHITE}Enter phone number (e.g., 017xxxxxxxx): {Style.RESET_ALL}")
        
        if phone.strip():
            self.send_otp(phone, 1)
        else:
            print(f"{Fore.RED}No number provided!{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def multi_otp_mode(self):
        """Single number multiple OTPs mode"""
        self.clear_screen()
        self.print_banner()
        
        print(f"{Fore.YELLOW}[Multi OTP Mode - Multiple OTPs to one number]{Style.RESET_ALL}\n")
        
        # Phone number input
        phone = input(f"{Fore.WHITE}Enter phone number (e.g., 017xxxxxxxx): {Style.RESET_ALL}")
        
        if not phone.strip():
            print(f"{Fore.RED}No number provided!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        # How many times to send
        while True:
            try:
                count = int(input(f"{Fore.WHITE}How many OTPs to send? (e.g., 5, 10, 20): {Style.RESET_ALL}"))
                if count > 0:
                    break
                else:
                    print(f"{Fore.RED}Please enter a number greater than 0{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
        
        # Delay setting
        while True:
            try:
                delay = input(f"{Fore.WHITE}Delay between requests in seconds? (Default 2): {Style.RESET_ALL}")
                if delay.strip() == "":
                    delay = 2
                    break
                delay = float(delay)
                if delay >= 0.5:
                    break
                else:
                    print(f"{Fore.RED}Delay must be at least 0.5 seconds{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
        
        # Confirmation
        print(f"\n{Fore.YELLOW}You are about to send {count} OTP(s) to {phone}")
        print(f"Delay between requests: {delay} seconds{Style.RESET_ALL}")
        
        confirm = input(f"\n{Fore.WHITE}Do you want to continue? (y/n): {Style.RESET_ALL}")
        
        if confirm.lower() == 'y':
            self.send_otp(phone, count, delay)
        else:
            print(f"{Fore.YELLOW}Cancelled{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def bulk_mode(self):
        """Multiple different numbers mode"""
        self.clear_screen()
        self.print_banner()
        
        print(f"{Fore.YELLOW}[Bulk Mode - One OTP to multiple numbers]{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Enter numbers (one per line):{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Press Enter twice to finish:{Style.RESET_ALL}\n")
        
        number_list = []
        while True:
            line = input()
            if not line:
                break
            number_list.append(line.strip())
        
        if not number_list:
            print(f"{Fore.RED}No numbers provided!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}Total {len(number_list)} numbers. Sending 1 OTP each{Style.RESET_ALL}\n")
        
        total_success = 0
        total_fail = 0
        
        for i, number in enumerate(number_list, 1):
            print(f"{Fore.CYAN}[{i}/{len(number_list)}] {number}{Style.RESET_ALL}")
            success, fail = self.send_otp(number, 1, 0)
            total_success += success
            total_fail += fail
            
            if i < len(number_list):
                print(f"{Fore.YELLOW}Moving to next number...{Style.RESET_ALL}")
                time.sleep(2)
        
        print(f"\n{Fore.GREEN}✓ All OTPs sent!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Successful: {total_success}, Failed: {total_fail}{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def run(self):
        """Main menu"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print(f"{Fore.WHITE}Main Menu:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}1.{Style.RESET_ALL} Single Mode (One OTP to one number)")
            print(f"{Fore.CYAN}2.{Style.RESET_ALL} {Fore.GREEN}Multi OTP Mode (Multiple OTPs to one number){Style.RESET_ALL}")
            print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bulk Mode (One OTP to multiple numbers)")
            print(f"{Fore.CYAN}4.{Style.RESET_ALL} Exit")
            
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1-4): {Style.RESET_ALL}")
            
            if choice == '1':
                self.single_mode()
            elif choice == '2':
                self.multi_otp_mode()
            elif choice == '3':
                self.bulk_mode()
            elif choice == '4':
                print(f"\n{Fore.GREEN}Thank you for using this tool!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
                time.sleep(2)

if __name__ == "__main__":
    try:
        tool = BioscopeOTPSender()
        tool.run()
    except ImportError:
        print("Some libraries are not installed. Please run:")
        print("pip install requests colorama")
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program stopped by user...{Style.RESET_ALL}")