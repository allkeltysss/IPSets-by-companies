- В **aws.txt** собраны все CIDR полученные с официального списка Amazon Web Service (AWS): https://ip-ranges.amazonaws.com/ip-ranges.json **(Для разблокировки Battlefield 6 и прочих игр стоит вводить именно этот список в запрет!)**
- Для **hetzner.txt** я использовал данные из репозитория: https://github.com/Pymmdrza/Datacenter_List_DataBase_IP/blob/mainx/Hetzner/CIDR.txt
- **cloudflare.txt** содержит ipv4 диапозоны с официальной страницы компании: https://www.cloudflare.com/ips/ **(Помогает с обходом блокировки сервисов Cloudflare, в том числе и Cloudflare WARP)**

- **ipset-all.txt** объединяет в себя CIDR'ы aws, cloudflare и hetzner.txt **(Добавляйте этот список в запрет, если хотите одновременной разблокировки Cloudflare WARP, Battlefield 6 и прочих игр/сервисов)**
___
В папке utilities лежат всякие удобные инструменты для работы со списками CIDR.
