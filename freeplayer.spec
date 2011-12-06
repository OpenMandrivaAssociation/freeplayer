%define name freeplayer
%define version 20070531
%define release %mkrel 0.5
%define aname vlc-fbx
%define bname fbx-playlist
%define longtitle Create Playlist for Freeplayer
%define title Freeplayer-playlist
%define playlist_version 1.1

Name:      %{name}
Version:   %{version}
Release:   %{release}
Summary:   Freeplayer from french isp Free ADSL
License:   GPL
URL:       http://faq.free.fr/adsl/Decouvrir_les_services/Freebox_TV/Options_supplementaires/FreePlayer
Group:     Video
Source0:   ftp://ftp.free.fr/pub/%{name}/%{name}-linux-%{version}.tgz
Source1:   vlc-fbx.init
Source2:   vlc-fbx.sysconfig
Source3:  freeplayer-images.tar.bz2

Source10:  %{name}-16.png
Source11:  %{name}-32.png
Source12:  %{name}-48.png
Patch0:    freeplayer-fix-vlc-args.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: qt4-devel
Requires: vlc >= 0.8.4
Requires: freeplayer-mod
Requires: freeplayer-common

%description
Freeplayer from french isp Free ADSL


%package data
Group: 		Video
License: 	GPL
Summary: 	Freeplayer from french isp Free ADSL
Provides: freeplayer-mod
Provides: freeplayer-data = %{version}
Requires: freeplayer-common

%description data
Freeplayer from french isp Free ADSL default mod

%package common
Group: 		Video
License: 	GPL
Summary: 	Freeplayer from french isp Free ADSL
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description common
Freeplayer from french isp Free ADSL default mod

%prep
rm -rf %buildroot

%setup -n %{name} -q

tar xzf share/fbx-playlist-%{playlist_version}.tar.gz
/usr/bin/bzip2 -dc %{SOURCE3} | tar -xf -

%build
cd fbx-playlist-%{playlist_version}
/usr/lib/qt4/bin/qmake
#qmake is dropping quotes, restoring them
sed -i -e 's/VERSION="1.1"/VERSION=\\"1.1\\"/g' Makefile
sed -i -e 's///g' license.ui
make

%install
mkdir -p %buildroot/%_datadir/%{name}
mkdir -p %buildroot/%_bindir %buildroot/%_sysconfdir/{init.d,sysconfig}

install -m 755 %{SOURCE1} %buildroot/%_sysconfdir/init.d/vlc-fbx
install -m 644 %{SOURCE2} %buildroot/%_sysconfdir/sysconfig/vlc-fbx

cp -r share/http-fbx %buildroot/%_datadir/%{name}
install -m 755 bin/vlc-fbx.sh -D %buildroot/%_bindir/%{aname}
install -m 755 fbx-playlist-%{playlist_version}/fbx-playlist -D %buildroot/%_bindir/%{bname}
sed -i -e 's@%HTTP_PATH%@/usr/share/freeplayer/http-fbx/@g' %buildroot/%_bindir/%{aname}

#menus

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=QT;Video;Player;X-MandrivaLinux-Multimedia-Video;
EOF

install -m644 %{SOURCE10} -D %buildroot/%{_miconsdir}/%{name}.png
install -m644 %{SOURCE11} -D %buildroot/%{_iconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %buildroot/%{_liconsdir}/%{name}.png

%clean
rm -rf %buildroot

%preun common
%_preun_service vlc-fbx

%post common
%_post_service vlc-fbx

%if %mdkversion < 200900
%post 
%{update_menus}
%endif

%if %mdkversion < 200900
%postun 
%{clean_menus}
%endif

%files 
%defattr(-,root,root)
%doc README share/doc/*
%_bindir/*
%_iconsdir/*.png
%_liconsdir/*.png
%_miconsdir/*.png
%_datadir/applications/mandriva-%{name}.desktop

%files data
%defattr(-,root,root)
%_datadir/%{name}

%files common
%defattr(-,root,root)
%config(noreplace) %_sysconfdir/sysconfig/vlc-fbx
%_sysconfdir/init.d/vlc-fbx

