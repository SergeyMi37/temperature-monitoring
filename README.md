# Проверка температуры и посылка уведомления в телегамм, если ниже пороговой
На Raspberry pi запущен сервис регулярного чтения датчика температуры (на питоне) и посылки сообщения в телегу моему боту. Малинка на даче включена в локальную сеть. Температурный датчик DS18B20 с резистом 4.7к спаен и прикручен к 4 пину Raspberry pi.
Проект долгострой (более5 лет) завершен в первой итерации.

# Инструкция по запуску

1. python -v venv <venv_name>
2. source venv_name/bin/activate # (`deactivate`)
3. pip install -r requirements.txt
4. Реактировать файл конфигурации `check-send.yml`
```
# Параметры
version: '1.0.0'

# выводить регульное сообщение в бот
dubug_print: yes
# периодичность опроса датчика в секундах
#timeout: 3600
timeout: 15
# Минимальный порог уведомления в градусах цельсия
min_threshold: 15
# Максмальный порог уведомления в градусах цельсия
max_threshold: 25


# Параметры телебота
token: 1111111
chat_id: 1111111

# Параметры датчика
# путь к файлу
#dirbus1w: /tmp/
dirbus1w: temp-test.txt
```


# Можно написать демон для systemd, если в вашей операционной системе он используется.

Создаём файл демона:
sudo touch /etc/systemd/system/bot.service

## Вставляем туда следующее:
```
[Unit]
Description=My bot
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /путь/до/скрипта/check-send.py.py
Restart=always
 
[Install]
WantedBy=multi-user.target
```

## После этого в консоли выполяем:
sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl start bot.service


## Чтобы остановить бот:
sudo systemctl stop bot.service
## Чтобы удалить из автозагрузки:
sudo systemctl disable bot.service
## Чтобы проверить работу демона:
sudo systemctl status bot.service

# Благодарности
https://myraspberrypi.ru/2018/10/24/%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-ds18b20-%D0%BA-raspberry-pi/
https://qna.habr.com/q/520860
http://slugg.spb.ru/ubuntu/ubuntu_setting/36-ubuntu-server-i-set-1-wire.html
https://sameak.ru/nastrojka-i-ispolzovanie-shiny-1-wire-na-raspberry-pi-3b-s-serverom-owserver/

