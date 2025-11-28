import json
import requests
import ipaddress
import logging
import os

# Получаем СИДРы с сайта AWS и записываем их в aws_raw.txt
aws_ip_data = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json").text
jsonfile = json.loads(aws_ip_data)

amazon_ranges = [item for item in jsonfile["prefixes"]]

for cidr in amazon_ranges:
    open("aws.txt", "a").write(f"{cidr["ip_prefix"]}\n")

# Фильтруем СИДРы и записываем в файл aws_filtered.txt
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

input_file = "aws.txt"
output_file = "aws.txt"

with open(input_file) as file:
  raw_lines = [line.strip() for line in file if line.strip()]

logging.info(f"Loaded {len(raw_lines)} entries from {input_file}")

subnets = []
seen = set()
for line in raw_lines:
  try:
    net = ipaddress.IPv4Network(line, strict=False)
    if net in seen:
      logging.warning(f"Duplicate found and skipped: {net}")
    else:
      seen.add(net)
      subnets.append(net)
  except ValueError as e:
    logging.error(f"Invalid subnet '{line}': {e}")

aggregated = list(ipaddress.collapse_addresses(subnets))
aggregated.sort(key=lambda net: int(net.network_address))

with open(output_file, "w") as out_file:
  for net in aggregated:
    out_file.write(str(net) + "\n")

logging.info(f"Aggregated list written to {output_file} ({len(aggregated)} entries)")

input("\nНажмите Enter для выхода...")
