# NetRelay
NetRelay is a simple network relay tool forwarding the shell command to the destination terminal.

## Usage

**For relay terminal**

```bash
python3 relay.py --src=<sourceAddr>
```

**For client terminal**

```bash
python3 client.py --dst=<destinationAddr>[ --error]
```

- `--error` will display `stderr` message on the screen.

**For API use**

```python
import netrelay.client as nr_client
```

- Use `nr_client.start(<ipPortAddr>)` and `nr_client.close()` to start the connection to the relay server and close the connection to the relay server. `start` will return two values `s, id` representing the remote relay server `<server>` and the index of the current client on the remote relay server.

- Use `nr_client.exec_cmd(<server>, <command>)` to execute the `<command>` remotely on relay server `<server>`. `exec_cmd` will return two values `res, err` representing the result of the execution and the error message of the execution respectively.
- Use `nr_client.exec_cmd_and_save(<server>, <command>, <resultDir>[, <errorMessageDir>])` to execute the `<command>` remotely on relay server `<server>`, and save the result in `<resultDir>`, save the error message in `<errorMessageDir>`.

Here is an example.

```python
import netrelay.client as nr_client
s, id = nr_client.start(('127.0.0.1', 2333))
res, err = nr_client.exec_cmd(s, 'curl -L www.linux.com')
nr_client.exec_cmd_and_save(s, 'curl -L www.linux.com', 'linux.html')
nr_client.close()
```

## To-dos

- [x] mini-shell client
- [x] client API support

