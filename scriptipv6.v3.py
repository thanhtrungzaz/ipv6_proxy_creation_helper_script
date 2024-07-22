import os
import random
import ipaddress

def generate_ipv6_addresses_random(prefix, count):
    prefix_network = ipaddress.IPv6Network(prefix)
    if prefix_network.prefixlen != 64:
        raise ValueError("Префикс должен быть /64")

    addresses = set()
    while len(addresses) < count:
        suffix = random.getrandbits(64)
        ip = prefix_network.network_address + suffix
        addresses.add(ip)

    return addresses

def generate_ipv6_addresses_sequential(prefix, count):
    prefix_network = ipaddress.IPv6Network(prefix)
    if prefix_network.prefixlen != 64:
        raise ValueError("Префикс должен быть /64")

    base_address = int(prefix_network.network_address)
    addresses = []
    for i in range(count):
        ip = ipaddress.IPv6Address(base_address + i)
        addresses.append(ip)

    return addresses

def save_to_file(addresses, filename):
    with open(filename, 'w') as file:
        for address in addresses:
            file.write(str(address) + '\n')

def generate_up_down_scripts(addresses, interface, home_directory):
    up_script_path = os.path.join(home_directory, "upipv6addr.sh")
    down_script_path = os.path.join(home_directory, "downipv6addr.sh")

    with open(up_script_path, 'w') as up_file, open(down_script_path, 'w') as down_file:
        for address in addresses:
            up_file.write(f"ip -6 addr add {address} dev {interface}\n")
            down_file.write(f"ip -6 addr del {address} dev {interface}\n")

def main():
    prefix = input("Введите первые 64 бита IPv6 префикса (например, 2001:0db8:85a3::/64): ")
    count = int(input("Введите количество уникальных IPv6 адресов, которые нужно сгенерировать: "))
    mode = input("Вы хотите использовать рандомизированную генерацию или последовательную (random/sequential)? ")

    try:
        if mode.lower() == "random":
            addresses = generate_ipv6_addresses_random(prefix, count)
        elif mode.lower() == "sequential":
            addresses = generate_ipv6_addresses_sequential(prefix, count)
        else:
            raise ValueError("Неизвестный режим генерации")

        home_directory = os.path.expanduser("~")
        filename = os.path.join(home_directory, "ipv6.list")
        save_to_file(addresses, filename)
        print(f"Список IPv6 адресов сохранен в файл: {filename}")

        generate_scripts = input("Вы хотите сгенерировать up и down скрипты для добавления/удаления IPv6 адресов на интерфейс (yes/no)? ").lower()
        if generate_scripts == "yes":
            interface = input("Введите имя интерфейса (например, eth0): ")
            generate_up_down_scripts(addresses, interface, home_directory)
            print(f"Скрипты upipv6addr.sh и downipv6addr.sh сохранены в папку: {home_directory}")

    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
