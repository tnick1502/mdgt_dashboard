Сервис поднимает веб-сервер на порте 8000. 

Автоматически генерируется и заполняется база данных отчетов и премий, создается суперпользователь для доступа.

Для просмотра документации по API надо перейти на http://127.0.0.1:8000/docs

Установка:

1. Создать папку для проекта. Открыть папку в терминале и выполнить:
    
    git init
    git clone https://github.com/tnick1502/mdgt_dashboard.ru

2. Создать папки для связи с контейнерами:
    
    Для Linux привяжем сетевой диск к папке:
    sudo mount.cifs //192.168.0.1/files YOUR_PATH -o user=v.antonij,pass=eHar4Er9
    YOUR_PATH выбираем сами. Пример: /home/nick/projects/reports

    Для Windows ничего не делаем. Далее испозьзуем YOUR_PATH = //192.168.0.1/files

3. Можно запустить через контейнер:
    
    docker build -t mdgt_dashboard .
    docker run -v YOUR_PATH:/files -p 8000:8000 mdgt_dashboard

4. Или через docker-compose:

    docker-compose up

