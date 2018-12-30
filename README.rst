GBF Bot
~~~~~~~
It's kind of lazy to do the same thing again and again.
It's not interesting and boring.
Why not let the computer to do these things for us?
That's how this robot being born.

For acdemic research use.  Use it at your own risk.

Development Environment
=======================
* Python 3.7.0
* PyAutoGUI 0.9.38
* OpenCV 3.3.0
* NumPy 1.15.4
* macOS Sierra 10.12.6

Mac users have to install ``pyobjc-core`` and ``pyobjc`` additionally.

Environment
===========
* Screen resolution: 1080p (1920 x 1080)
* Granblue fantasy: AndApp version
* Application position: alignment top-right
* Application size: middle (choose 2 diamond in the bottom)

Configuration
=============
Enter parameters in the ``gbf_bot/config.ini``.
If you have the same environment as me,
all you need to do is change the ``battle time``.

Enter the summon you want to use in the ``summon name``.

You could use ``mouse_now.py`` to capture the coordinate of mouse.

Summon Support List
-------------------
These are currently supported summon list:

* apollo
* baal
* bahamut
* celeste omega
* celeste omega 4(★)
* dark angel olivia
* europa
* godsworn alexiel
* kaguya
* leviathan omega
* lucifer
* macula marius
* medusa
* odin
* tezcatlipoca
* white rabbit

Usage
=====
Make sure you have enough AP, then execute ``run.py``.

Warning: If captcha popup, you have to handle it manually,
or you will be banned.

Favorites Mission
-----------------
* Just put the mission you want to auto-play in the top of favorites.
* If **Nightmare: Dimension Halo** pop up,
  program will terminate automatically.

Slime Blasting
--------------
* Set everything ready before blasting.

Poker Bot
---------
* Enter poker play page first.
* The default play time is 30 minutes (1800 seconds).
  
Guild Wars EXTREME+
-------------------
* First, enter guild wars page, and select AndApp windows immediately
  after select guild wars ex+.
* You can create your battle behaviors in ``guild_wars.ini`` manually.
