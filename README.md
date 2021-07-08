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

The project exists in multiple distinct parts: individual MACHINE nodes, and a SUPERVISOR that looks out for them.

You can start up MACHINES like so

```bash
./env/bin/python3 machine [unique identifier] [machine type] [URL of supervisor]
```

They'll begin doing their thing and reporting back to the supervisor
