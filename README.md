# PyDash - A dashboard for Redis written in Python

This is my first attempt at writing a program in Python. It's a command-line application that takes in a Redis URI, parses it and gives you real-time statistics about your Redis database in your terminal.

### Running it
Using the command line, run:

```
python3 main.py redis://connection.string.here
```

If you don't have a connection string starting with `redis://`, it won't work.

## Updates
The project is in development now. A checklist of what's going to be covered by the application is:

- [x] Connecting to Redis
- [ ] Show memory statistics - _in development_
- [ ] Show time statistics - _in development_
- [ ] Show real-time monitoring:
    - [ ] Show inserts
    - [ ] Show reads
    - [ ] Show writes
    - [ ] Show deletes
    
_... more to come._