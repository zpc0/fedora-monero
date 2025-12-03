# SPDX-License-Identifier: GPL-3.0-or-later
%global debug_package %{nil}

Name:		p2pool
Version:	4.12
Release:	2%{?dist}
Summary:	Decentralized pool for Monero mining

License:	GPL-3.0-only
URL:		https://p2pool.io
Source0:	https://github.com/SChernykh/%{name}/releases/download/v%{version}/%{name}_source-v%{version}.tar.xz
Source1:	https://github.com/SChernykh/%{name}/releases/download/v%{version}/sha256sums.txt.asc
Source2:	SChernykh.asc

# for source tarball verification
BuildRequires:	coreutils
BuildRequires:	gnupg2

BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	gcc-c++
BuildRequires:	libcurl-devel
BuildRequires:	libstdc++-static
BuildRequires:	libuv-devel
BuildRequires:	zeromq-devel

%description
Decentralized pool for Monero mining

%prep
# check PGP signature
gpg --dearmor --output SChernykh-keyring.gpg %{SOURCE2}
gpgv --keyring ./SChernykh-keyring.gpg %{SOURCE1}

# calc hashes
trusted_hash=$(sed -n '/Name:\sp2pool_source-v%{version}.tar.xz/,/SHA256:\s/p' %{SOURCE1} | tail -c 65 | head -c 64)
archive_hash=$(sha256sum %{SOURCE0} | head -c 64)

# check against correct hash
if ! [ $trusted_hash = $archive_hash ]; then
	exit 1
fi

%autosetup -n %{name}

%build
%cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -DWITH_RANDOMX=OFF -DWITH_UPNP=OFF -DWITH_GRPC=OFF -DWITH_TLS=OFF -DWITH_MERGEMINING_DONATION=OFF
%cmake_build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/p2pool %{buildroot}%{_bindir}/p2pool

%files
%license LICENSE
%{_bindir}/p2pool

%changelog
%autochangelog
