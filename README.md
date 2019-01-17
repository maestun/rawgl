
# raw(gl) - Another World Interpreter - Switch Port

rawgl is a re-implementation of the engine used in the game Another World.

![Screenshot Intro Amiga](docs/screenshot-intro-amiga.png) ![Screenshot Intro 3DO](docs/screenshot-intro-3do.png)

## Supported Versions

The program requires the original data files.

- Amiga (Bank*)
- DOS (Bank*, memlist.bin)
- DOS demo (Demo*, memlist.bin)
- 15th Anniversary Edition (Pak01.pak, Intro2004.wav, End2004.wav)
- 20th Anniversary Edition (game/*)
- Windows 3.1 (Bank, *mid)
- 3DO (GameData/*)
- Macintosh (File*, *pict)

## Running

By default, the engine tries to load the game data files from the current
directory. This can be changed with command line switches.

```
  Usage: rawgl [OPTIONS]...
    --datapath=PATH   Path to data files (default '.')
    --language=LANG   Language (fr,us,de,es,it)
    --part=NUM        Game part to start from (0-35 or 16001-16009)
    --render=NAME     Renderer (original,software,gl)
    --window=WxH      Windowed displayed size (default '640x480')
    --fullscreen      Fullscreen display (stretched)
    --fullscreen-ar   Fullscreen display (4:3 aspect ratio)
    --ega-palette     Use EGA palette with DOS version
```

In game hotkeys :

```
  Arrow Keys      move Lester
  Enter/Space     run/shoot
  C               enter a code to start at a specific position
  P               pause the game
  Alt X           exit the game
```

## Technical Details

- [3DO](docs/3DO.md)
- [WiiU](docs/WiiU.md)
