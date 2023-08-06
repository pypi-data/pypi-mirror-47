# MyPiano

A simple terminal based piano for playing notes and MIDI files. Not TUI/GUI
available.

# Install

    pip install mypiano --user

# How to use it 

To see the help message,

```
usage: mypiano [-h] [--midifile MIDIFILE] [--note NOTE] [--duration DURATION]

MyPiano

optional arguments:
  -h, --help            show this help message and exit
  --midifile MIDIFILE, -m MIDIFILE
                        Midi file to play
  --note NOTE, -n NOTE  A note to play
  --duration DURATION, -d DURATION
                        Note duration (use it with --note)

```

When no option is given `mypiano` just play the note `A1`. 

