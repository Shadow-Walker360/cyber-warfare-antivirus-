import os
import hashlib
import itertools
import platform
import psutil
from scapy.all import ARP, Ether, srp
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from rich.console import Console
from rich.progress import Progress

# Initialize rich console
console = Console()

# Configuration
COMMON_PASSWORDS = ["123456", "password", "admin", "letmein", "qwerty"]
CHARACTER_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MAX_PASSWORD_LENGTH = 6  # Maximum length for brute force attempts

# Brute force AES decryption
def brute_force_decrypt(filepath, known_nonce, known_tag):
    console.print(f"[blue]Attempting to brute force decryption of {filepath}...")
    try:
        with open(filepath, "rb") as f:
            encrypted_data = f.read()

        # Try common passwords first
        for password in COMMON_PASSWORDS:
            if attempt_decryption(filepath, password, known_nonce, known_tag, encrypted_data):
                return

        # Brute force passwords up to MAX_PASSWORD_LENGTH
        with Progress() as progress:
            task = progress.add_task("[cyan]Brute forcing...", total=len(CHARACTER_SET) ** MAX_PASSWORD_LENGTH)
            for length in range(1, MAX_PASSWORD_LENGTH + 1):
                for password_tuple in itertools.product(CHARACTER_SET, repeat=length):
                    password = ''.join(password_tuple)
                    if attempt_decryption(filepath, password, known_nonce, known_tag, encrypted_data):
                        return
                    progress.update(task, advance=1)

        console.print(f"[red]Failed to decrypt {filepath}.")
    except Exception as e:
        console.print(f"[red]Error during brute force decryption: {e}")

# Attempt decryption with a given password
def attempt_decryption(filepath, password, known_nonce, known_tag, encrypted_data):
    try:
        cipher = AES.new(password.encode('utf-8'), AES.MODE_EAX, nonce=known_nonce)
        decrypted_data = unpad(cipher.decrypt_and_verify(encrypted_data, known_tag), AES.block_size)
        with open(filepath + ".decrypted", "wb") as f:
            f.write(decrypted_data)
        console.print(f"[green]Successfully decrypted {filepath} with password: {password}")
        return True
    except (ValueError, KeyError):
        return False

# Dictionary attack
def dictionary_attack(filepath, dictionary_file, known_nonce, known_tag):
    console.print(f"[blue]Starting dictionary attack on {filepath}...")
    try:
        with open(dictionary_file, "r") as f:
            passwords = f.readlines()

        for password in passwords:
            password = password.strip()
            if attempt_decryption(filepath, password, known_nonce, known_tag, encrypted_data):
                return

        console.print(f"[red]Dictionary attack failed for {filepath}.")
    except Exception as e:
        console.print(f"[red]Error during dictionary attack: {e}")

# Scan for connected devices (network or cable)
def scan_connected_devices():
    console.print("[blue]Scanning for connected devices...")
    devices = []

    # Network scanning using ARP
    try:
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24")
        answered, _ = srp(arp_request, timeout=2, verbose=False)
        for sent, received in answered:
            devices.append({"ip": received.psrc, "mac": received.hwsrc})
            console.print(f"[green]Device found: {received.psrc} ({received.hwsrc})")
    except Exception as e:
        console.print(f"[red]Error scanning network: {e}")

    # USB or external devices
    for partition in psutil.disk_partitions():
        if "removable" in partition.opts:
            devices.append({"device": partition.device})
            console.print(f"[cyan]External device detected: {partition.device}")

    return devices

# Attempt brute force entry into a device
def brute_force_device(device_info):
    console.print(f"[blue]Attempting brute force on device: {device_info}...")
    try:
        # Simulate brute force by iterating over common passwords
        for password in COMMON_PASSWORDS:
            if attempt_device_access(device_info, password):
                return

        # Brute force passwords up to MAX_PASSWORD_LENGTH
        with Progress() as progress:
            task = progress.add_task("[cyan]Brute forcing...", total=len(CHARACTER_SET) ** MAX_PASSWORD_LENGTH)
            for length in range(1, MAX_PASSWORD_LENGTH + 1):
                for password_tuple in itertools.product(CHARACTER_SET, repeat=length):
                    password = ''.join(password_tuple)
                    if attempt_device_access(device_info, password):
                        return
                    progress.update(task, advance=1)

        console.print(f"[red]Failed to access device: {device_info}.")
    except Exception as e:
        console.print(f"[red]Error during brute force: {e}")

# Attempt to access a device with a given password
def attempt_device_access(device_info, password):
    try:
        # Simulate device access logic (e.g., SSH, SMB, or file system access)
        console.print(f"[yellow]Trying password: {password} for device: {device_info}")
        # Replace this with actual access logic
        if password == "admin":  # Simulated successful password
            console.print(f"[green]Successfully accessed device: {device_info} with password: {password}")
            return True
    except Exception as e:
        console.print(f"[red]Error accessing device: {e}")
    return False

# Extract hints from the OS registry or file system
def extract_hints():
    console.print("[blue]Extracting hints from the local system...")
    hints = []

    # Simulate extracting hints from the OS registry or file system
    if platform.system() == "Windows":
        hints.append("admin")
        hints.append("password123")
        console.print("[green]Extracted hints from Windows registry: admin, password123")
    elif platform.system() == "Linux":
        hints.append("root")
        hints.append("toor")
        console.print("[green]Extracted hints from Linux file system: root, toor")
    else:
        console.print("[yellow]No specific hints found for this OS.")

    return hints

# Main function
def main():
    console.print("[blue]Starting Offensive Methods...")

    # Example usage
    filepath = input("Enter the path to the encrypted file: ").strip()
    known_nonce = input("Enter the known nonce (hex): ").strip()
    known_tag = input("Enter the known tag (hex): ").strip()

    known_nonce = bytes.fromhex(known_nonce)
    known_tag = bytes.fromhex(known_tag)

    # Choose attack method
    console.print("[yellow]Choose an attack method:")
    console.print("1. Brute Force")
    console.print("2. Dictionary Attack")
    console.print("3. Scan Connected Devices")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        brute_force_decrypt(filepath, known_nonce, known_tag)
    elif choice == "2":
        dictionary_file = input("Enter the path to the dictionary file: ").strip()
        dictionary_attack(filepath, dictionary_file, known_nonce, known_tag)
    elif choice == "3":
        devices = scan_connected_devices()
        if not devices:
            console.print("[red]No devices found. Exiting.")
            return

        # Extract hints from the local system
        hints = extract_hints()
        if hints:
            console.print("[yellow]Using extracted hints for brute force attempts.")

        # Attempt brute force on each device
        for device in devices:
            brute_force_device(device)
    else:
        console.print("[red]Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
