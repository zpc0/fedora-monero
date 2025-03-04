# SPDX-License-Identifier: BSD-3-Clause
# fix build error on F40+
%global build_type_safety_c 0

Name:		monero
Version:	0.18.3.4
Release:	3%{?dist}
Summary:	Monero - the secure, private, untraceable cryptocurrency

License:	BSD-3-Clause
URL:		https://getmonero.org
Source0:	https://downloads.getmonero.org/cli/%{name}-source-v%{version}.tar.bz2
Source1:	https://www.getmonero.org/downloads/hashes.txt
Source2:	binaryfate.asc

Patch0:		optimize-o2.patch

# for source tarball verification
BuildRequires:	coreutils
BuildRequires:	gnupg2

BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	pkgconf
BuildRequires:	boost-devel
BuildRequires:	libsodium-devel
BuildRequires:	openpgm-devel
BuildRequires:	openssl-devel
# Boost uses OpenSSL engine, which removed from openssl-devel (F41+)
%if 0%{?fedora} >= 41
BuildRequires:	openssl-devel-engine
%endif
BuildRequires:	unbound-devel
BuildRequires:	zeromq-devel
# for input editing
BuildRequires:	readline-devel
# for hardware wallet
BuildRequires:	hidapi-devel
BuildRequires:	libusb1-devel
BuildRequires:	protobuf-compiler
BuildRequires:	protobuf-devel
BuildRequires:	systemd-devel

%description
Monero - Private decentralized cryptocurrency that keeps
your finances confidential and secure.

%package	utils
Summary:	Monero misc utils

%description	utils
Monero CLI misc utils

%package	wallet
Summary:	Monero wallet

%description	wallet
Monero CLI wallet

%prep
# print host cpu info
cat /proc/cpuinfo

# check PGP signature
gpg --dearmor --output binaryfate-keyring.gpg %{SOURCE2}
gpgv --keyring ./binaryfate-keyring.gpg %{SOURCE1}

# calc hashes
trusted_hash=$(grep monero-source %{SOURCE1} | head -c 64)
archive_hash=$(sha256sum %{SOURCE0} | head -c 64)

# check against correct hash
if ! [ $trusted_hash = $archive_hash ]; then
	exit 1
fi

%autosetup -n %{name}-source-v%{version}

%build
%make_build release

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 build/release/bin/* %{buildroot}%{_bindir}/

%files
%license LICENSE
%{_bindir}/monerod

%files		utils
%license LICENSE
%{_bindir}/monero-blockchain-ancestry
%{_bindir}/monero-blockchain-depth
%{_bindir}/monero-blockchain-export
%{_bindir}/monero-blockchain-import
%{_bindir}/monero-blockchain-mark-spent-outputs
%{_bindir}/monero-blockchain-prune
%{_bindir}/monero-blockchain-prune-known-spent-data
%{_bindir}/monero-blockchain-stats
%{_bindir}/monero-blockchain-usage
%{_bindir}/monero-gen-ssl-cert
%{_bindir}/monero-gen-trusted-multisig

%files		wallet
%license LICENSE
%{_bindir}/monero-wallet-cli
%{_bindir}/monero-wallet-rpc

%changelog
%autochangelog
