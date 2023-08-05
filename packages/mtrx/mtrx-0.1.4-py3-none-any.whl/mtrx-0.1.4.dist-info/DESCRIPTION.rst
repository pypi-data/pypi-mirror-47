MTRX
=====

A Python ToolBox for Python Programmers

Author Website :  https://mostafa-vn.ir/

Features
=============
 * works with Python 3.x
 * to easy
 * possibility to cache results


$ pip3 install mtrx
===================

>>> import mtrx

>>> mtrx.sendgmail(username='yourGmail', password='yourPassword', to='toGmail', text='yourText')
Sending Gmail

>>> mtrx.qrcode(text='mtrx.ir', Format='svg')     # Formats are svg, eps, terminal
Creating QRcode

>>> print(mtrx.DNS(url='mtrx.ir'))
Website DNS

>>> mtrx.download(url='fileURL')
Download a file

>>> mtrx.screensh()
getting screen shot

>>> print(mtrx.myip())
Your IP

>>> print(mtrx.timeNow())
>>> print(mtrx.dateNow())
Get Time And Date



get Information from mtrx

>>> mtrx.__author__
'Mostafa Vahedi Nejad'

>>> mtrx.__website__
'https://mostafa-vn.ir'

>>> mtrx.__version__
'0.0.5'


