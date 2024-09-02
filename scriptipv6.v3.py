import os
import random
import ipaddress

def generate_ipv6_addresses_random(prefix, count):
    prefix_network = ipaddress.IPv6Network(prefix)
    if prefix_network.prefixlen != 64:
        raise ValueError("Tiền tố phải là /64")

    addresses = set()
    while len(addresses) < count:
        suffix = random.getrandbits(64)
        ip = prefix_network.network_address + suffix
        addresses.add(ip)

    return addresses

def generate_ipv6_addresses_sequential(prefix, count):
    prefix_network = ipaddress.IPv6Network(prefix)
    if prefix_network.prefixlen != 64:
        raise ValueError("Tiền tố phải là /64")

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
    prefix = input("Nhập 64 bit đầu tiên của tiền tố IPv6 (ví dụ: 2001:0db8:85a3::/64): ")
    count = int(input("Nhập số lượng địa chỉ IPv6 duy nhất sẽ được tạo: "))
    mode = input("Bạn có muốn sử dụng tạo ngẫu nhiên hoặc tuần tự (ngẫu nhiên/tuần tự)? ")

    try:
        if mode.lower() == "random":
            addresses = generate_ipv6_addresses_random(prefix, count)
        elif mode.lower() == "sequential":
            addresses = generate_ipv6_addresses_sequential(prefix, count)
        else:
            raise ValueError("Chế độ tạo không xác định")

        home_directory = os.path.expanduser("~")
        filename = os.path.join(home_directory, "ipv6.list")
        save_to_file(addresses, filename)
        print(f"Danh sách địa chỉ IPv6 được lưu vào một tệp: {filename}")

        generate_scripts = input("Bạn muốn tạo các tập lệnh lên xuống để thêm/xóa địa chỉ IPv6 trên một giao diện (yes/no)? ").lower()
        if generate_scripts == "yes":
            interface = input("Nhập tên giao diện (ví dụ: eth0): ")
            generate_up_down_scripts(addresses, interface, home_directory)
            print(f"Các tập lệnh upipv6addr.sh và downipv6addr.sh được lưu trong thư mục: {home_directory}")

    except ValueError as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
