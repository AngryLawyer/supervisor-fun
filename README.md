Supervisor fun
---

An example of some Python3 logic simulating a distributed set of engines.

Getting started
-----

You're going to want to run this through venv.

```bash
python3 -m venv ./env
./env/bin/pip install -r requirements.txt
```

A precompiled frontend has been provided, but you can compile it yourself by reading the instructions in the `frontend` directory.

Running
-----

The project exists in multiple distinct parts: individual MACHINE nodes, and a SUPERVISOR that looks out for them.

You can start up MACHINES like so

```bash
./env/bin/python3 machine [unique identifier] [machine type] [URL of supervisor]
```

They'll begin doing their thing and reporting back to the supervisor. The currently available types are:

* Blinker - simulate a blinking light

To start up a SUPERVISOR, do the following

```bash
./env/bin/python3 supervisor [port]
```

You'll want to make the port the same as the ones the MACHINES are calling back to.

A dashboard will become available on `http://localhost:[port]` - you can watch as the machines dial home and register with the dashboard.
