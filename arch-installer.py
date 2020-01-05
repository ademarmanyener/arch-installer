#!/usr/bin/env python3
import os, sys

def pr(text):
    print("==> "+text.upper())

class arch_installer:
    def set_keyboard_layout(self): 
        keyboard_layout = input("==> ENTER YOUR KEYBOARD LAYOUT (ENTER list FOR LIST): ")
        if keyboard_layout == "list":
            os.system("ls /usr/share/kbd/keymaps/**/*.map.gz")
        else:
            os.system("loadkeys "+keyboard_layout)
        return

    def verify_boot_mode(self):
        os.system("ls /sys/firmware/efi/efivars")
        return

    def update_system_clock(self):
        os.system("timedatectl set-ntp true")
        return

    def partition_disk(self):
        pr("better you create boot, swap and main!")
        os.system("cfdisk")
        return

    def format_partitions(self):
        pr("this is going to format parts as ext4!")
        boot_part = input("BOOT PART: ")
        boot_label = input("BOOT LABEL: ")
        swap_part = input("SWAP PART: ")
        swap_label = input("SWAP LABEL: ")
        main_part = input("MAIN PART: ")
        main_label = input("MAIN LABEL: ")
        os.system("mkfs.ext4 "+boot_part+" -L "+boot_label)
        os.system("mkswap "+swap_part+" -L "+swap_label)
        os.system("swapon "+swap_part)
        os.system("mkfs.ext4 "+main_part+" -L "+main_label)
        mount_option = input("DO YOU WANT TO MOUNT DISKS? [y/n] ")
        if mount_option == "y":
            os.system("mount "+main_part+" /mnt")
            os.system("mkdir /mnt/boot/")
            os.system("mount "+boot_part+" /mnt/boot/")
        return

    def select_mirrors(self):
        os.system("cat values/mirrorlist.txt > /etc/pacman.d/mirrorlist")
        return

    def install_essential_packages(self):
        os.system("scripts/essential_packages.sh")
        return

    def fstab(self):
        os.system("genfstab -U /mnt >> /mnt/etc/fstab")
        return

    def chroot(self):
        os.system("arch-chroot /mnt")
        return

    def timezone(self):
        region = input("ENTER YOUR REGION: ")
        city = input("ENTER YOUR CITY: ")
        os.system("ln -sf /usr/share/zoneinfo/"+region+"/"+city+" /etc/localtime")
        os.system("hwclock --systohc")
        return

    def localization(self):
        os.system("vim /etc/locale.gen")
        locale = input("ENTER YOUR LOCALE (like: en_US.UTF-8 or tr_TR.UTF-8):")
        keyboard_layout = input("ENTER YOUR KEYBOARD LAYOUT (like: de-latin1 or tr): ")
        os.system("echo LANG="+locale+" > /etc/locale.conf")
        os.system("echo KEYMAP="+keyboard_layout+" > /etc/vconsole.conf")
        return

    def hostname(self):
        hostname = input("ENTER HOSTNAME FOR YOUR COMPUTER: ")
        os.system("echo "+hostname+" > /etc/hostname")
        os.system("cat notes/hosts.txt")
        return

    def initramfs(self):
        os.system("mkinitcpio -P")
        return

    def root_password(self):
        os.system("passwd")
        return
    
    def grub_boot_loader(self):
        architecture = input("legacy OR uefi? ")
        os.system("pacman -S grub os-prober")
        if architecture == "legacy":
            os.system("grub-install --target=i386-pc /dev/sda")
        elif architecture == "uefi":
            os.system("grub-install --target=x86_64-efi --efi-directory=esp --bootloader-id=GRUB")
        os.system("grub-mkconfig -o /boot/grub/grub.cfg")
        return

def main():
    arch = arch_installer()
    pr("1 - set keyboard layout")
    pr("2 - verify boot mode")
    pr("3 - update system clock")
    pr("4 - partition disk")
    pr("5 - format partitions")
    pr("6 - select mirrors")
    pr("7 - install essential packages")
    pr("8 - fstab")
    pr("9 - chroot")
    pr("10 - timezone")
    pr("11 - localization")
    pr("12 - hostname")
    pr("13 - initramfs")
    pr("14 - root password")
    pr("15 - grub boot loader")
    selection = input(" $ WHAT'S YOUR SELECTION? ")
    if selection == "1":
        arch.set_keyboard_layout()
    if selection == "2":
        arch.verify_boot_mode()
    if selection == "3":
        arch.update_system_clock()
    if selection == "4":
        arch.partition_disk()
    if selection == "5":
        arch.format_partitions()
    if selection == "6":
        arch.select_mirrors()
    if selection == "7":
        arch.install_essential_packages()
    if selection == "8":
        arch.fstab()
    if selection == "9":
        arch.chroot()
    if selection == "10":
        arch.timezone()
    if selection == "11":
        arch.localization()
    if selection == "12":
        arch.hostname()
    if selection == "13":
        arch.initramfs()
    if selection == "14":
        arch.root_password()
    if selection == "15":
        arch.grub_boot_loader()

if sys.platform == "linux" and __name__ == "__main__":
    main()
