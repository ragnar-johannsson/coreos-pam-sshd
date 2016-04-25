## PAM enabled SSHd for CoreOS

CoreOS does not come with support for Pluggable Authentication Modules. This is understandable considering the philosophy of CoreOS. However, there are times when you need Yubikey for two-factor authentication or OpenLDAP or some other means to authenticate users - basically, what people have come to expect from other distros.

The PAM enabled SSH server for CoreOS works by positioning itself in between the user and the host, handling all authentication according to the PAM modules installed and sending authenticated sessions onwards to the host's SSH daemon. The server is based on Debian Jessie, meaning it should support all standard PAM installations.

### Usage

First, deploy a new CoreOS instance with `cloud-config.yml` as userdata, or configure an existing instance using the `coreos-cloudinit -from-file <file>` command. This will install the necessary services to proxy SSH into the host.

Second, prepare a container based on `ragnarb/coreos-pam-sshd`, installing the PAM modules you need and any configurations that might be called for. Push said container.

Lastly, configure the *CONTAINER* variable in `/etc/default/pam-sshd` to point to your container and adjust any docker run options you might need in the *OPTS* variable. Restart the `pam-sshd` service.

### How does it work?

The `ragnarb/coreos-pam-sshd` proxy container (or its derivative) listens on port 22 and authenticates users according to the PAM modules installed. Upon a successful authentication a one-time SSH key pair is generated for that username and pulled from the host's ssh daemon upon a connection to port 4418 from the proxy container.

Once the host has queried for username's public key (essentially the user's authorized_keys file) the key pair can never be used again. This ensures that only the proxy container which has the one-time private key for the authenticated user can connect to the host's ssh server successfully.

### Disclaimer

The `cloud-config.yml` provided changes the configuration of the SSH server on the host it is run on. Furthermore, CoreOS specific system users and groups as referenced by the *usrfiles* directive in `/etc/nsswitch.conf` are merged into `/etc/passwd` and `/etc/group` for sshd privilege-separation to work in the proxy container. This may break future updates of CoreOS. Do not deploy blindly; understand the code before continuing.

### License

BSD 2-Clause. See the LICENSE file for details.
