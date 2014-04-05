<h2>tryToxics</h2><hr />
=========
<img href="https://raw.githubusercontent.com/skamster/tryToxics/master/ui/logo.jpg" alt="logo" />

..and another tox-api-client, based on pyTox and pyQt, written in pure python 3..

<h3>This project..</h3>
.. is a try. Because of that it get its initially name "toxTry" which existed as a context-free (or "nonsense") project in my repo "jobManagement".<br />
The new name should be a motivation too - there are some tox-api-clients and tox-users. "Try" them, but pls no real toxics! :)

<h3>Build-Instructions</h3>
Something more serious. You baiscly need:
<ul><li>pyQt4</li><li>pyCrypto</li><li>header/dev-Files for python 3 (needed by pyTox)</li><li><a href="https://github.com/aitjcize/PyTox">pyTox</li>
On *buntu (13.10) they're the following:
<br /> <b>sudo apt-get install python3-crypto python3-pyqt4 python3-dev</b>
Look <a href="https://github.com/irungentoo/ProjectTox-Core/blob/master/INSTALL.md#unix">here</a> for building tox-core. 
<br /> Requirements for building tox-core: <b>sudo apt-get install build-essential libtool autotools-dev automake checkinstall check git yasm</b>

<br />After installing that stuff (tox-core, libsodium, packages) stuff, clone <a href="https://github.com/aitjcize/PyTox">pyTox</a>: <br />
<b>git clone https://github.com/aitjcize/PyTox.git</b> <br />
Or just download and extract it as zip. Anyway, go into a shell and the right folder and put in<b />
<b>sudo python3 setup.py install</b> <br />
After it compiles, you should be ready, give start.sh a kick. Don't forget to update and reinstall tox-core and pyTox by hand.

<h3>Increase debug</h3>
There's a logger used to detect failures in structure (multiple used methods as example). Settings are saved in lib/header.py and setted per default on error-level.

<h3>Whats working / Bugs</h3>
Important to know: friendRequests get automatic accepted, also groupchat for debugging..<br />
<b>Working!</b>
<ul>
  <li>Add and save toxUsers, experimental support for tox-id v2</li>
  <li>"Profile"-Signals (status, statusmessage, name)</li>
  <li>Save messages/history log (encrypted, look local storages)</li>
  <li>Send and reciving messages</li>
  <li>Encryption of <a href="https://github.com/skamster/tryToxics/wiki/LocalStorages" >LocalStorages</a></li>
  <li>Internationalisised (at the moment english + german)</li>
  <li>Groupchat is working,including create groups and invite people into them</li>
  <li>Set Loglevel for console and file on the flow</li>
  <li>Grouped chatview, diffrented by colors and little heading.</li>
</ul>

<b>Not working / known Bugs</b>
<ul>
  <li>fileTransfer</li>
  <li>friends keys are weirdly shorted - crap for giving to a friend (the own is well)</li>
  <li><del>nr's of peers isn't right (ever 1 persons)</del></li>
  <li>this stuff i couldn't resolve for moment, but there's enough to improve :)</li>
</ul>
<b>Ideas/Future</b>
<ul>
  <li>QrCode for publickey/adress. Find no good framework which is easy to install for python 3</li>
  <li>AudioVideo - i think everyone who play/dev with tox like to got this. Big part..</li>
  
...etc. I've now a moment time to work on, so i think, it will get a bit more extendet soon (i've broke my feet and shouldn't move - lets dev!).
