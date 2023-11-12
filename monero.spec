Name:		monero
Version:	0.18.3.1
Release:	1%{?dist}
Summary:	Monero the secure, private, untraceable cryptocurrency

License:	MIT
URL:		https://getmonero.org
Source0:	https://downloads.getmonero.org/cli/%{name}-source-v%{version}.tar.bz2
Source1:	https://www.getmonero.org/downloads/hashes.txt
Source2:	https://github.com/zpc0/fedora-monero/raw/master/binaryFate.gpg

# for source tarball verification
BuildRequires:	coreutils
BuildRequires:	gnupg2

BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	boost-devel
BuildRequires:	libsodium-devel
BuildRequires:	openpgm-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconf
BuildRequires:	unbound-devel
BuildRequires:	zeromq-devel

%description
Monero daemon - Private decentralized cryptocurrency that keeps
your finances confidential and secure.

%package	utils
Summary:	Monero misc utils

%description
Monero CLI misc utils

%package	wallet
Summary:	Monero wallet

%description
Monero CLI wallet

%prep
# check PGP signature
gpgv --keyring %{SOURCE2} %{SOURCE1}

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
* Fri Nov 10 2023 zpc <dev@zpc.st>
- initial release.
