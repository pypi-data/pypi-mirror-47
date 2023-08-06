# Node Backup Utility

## About

This is a utility which allows for backuping up of a lightning node

## Usage

### Configuring

You need to have a config file in ```$HOME/.lncm/nodebackup.toml```

```
provider = "dropbox"
nodename = "testnode"
logfile = "/var/log/backup.log"
backupfile = "/root/.lnd/data/chain/bitcoin/mainnet/channel.backup"
pidfile = "/var/run/nodebackup.pid"

[apikeys]
dropbox = "APIKEYHERE"

```

### Running

After installing the utility simply invoke

```bash
lndnodebackup
```

This will run as a background task.

## Building

```bash
sudo python3 -m pip install setuptools wheel twine
python3 setup.py bdist_wheel
sudo pip3 uninstall dist/nodebackup-X.X.X-py3-none-any.whl
```

## Todo / What's Missing

- [ ] Support for Amazon S3
- [ ] Connect to LND and backup each channel individually and grab the text backup as well
- [ ] Robustness (maybe have the script handle SIGHUP to reload configuration file)