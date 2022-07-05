# Dashboard MDGT

Запускается как набор микросервисов.

Сервисы:
* service_bot - Асинхронный бот. Парсит данные по запросам и в канал.
* service_organization - Сервис собирает и обновляет данные по премии, отчетам и сотрудникам.
* service_customer - Сервис собирает и обновляет данные по заказчикам.

Работает с сетевым диском компании. Для работы надо подключить диск к папке.

## Запуск:
1. Создать папку для проекта. Открыть папку в терминале и выполнить:
    `git init git clone https://github.com/tnick1502/mdgt_dashboard.git`

2. Подключение диска:
    Для Linux привяжем сетевой диск к папке:
    `sudo mount.cifs ip_диска/files YOUR_PATH -o user=пользователь,pass=пароль`
    
    YOUR_PATH выбираем сами. Пример: 
    `/home/nick/projects/reports`

    Для Windows ничего не делаем. Далее испозьзуем `YOUR_PATH = ip_диска/files`

3. Создать структуру папок:
   `-/home/database/
      -customers
         -customers.xlsx         
         -photos
            -1/pick1.jpg....
            -2/pick1.jpg....
      -organization
         -staff.xlsx`
    В папке photos хранятся фото заказчиков c именами по id в формате jpg.
    Файлы staff.xlsx и customers.xlsx хранятся в папке data.

4. Запуск через docker-compose
    `docker-compose up`
