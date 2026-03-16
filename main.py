import getpass
import sys

from colorama import Fore, Style, init as colorama_init
import pyfiglet

import config
import modules


def print_banner():
    banner = pyfiglet.figlet_format("Red Velvet", font="slant")
    print(Fore.RED + Style.BRIGHT + banner + Style.RESET_ALL, end="")
    print(Fore.YELLOW + "     [ Educational Anonymous Messaging Tool ]")
    print("     [ For personal testing purposes only  ]" + Style.RESET_ALL)
    print()


def print_menu():
    print(Fore.CYAN + Style.BRIGHT + "  ╔══════════════════════════════════╗")
    print("  ║                                  ║")
    print("  ║   [1]  Send Anonymous SMS         ║")
    print("  ║   [2]  Send Anonymous Email        ║")
    print("  ║   [3]  Configure SMTP Settings     ║")
    print("  ║   [4]  About                       ║")
    print("  ║   [0]  Exit                        ║")
    print("  ║                                  ║")
    print("  ╚══════════════════════════════════╝" + Style.RESET_ALL)
    print()


def handle_sms():
    print(Fore.MAGENTA + "\n  ── Anonymous SMS ──" + Style.RESET_ALL)
    phone = input(Fore.WHITE + "  Enter phone number (+94XXXXXXXXX): " + Style.RESET_ALL).strip()
    if not phone:
        print(Fore.RED + "  [!] Phone number cannot be empty." + Style.RESET_ALL)
        return

    message = input(Fore.WHITE + "  Enter your message: " + Style.RESET_ALL).strip()
    if not message:
        print(Fore.RED + "  [!] Message cannot be empty." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "\n  [*] Sending SMS..." + Style.RESET_ALL)
    result = modules.send_sms(phone, message)

    if result.get("success"):
        print(Fore.GREEN + f"  [+] SMS sent successfully!" + Style.RESET_ALL)
        print(Fore.GREEN + f"  [+] Sender name: {result.get('sender_name', 'N/A')}" + Style.RESET_ALL)
        print(Fore.GREEN + f"  [+] Quota remaining: {result.get('quotaRemaining', 'N/A')}" + Style.RESET_ALL)
    else:
        error = result.get("error", result.get("message", "Unknown error"))
        print(Fore.RED + f"  [-] Failed to send SMS: {error}" + Style.RESET_ALL)
        if result.get("sender_name"):
            print(Fore.YELLOW + f"  [*] Would-be sender: {result['sender_name']}" + Style.RESET_ALL)


def handle_email():
    print(Fore.MAGENTA + "\n  ── Anonymous Email ──" + Style.RESET_ALL)

    if not config.smtp_config["email"]:
        print(Fore.RED + "  [!] SMTP not configured. Use option [3] first." + Style.RESET_ALL)
        return

    to_addr = input(Fore.WHITE + "  Enter recipient email: " + Style.RESET_ALL).strip()
    if not to_addr:
        print(Fore.RED + "  [!] Email address cannot be empty." + Style.RESET_ALL)
        return

    subject = input(Fore.WHITE + "  Enter subject: " + Style.RESET_ALL).strip()
    if not subject:
        subject = "(No Subject)"

    body = input(Fore.WHITE + "  Enter message body: " + Style.RESET_ALL).strip()
    if not body:
        print(Fore.RED + "  [!] Message body cannot be empty." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "\n  [*] Sending email..." + Style.RESET_ALL)
    success, sender_name, error = modules.send_email(to_addr, subject, body)

    if success:
        print(Fore.GREEN + f"  [+] Email sent successfully!" + Style.RESET_ALL)
        print(Fore.GREEN + f"  [+] Sender name: {sender_name}" + Style.RESET_ALL)
        print(Fore.GREEN + f"  [+] Sent to: {to_addr}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"  [-] Failed to send email: {error}" + Style.RESET_ALL)


def handle_smtp_config():
    print(Fore.MAGENTA + "\n  ── SMTP Configuration ──" + Style.RESET_ALL)
    print(Fore.YELLOW + "  [*] Leave blank to keep default values." + Style.RESET_ALL)
    print()

    host = input(f"  SMTP Host [{config.smtp_config['host']}]: ").strip()
    if host:
        config.smtp_config["host"] = host

    port_str = input(f"  SMTP Port [{config.smtp_config['port']}]: ").strip()
    if port_str:
        try:
            config.smtp_config["port"] = int(port_str)
        except ValueError:
            print(Fore.RED + "  [!] Invalid port number, keeping default." + Style.RESET_ALL)

    email = input("  Email address: ").strip()
    if email:
        config.smtp_config["email"] = email
    elif not config.smtp_config["email"]:
        print(Fore.RED + "  [!] Email is required." + Style.RESET_ALL)
        return

    password = getpass.getpass("  App password (hidden): ")
    if password:
        config.smtp_config["password"] = password
    elif not config.smtp_config["password"]:
        print(Fore.RED + "  [!] Password is required." + Style.RESET_ALL)
        return

    print(Fore.GREEN + "\n  [+] SMTP configured successfully!" + Style.RESET_ALL)
    print(Fore.GREEN + f"  [+] Host: {config.smtp_config['host']}:{config.smtp_config['port']}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  [+] Email: {config.smtp_config['email']}" + Style.RESET_ALL)


def handle_about():
    print(Fore.YELLOW + config.DISCLAIMER + Style.RESET_ALL)


def main():
    colorama_init(autoreset=True)
    print_banner()

    while True:
        print_menu()
        choice = input(Fore.WHITE + Style.BRIGHT + "  Red Velvet > " + Style.RESET_ALL).strip()

        if choice == "1":
            handle_sms()
        elif choice == "2":
            handle_email()
        elif choice == "3":
            handle_smtp_config()
        elif choice == "4":
            handle_about()
        elif choice == "0":
            print(Fore.RED + "\n  [*] Goodbye. Stay anonymous. 🌹\n" + Style.RESET_ALL)
            sys.exit(0)
        else:
            print(Fore.RED + "  [!] Invalid option. Try again." + Style.RESET_ALL)

        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [*] Interrupted. Goodbye. 🌹\n" + Style.RESET_ALL)
        sys.exit(0)
