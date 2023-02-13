#!/usr/bin/env python3

import os
import platform
import socket
import requests
import psutil
import time
import subprocess

def main_menu():
    print("\033[4;36m\nWybierz opcję:\033[0;0m")
    print("\n1. Sprawdzenie wydania systemu")
    print("2. Pokaż hostname")
    print("3. Sprawdzenie dostępnej przestrzeni dyskowej")
    print("4. Sprawdzenie adresu IP lokalnego")
    print("5. Sprawdzenie adresu IP publicznego")
    print("6. Proces z największym zużyciem pamięci")
    print("7. Uptime systemu")
    print("8. Sprawdzenie dostępnych aktualizacji")
    print("9. Test prędkości internetu")
    print("10. Neofetch")
    print("11. Wyjście")
    choice = int(input("\033[1;36m\nWybierz opcję (1-11):\033[0;0m"))
    return choice

def check_release():
    os_release = os.popen("cat /etc/os-release").read()
    print("\033[1;34m\nWydanie systemu:\n\n", os_release)
    print("\033[0;0m")
    
def display_hostname():
    hostname = os.uname()[1]
    print("\033[1;34m\nHostname:\n\n", hostname)
    print("\033[0;0m")
    main_menu()    

def check_disk_space():
    disk_space = os.statvfs("/")
    available = disk_space.f_frsize * disk_space.f_bavail
    available_gb = available / (1024.0 ** 3)
    available_mb = available / (1024.0 ** 2)
    print("\033[1;34m\nDostępne miejsce na dysku: {:.2f} GB".format(available_gb))
    print("Dostępne miejsce na dysku: {:.2f} MB".format(available_mb))
    print("\033[0;0m")

def check_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("\033[1;34m\nAdres IP:", ip)
    print("\033[0;0m")

def check_public_ip():
    response = requests.get("https://api.ipify.org")
    public_ip = response.text
    print("\033[1;34m\nPubliczny adres IP:", public_ip)
    print("\033[0;0m")

def check_process_memory():
    processes = list(psutil.process_iter())
    process_memory = [(process.pid, process.memory_info().rss) for process in processes]
    process_memory.sort(key=lambda x: x[1], reverse=True)
    top_process = psutil.Process(process_memory[0][0])
    print("\033[1;34m\nProces z największym zużyciem pamięci:")
    print("Nazwa procesu:", top_process.name())
    print("Zużycie pamięci:", top_process.memory_info().rss / (1024 ** 2), "MB")
    print("\033[0;0m")

def check_uptime():
    uptime = int(time.time() - psutil.boot_time())
    uptime_minutes, uptime_seconds = divmod(uptime, 60)
    uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)
    uptime_days, uptime_hours = divmod(uptime_hours, 24)
    print("\033[1;34m\nUptime systemu:")
    print("{} dni, {} godzin, {} minut, {} sekund".format(uptime_days, uptime_hours, uptime_minutes, uptime_seconds))
    print("\033[0;0m")

def check_updates():
    result = os.popen("sudo apt update && sudo apt list --upgradable").read()
    print("\033[1;34m\nWynik komendy 'sudo apt update && sudo apt list --upgradable':\n\n", result)
    print("\033[0;0m")
    update_confirmation = input("\033[1;34m\nCzy chcesz wykonać aktualizację? (tak/nie)\033[0;0m")
    if update_confirmation.lower() == "tak":
        os.system("sudo apt upgrade")
        print("\033[1;34m\nAktualizacja zakończona\033[0;0m")
    else:
        print("\033[1;31m\nAnulowanie aktualizacji\033[0;0m")
        
def check_internet_speed():
    result = os.popen("speedtest-cli --no-upload 2>&1").read()
    if "not found" in result:
        install_confirmation = input("\033[1;31m\nNarzędzie speedtest-cli nie jest zainstalowane. Czy chcesz je zainstalować i wykonać test prędkości internetu? (tak/nie)\033[0;0m")
        if install_confirmation.lower() == "tak":
            process = subprocess.Popen(["sudo", "apt", "install", "-y", "speedtest-cli"], stdout=subprocess.PIPE)
            print("\033[1;34m\nInstalowanie narzędzia, proszę czekać...\033[0;0m")
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode("utf-8"))
            result = os.popen("speedtest-cli --no-upload").read()
            print("\033[1;34m\nWynik testu prędkości internetu:\n\n", result)
            print("\033[0;0m")
        else:
            print("\033[1;31m\nAnulowanie instalacji narzędzia\033[0;0m")
    else:
        print("\033[1;34m\nWynik testu prędkości internetu:\n\n", result)
        print("\033[0;0m")
    repeat_confirmation = input("\033[1;33m\nCzy chcesz powtórzyć test prędkości internetu? (tak/nie)\033[0;0m")
    if repeat_confirmation.lower() == "tak":
        check_internet_speed()
    else:
        main_menu()
        
def run_neofetch():
    result = os.popen("neofetch 2>&1").read()
    if "not found" in result:
        install_confirmation = input("\033[1;31m\nNeofetch nie jest zainstalowane. Czy chcesz je zainstalować i uruchomić? (tak/nie)\033[0;0m")
        if install_confirmation.lower() == "tak":
            process = subprocess.Popen(["sudo", "apt", "install", "-y", "neofetch"], stdout=subprocess.PIPE)
            print("\033[1;34m\nInstalowanie neofetch, proszę czekać...\033[0;0m")
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode("utf-8"))
            result = os.popen("neofetch").read()
            print("\033[1;34m\nNeofetch:\n\n", result)
            print("\033[0;0m")
        else:
            print("\033[1;31m\nAnulowanie instalacji neofetch\033[0;0m")
    else:
        print("\033[1;34m\n=):\n\n", result)
        print("\033[0;0m")
        main_menu()

while True:
    choice = main_menu()
    if choice == 1:
        check_release()
    elif choice == 2:
        display_hostname()
    elif choice == 3:
        check_disk_space()
    elif choice == 4:
        check_ip()
    elif choice == 5:
        check_public_ip()
    elif choice == 6:
        check_process_memory()
    elif choice == 7:
        check_uptime()
    elif choice == 8:
        check_updates()
    elif choice == 9:
        check_internet_speed()
    elif choice == 10:
        run_neofetch()        
    elif choice == 11:
        break
    else:
        print("\033[1;31m\nNieprawidłowa opcja, wybierz ponownie\033[0;0m")
