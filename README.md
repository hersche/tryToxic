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
  <li><del>nr's of peers isn't right (ever 1 persons)</del></li>
  <li>this stuff i couldn't resolve for moment, but there's enough to improve :)</li>
</ul>
<b>Ideas/Future</b>
<ul>
  <li>QrCode for publickey/adress. Find no good framework which is easy to install for python 3</li>
  <li>AudioVideo - i think everyone who play/dev with tox like to got this. Big part..</li>

...etc. I've now a moment time to work on, so i think, it will get a bit more extendet soon (i've broke my feet and shouldn't move - lets dev!).
