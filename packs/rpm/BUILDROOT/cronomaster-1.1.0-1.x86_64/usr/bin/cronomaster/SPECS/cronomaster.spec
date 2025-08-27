Name:           cronomaster
Version:        1.1.0
Release:        1%{?dist}
Summary:        Time Wallet GTK written tha save and sen seconds between app using TCP/IP.
License:        MIT
URL:            https://github.com/martina-pauer/cronomaster
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python3-gobject
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-gobject
Requires:       gtk3
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This is a simple GTK application built with Python and the GObject Introspection
bindings. This package demonstrates how to properly package a Python/GTK app
for RPM-based systems.

%prep
%setup -q %{name}-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin/cronomaster
cp -R ../../* %{buildroot}/usr/bin/cronomaster/
rm -rf %{buildroot}

%files
%doc README.md
%license LICENSE
%{python3_sitelib}/%{name}/
%{buildroot}/usr/bin/cronomaster/

%changelog
* Wed Aug 27 2025 Martina Pauer
- Making rpm package for cronomaster


