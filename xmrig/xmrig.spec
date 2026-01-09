# SPDX-License-Identifier: GPL-3.0-or-later
%global debug_package %{nil}

%global _pkg_extra_ldflags -Wl,-z,nodlopen

Name:		xmrig
Version:	6.25.0
Release:	2%{?dist}
Summary:	unified CPU/GPU miner

License:	GPL-3.0-or-later
URL:		https://xmrig.com
Source0:	https://github.com/%{name}/%{name}/archive/refs/tags/v%{version}.tar.gz
Source1:	xmrig.service

Patch0:		disable-auto-donate.patch

BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	hwloc-devel
BuildRequires:	libstdc++-static
BuildRequires:	libuv-static
BuildRequires:	openssl-devel
BuildRequires:	systemd-rpm-macros

%description
XMRig is a high performance, open source, cross platform
unified CPU/GPU miner

%prep
%setup -q
%patch 0

%build
%cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -DWITH_HTTP=OFF -DWITH_ENV_VARS=OFF -DWITH_OPENCL=OFF -DWITH_CUDA=OFF
%cmake_build

%install
install -d %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/xmrig %{buildroot}%{_bindir}/xmrig
install -d %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

%files
%license LICENSE
%{_bindir}/xmrig
%{_unitdir}/xmrig.service

%changelog
%autochangelog
