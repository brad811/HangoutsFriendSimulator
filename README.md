# HangoutsFriendSimulator

Parses your Google Hangouts conversations export file and simulates the people you talk to using Markov chains.

You can export your Google Hangouts conversation history here: https://takeout.google.com/settings/takeout

## Usage

```
usage: hangouts_friend_simulator.py input_file [person ...]
```

```
$ python hangouts_friend_simulator.py Hangouts.json
$ python hangouts_friend_simulator.py Hangouts.json "Bradley Jewell"
$ python hangouts_friend_simulator.py Hangouts.json "Bradley Jewell" "Jean-Luc Picard" "+15551234567"
```

## Example output

```
----------
Bradley Jewell:
I got one of the keyboards so you don't have to listen to the same thing on ethernet
----------
```
