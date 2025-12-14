# Monero unofficial package repository for Fedora
![rpmlint status](https://img.shields.io/github/actions/workflow/status/zpc0/fedora-monero/rpmlint.yml?label=rpmlint)

## How to enable this repo
```
sudo dnf copr enable zpc00/monero
```

## How to setup
1. Create required user and directories
```
sudo useradd --system monero
sudo mkdir /var/lib/{monero,p2pool}
sudo chown monero:monero /var/lib/monero
sudo chown monero:monero /var/lib/p2pool
```
2. Install softwares
3. Add config files
```
sudo mkdir /etc/monero
sudo cp /usr/share/monero/monero.conf /etc/monero/
sudo cp /usr/share/p2pool/p2pool.conf /etc/monero/
sudoedit /etc/monero/p2pool.conf
```
4. Run
```
sudo systemctl start monerod.service
sudo systemctl start p2pool.service
```

## Included Softwares

### Monero
![BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-orange?style=flat-square&cacheSeconds=36000)
![Last update](https://img.shields.io/github/last-commit/zpc0/fedora-monero?style=flat-square&path=monero&cacheSeconds=7200)
[![Build status](https://copr.fedorainfracloud.org/coprs/zpc00/monero/package/monero/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zpc00/monero/package/monero/)
- [Upstream](https://github.com/monero-project/monero/)
```
sudo dnf install monero
sudo dnf install monero-wallet
sudo dnf install monero-utils
```

### P2Pool
![GPL-3.0-only](https://img.shields.io/badge/License-GPL--3.0--only-orange?style=flat-square&cacheSeconds=36000)
![Last update](https://img.shields.io/github/last-commit/zpc0/fedora-monero?style=flat-square&path=p2pool&cacheSeconds=7200)
[![Build status](https://copr.fedorainfracloud.org/coprs/zpc00/monero/package/p2pool/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zpc00/monero/package/p2pool/)
- [Upstream](https://github.com/SChernykh/p2pool/)
```
sudo dnf install p2pool
```

### XMRig
![GPL-3.0-or-later](https://img.shields.io/badge/License-GPL--3.0--or--later-orange?style=flat-square&cacheSeconds=36000)
![Last update](https://img.shields.io/github/last-commit/zpc0/fedora-monero?style=flat-square&path=xmrig&cacheSeconds=7200)
[![Build status](https://copr.fedorainfracloud.org/coprs/zpc00/monero/package/xmrig/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zpc00/monero/package/xmrig/)
- [Upstream](https://github.com/xmrig/xmrig/)
```
sudo dnf install xmrig
```

