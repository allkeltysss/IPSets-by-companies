import json
import requests
import ipaddress
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

output_file = "aws.txt"

try:
    # 1. Получаем СИДРы с сайта AWS
    logging.info("Downloading AWS IP ranges...")
    aws_ip_data = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json").text
    jsonfile = json.loads(aws_ip_data)
    
    amazon_ranges = jsonfile["prefixes"]
    logging.info(f"Downloaded {len(amazon_ranges)} prefixes.")

    # 2. Собираем список подсетей в памяти
    subnets = []
    seen = set()

    for item in amazon_ranges:
        cidr = item["ip_prefix"]
        try:
            net = ipaddress.IPv4Network(cidr, strict=False)
            # Пропускаем дубликаты сразу
            if net not in seen:
                seen.add(net)
                subnets.append(net)
        except ValueError as e:
            logging.error(f"Invalid subnet '{cidr}': {e}")

    # 3. Агрегация (объединение пересекающихся сетей)
    logging.info("Aggregating subnets...")
    aggregated = list(ipaddress.collapse_addresses(subnets))
    aggregated.sort(key=lambda net: int(net.network_address))

    # 4. Запись результата в файл (полная перезапись)
    with open(output_file, "w") as out_file:
        for net in aggregated:
            out_file.write(str(net) + "\n")

    logging.info(f"Success! Aggregated list written to {output_file} ({len(aggregated)} entries)")

except Exception as e:
    logging.error(f"Critical error: {e}")
    exit(1) # Выход с ошибкой, чтобы GitHub Actions увидел проблему
