# TODO:
# - does ASL requir source be available?
#   https://github.com/metageek-llc/inSSIDer-2-Cross-Platform/wiki/Installation-instructions-+-Troubleshooting-+-FAQ-for-inSSIDer-Beta-0.1.1.0429
#   Q: Where is the source code?
#   A: Again, nowhere! We will be releasing the source code for sure but we want
#   to make sure everything works. We also need to cleanup and document the
#   source code.
Summary:	inSSIDer 2 for Linux
Name:		inssider
Version:	0.1.1.0429
Release:	0.2
License:	Apache v2.0
Group:		Applications/Networking
Source0:	https://github.com/downloads/metageek-llc/inSSIDer-2-Cross-Platform/%{name}-%{version}-1.i386.rpm
# Source0-md5:	f62c4f163ddca2987f570cc6cfbae3bc
Source1:	https://github.com/downloads/metageek-llc/inSSIDer-2-Cross-Platform/%{name}-%{version}-1.x86_64.rpm
# Source1-md5:	8f1ca45c92a19f3f7b419e3ebba52860
Source2:	https://github.com/downloads/metageek-llc/inSSIDer-2-Cross-Platform/%{name}_patch_x86_for_%{version}.zip
# Source2-md5:	0a105705f15ab0897a82f1830d873115
Source3:	https://github.com/downloads/metageek-llc/inSSIDer-2-Cross-Platform/%{name}_patch_x64_for_%{version}.zip
# Source3-md5:	271040e4fa1ded4700f596e164a6af65
URL:		http://www.metageek.net/products/inssider/linux/
BuildRequires:	rpm-utils
BuildRequires:	unzip
Requires:	mono-tools-webkit
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nSSIDer is the first award-winning Wi-Fi scanner to come out of the
woodwork since the netstumbler era. Use inSSIDer to war drive or
troubleshoot Wi-Fi channel placement. This program will display all
Wi-Fi access points within range and display their MAC address, SSID,
RSSI, Channel, Vendor, Encryption, Max Rate and Network Type. Use the
filters feature to quickly sort through long lists of access points.

%prep
%setup -qcT
%ifarch %{ix86}
rpm2cpio %{SOURCE0} | cpio -dimu
unzip -qq %{SOURCE2}
%endif
%ifarch %{x8664}
rpm2cpio %{SOURCE1} | cpio -dimu
unzip -qq %{SOURCE3}
%endif

mv .%{_desktopdir}/*.desktop .
mv .%{_datadir}/%{name} .
mv %{name}/%{name}.sh .

# patch files
mv inssider_patch_*/MetaGeek.inSSIDer.LinuxManager.dll inssider/Components
mv inssider_patch_*/MetaGeek.inSSIDer.Extensions.NewsFeed.dll inssider/Extensions

cat <<EOF > %{name}.sh
#!/bin/sh
exec mono %{_datadir}/%{name}/inSSIDer.exe "$@"
EOF

mv .%{_docdir}/inssider/* .
gzip -d changelog.Debian.gz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_desktopdir}}
cp -a %{name}/* $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -p *.desktop $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.Debian copyright
%attr(755,root,root) %{_bindir}/inssider
%{_datadir}/%{name}
%{_desktopdir}/inSSIDer.desktop
