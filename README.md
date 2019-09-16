# Python-P2P

Rudimentary Peer-to-Peer file transfer service written in Python. All files to be transferred will
need to be in the `local_files` directory which should be located in the root of the project. On
Client startup, all current files in the `local_files` directory will be sent to the Server. Any
additional files will need to be added to the `local_files` directory and need to be added to the
Server via the `add` command.


## Steps to Run

Run `python3 server.py` on the machine you would like to act as your main Server. Once the server is
running, it will output the IP address and port number the server is running on (the Port Number is
configured to be static) for future reference

For any Clients, run `python3 client.py` and enter the requested information (Port number
to run the Client service on and the hostname of the Server).

NOTE: For running on Python2, find/replace all instances of `input()` with `raw_input()` in both the
Server and Client source code.


## Commands

| Command | Description |
|---|---|
| `add` | Adds a local file to the Server's list of tracked files |
| `list` | Lists all files currently recognized by the Server |
| `lookup` | Returns information on a specific file, namely, what Clients have the file and the information (Hostname/Port) of those Clients |
| `get` | Downloads a specific file from another Client |
| `quit` | Exits the Client |
