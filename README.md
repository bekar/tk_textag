# tk-textag

An extension for the [vtk100-colors][vtk100-colors], to enable and disable the color-tags, cool way huh!

![screenshot][screenshot]

#### HOW-TO-RUN

Yes, you will need [vtk100-colors][vtk100-colors] which is included in submodule.

```bash
$ git submodule init
$ git submodule update
```

to run it:

```bash
$ ./main.py <any command with color output>
```

Some example simple examples can be found in `make`:

```bash
$ make
make [hello|ls]
```

#### Read more

 - [ANSI color][ansi]
 - [256 color chart][chart]
 - [Ecma-048][ecma]
 - [VT100][vt100]

[vt100]: http://en.wikipedia.org/wiki/VT100
[ecma]: http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-048.pdf
[screenshot]: https://raw.github.com/bekar/tk-textag/dump/images/screenshot.png
[vtk100-colors]: https://github.com/bekar/vtk100-colors
[extreme]: https://raw.github.com/bekar/vtk100-colors/dump/samples/colorextreme
[chart]: http://www.calmar.ws/vim/256-xterm-24bit-rgb-color-chart.html
[ansi]: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
