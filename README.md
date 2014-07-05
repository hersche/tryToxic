<h2>tryToxics</h2><hr />
=========
<img src="https://raw.githubusercontent.com/skamster/tryToxics/master/ui/logo.jpg" alt="logo" width="40%" height="40%" />

..and another tox-api-client, based on pyTox and pyQt, written in pure python 3..

<h3>This project..</h3>
.. is a try. Because of that it get its initially name "toxTry" which existed as a context-free (or "nonsense") project in my repo "jobManagement".<br />
The new name should be a motivation too - there are some tox-api-clients and tox-users. "Try" them, but pls no real toxics! :)

<h3>Build-Instructions</h3>
For *buntu, you could just make buildDepsBuntu.sh executable and start it by <br />
<b>./buildDepsBuntu.sh install</b>
<br />When you like to update, you just could <br />
<b>./buildDepsBuntu.sh update</b>

After it the dependencies compiled, you should be ready. Give start.sh a kick. Don't forget to update and reinstall tox-core and pyTox by hand.

<h3>Dev-infos</h3>
<ul><li>Go to settings for debug-levels</li>
<li><a href="http://skamster.github.io/tryToxicDocs/">Go here for source-docs</a></li>
<li>Have a look into wiki for descriptions</li>
</ul>
<h3>Whats working</h3>
<del>Important to know: friendRequests get automatic accepted, also groupchat for debugging..</del> Deprecated, you will be asked for everything!<br />
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
  <li>The encryption for the local storage from "Project tox-core" gets splitted into a seperate lib which isn't avaible to python yet. Because of i want 
to provide encryption for local data, i work on two new methods to de- and encrypt all kind of files, what makes the project independend in this point. 
Look into wiki, http://piratepad.net/fileEncryption (posted in diaspora) and the file lib/cryptClass.py for changes and join, if you like to (for 
auditing, development, forking or using, when it works). If the class gets avaible, it could be activated too, as a hardening. i also will not remove the 
sql-data-based encryption, so you will be able to choose at least two algorithms (nice thing would be to increase it to many algos on both kinds of 
encryption). </li>
  <li>this stuff i couldn't resolve for moment, but there's enough to improve :)</li>
</ul>
<b>Ideas/Future</b>
<ul>
  <li>QrCode for publickey/adress. Find no good framework which is easy to install for python 3</li>
  <li>AudioVideo - i think everyone who play/dev with tox like to got this. Big part..</li>

...etc. I've now a moment time to work on, so i think, it will get a bit more extendet soon (i've broke my feet and shouldn't move - lets dev!).
