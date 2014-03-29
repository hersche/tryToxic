<h2>tryToxics</h2><hr />
=========
<img href="ui/logo.jpg" alt="logo" />

..and another tox-api-client, based on pyTox and pyQt, written in pure python 3..

<h3>This project..</h3>
.. is a try. Because of that it get its initially name "toxTry" which existed as a context-free (or "nonsense") project in my repo "jobManagement".<br />
The new name should be a motivation too - there are some tox-api-clients and tox-users. "Try" them, but pls no real toxics! :)

<h3>Build-Instructions</h3>
Something more serious. You baiscly need:
<ul><li>pyQt4</li><li>pyCrypto</li><li>header/dev-Files for python 3 (needed by pyTox)</li><li><a href="https://github.com/aitjcize/PyTox">pyTox</li>
On *buntu (13.10) they're the following:
<br /> <b>sudo apt-get install python3-crypto python3-pyqt4 python3-dev</b>
<br />After installing that stuff, clone pyTox: <br />
<b>git clone https://github.com/aitjcize/PyTox.git</b> <br />
Or just download and extract it as zip. Anyway, go into a shell and the right folder and put in<b />
<b>sudo python3 setup.py install</b> <br />
After it compiles, you should be ready, give start.sh a kick. Don't forget to update and reinstall this lib by hand.

<h3>Whats working / Bugs</h3>
Important to know: friendRequests get automatic accepted, also groupchat for debugging..<br />
<b>Working!<b>
<ul>
  <li>Add and save toxUsers</li>
  <li>"Profile"-Signals (status, statusmessage, name)</li>
  <li>Save messages/history log</li>
  <li>Send and reciving messages</li>
</ul>

<b>Not working / known Bugs</b>
<ul>
  <li>Status (backgroundcolor in friendlist) shows always online</li>
  <li>Encryption is incomplete and fucks around (padding is not right anymore)-when u want to use it, take arc4 or xor to encrypt, they should work.</li>
  <li>It's easy possible to kill the app, when you don't wait, until it's really connectet to a user and stress it around</li>
  <li>language has to be fixed</li>
</ul>
...etc. I've now a moment time to work on, so i think, it will get a bit more extendet soon (i've broke my feet and shouldn't move - lets dev!).