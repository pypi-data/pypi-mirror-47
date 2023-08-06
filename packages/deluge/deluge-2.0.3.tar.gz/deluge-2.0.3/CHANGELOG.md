# Changelog

## 2.0.3 (2019-06-12)

### Gtk UI

- Fix errors running on Wayland (#3265).
- Fix Peers Tab tooltip and context menu errors (#3266).

### Web UI

- Fix TypeError in Peers Tab setting country flag.
- Fix reverse proxy header TypeError (#3260).
- Fix request.base 'idna' codec error (#3261).
- Fix unable to change password (#3262).

### Extractor plugin

- Fix potential error starting plugin.

### Documentation

- Fix macOS install typo.
- Fix Windows install instructions.

## 2.0.2 (2019-06-08)

### Packaging

- Add systemd deluged and deluge-web service files to package tarball (#2034)

### Core

- Fix Python 2 compatiblity issue with SimpleNamespace.

## 2.0.1 (2019-06-07)

### Packaging

- Fix setup.py build error without git installed.

## 2.0.0 (2019-06-06)

### Codebase

- Ported to Python 3

### Core

- Improved Logging
- Removed the AutoAdd feature on the core. It's now handled with the AutoAdd
  plugin, which is also shipped with Deluge, and it does a better job and
  now, it even supports multiple users perfectly.
- Authentication/Permission exceptions are now sent to clients and recreated
  there to allow acting upon them.
- Updated SSL/TLS Protocol parameters for better security.
- Make the distinction between adding to the session new unmanaged torrents
  and torrents loaded from state. This will break backwards compatability.
- Pass a copy of an event instead of passing the event arguments to the
  event handlers. This will break backwards compatability.
- Allow changing ownership of torrents.
- File modifications on the auth file are now detected and when they happen,
  the file is reloaded. Upon finding an old auth file with an old format, an
  upgrade to the new format is made, file saved, and reloaded.
- Authentication no longer requires a username/password. If one or both of
  these is missing, an authentication error will be sent to the client
  which sould then ask the username/password to the user.
- Implemented sequential downloads.
- Provide information about a torrent's pieces states
- Add Option To Specify Outgoing Connection Interface.
- Fix potential for host_id collision when creating hostlist entries.

### Gtk UI

- Ported to GTK3 (3rd-party plugins will need updated).
- Allow changing ownership of torrents.
- Host entries in the Connection Manager UI are now editable.
- Implemented sequential downloads UI handling.
- Add optional pieces bar instead of a regular progress bar in torrent status tab.
- Make torrent opening compatible with all unicode paths.
- Fix magnet association button on Windows.
- Add keyboard shortcuts for changing queue position:
  - Up: Ctrl+Alt+Up
  - Down: Ctrl+Alt+Down
  - Top: Ctrl+Alt+Shift+Up
  - Bottom: Ctrl+Alt+Shift+Down

### Web UI

- Server (deluge-web) now daemonizes by default, use '-d' or '--do-not-daemonize' to disable.
- Fixed the '--base' option to work for regular use, not just with reverse proxies.

### Blocklist Plugin

- Implemented whitelist support to both core and GTK UI.
- Implemented ip filter cleaning before each update. Restarting the deluge
  daemon is no longer needed.
- If "check_after_days" is 0(zero), the timer is not started anymore. It
  would keep updating one call after the other. If the value changed, the
  timer is now stopped and restarted using the new value.
