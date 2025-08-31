# SPDX-License-Identifier: BSD-3-Clause
# fix build error on F40+
%global build_type_safety_c 0

Name:		monero
Version:	0.18.4.2
Release:	1%{?dist}
Summary:	Monero - the secure, private, untraceable cryptocurrency

License:	BSD-3-Clause
URL:		https://getmonero.org
Source0:	https://downloads.getmonero.org/cli/%{name}-source-v%{version}.tar.bz2
Source1:	https://www.getmonero.org/downloads/hashes.txt
Source2:	binaryfate.asc
Source3:	jeffro256.asc
# from https://github.com/Boog900/monero-ban-list/
Source4:	ban_list.txt
Source5:	jeffro256.sig

Patch0:		optimize-o2.patch

# for source tarball verification
BuildRequires:	coreutils
BuildRequires:	gnupg2

BuildRequires:	bzip2
BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	pkgconf
BuildRequires:	boost-devel
BuildRequires:	libsodium-devel
BuildRequires:	openpgm-devel
BuildRequires:	openssl-devel
# Boost uses OpenSSL engine, which removed from openssl-devel
BuildRequires:	openssl-devel-engine
BuildRequires:	unbound-devel
BuildRequires:	miniupnpc-devel
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

# check ban list signature
gpg --dearmor --output ./jeffro256-keyring.gpg %{SOURCE3}
gpgv --keyring ./jeffro256-keyring.gpg %{SOURCE5} %{SOURCE4}

%autosetup -n %{name}-source-v%{version}

%build
# enforce minimum CMake version
export CMAKE_POLICY_VERSION_MINIMUM=3.5

%cmake -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DUSE_CCACHE=OFF -DBUILD_DOCUMENTATION=OFF -DBUILD_DEBUG_UTILITIES=OFF -DBUILD_SHARED_LIBS=OFF -DSTACK_TRACE=OFF -DNO_AES=ON
%cmake_build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/bin/* %{buildroot}%{_bindir}/
# install MRL recommended ban list
# https://github.com/monero-project/meta/issues/1124
mkdir -p %{buildroot}%{_datadir}/monero
install -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/monero/

%files
%license LICENSE
%{_bindir}/monerod
%{_datadir}/monero/ban_list.txt

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
