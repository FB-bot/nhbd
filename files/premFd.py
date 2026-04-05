import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import time
import sys
import os

visited = set()

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ======================
# COLOR STYLE
# ======================

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# ======================
# ANIMATION FUNCTIONS
# ======================

def type_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading(text):
    for _ in range(3):
        sys.stdout.write(f"\r{text}.  ")
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write(f"\r{text}.. ")
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write(f"\r{text}...")
        sys.stdout.flush()
        time.sleep(0.3)
    print()

# ======================
# HACKER BANNER
# ======================

os.system("clear")

print(GREEN + r"""
 
 
   _   _  ___   ___  ______  ____     ___   _   _ 
 | \ | |/ _ \ / _ \| __ ) \/ /\ \   / / \ | | | |
 |  \| | | | | | | |  _ \\  /  \ \ / / _ \| | | |
 | |\  | |_| | |_| | |_) /  \   \ V / ___ \ |_| |
 |_| \_|\___/ \___/|____/_/\_\   \_/_/   \_\___/ 
                                                 
 
 
""" + RESET)

type_print(CYAN + "[ SYSTEM INITIALIZING ]" + RESET)
loading("Booting modules")
type_print(RED + "[ OK ] Scanner Ready\n" + RESET)

# ======================
# GET PARAMETERS FROM URL
# ======================

def find_url_params(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if params:
        print(GREEN + "\n[+] URL Parameters Found:" + RESET)
        for k, v in params.items():
            print(YELLOW + f"   -> {k} = {v[0]}" + RESET)


# ======================
# FORM PARAMETER FINDER
# ======================

def find_forms(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        forms = soup.find_all("form")

        if forms:
            print(GREEN + f"\n[+] Forms Detected: {len(forms)}" + RESET)

        for form in forms:

            action = form.get("action")
            method = form.get("method", "GET").upper()

            action_url = urljoin(url, action)

            print(CYAN + "\n--- FORM TARGET ---" + RESET)
            print(YELLOW + f"Action : {action_url}")
            print(f"Method : {method}" + RESET)

            inputs = form.find_all("input")

            for inp in inputs:
                name = inp.get("name")
                typ = inp.get("type")

                if name:
                    print(GREEN + f"Input -> {name} ({typ})" + RESET)

    except:
        print(RED + "[!] Form parsing failed" + RESET)



# CRAWLER


def crawl(url, depth=1):

    if depth == 0 or url in visited:
        return

    visited.add(url)

    type_print(CYAN + f"\n[ SCANNING ] {url}" + RESET, 0.01)

    find_url_params(url)
    find_forms(url)

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a", href=True)

        for link in links:
            new_url = urljoin(url, link["href"])

            if urlparse(new_url).netloc == urlparse(url).netloc:
                crawl(new_url, depth - 1)

    except:
        print(RED + "[!] Crawl blocked by target" + RESET)


# ======================
# START SCAN
# ======================

target = input(GREEN + "TARGET >>> " + RESET)

loading("Connecting to target")

crawl(target, depth=2)

type_print(GREEN + "\n[✓] SCAN COMPLETE" + RESET)
type_print(CYAN + "[ SESSION TERMINATED ]" + RESET)