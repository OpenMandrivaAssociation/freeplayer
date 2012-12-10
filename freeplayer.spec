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
sed -i -e 's^%HTTP_PATH%^/usr/share/freeplayer/http-fbx/^g' %buildroot/%_bindir/%{aname}

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



%changelog
* Tue Dec 06 2011 Götz Waschk <waschk@mandriva.org> 20070531-0.5mdv2012.0
+ Revision: 738184
- fix sed command
- yearly rebuild

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 20070531-0.4mdv2011.0
+ Revision: 610768
- rebuild

* Wed Feb 10 2010 Guillaume Rousse <guillomovitch@mandriva.org> 20070531-0.3mdv2010.1
+ Revision: 503481
- fix VLC args
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 20070531-0.1mdv2009.0
+ Revision: 218423
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Jun 03 2007 Frederic Crozat <fcrozat@mandriva.com> 20070531-0.1mdv2008.0
+ Revision: 34838
- Release 20070531
- Remove patch0, merged upstream


* Fri Aug 11 2006 Emmanuel Andry <eandry@mandriva.org> 20050905-0.14mdv2007.0
- statically set qt4 to /usr/lib/qt4/bin/qmake to fix x86_64 build (strange, I know)

* Fri Jun 23 2006 Jerome Martin <jmartin@mandriva.org> 20050905-0.13mdv2007.0
- xdg menu
- Fix url
- Fix missing images

* Sun Jun 04 2006 Jerome Martin <jmartin@mandriva.org> 20050905-0.12mdk
- Split common and data for other mod
- Fix require

* Wed May 10 2006 Frederic Crozat <fcrozat@mandriva.com> 20050905-0.11mdk
- Drop the "base" package, rename it back freeplayer, there is no
  need to call it "base"
- Fix initscript and sysconfig file to use "daemon" user and allow
  easy change by user (Mdk bug #22200)
- Move initscript into freeplayer-data package, they can be used without
  main freeplayer package

* Fri Apr 07 2006 Jerome Martin <jmartin@mandriva.org> 20050905-0.10mdk
- Fixed rpmlint errors

* Sun Mar 19 2006 Jerome Martin <jerome.f.martin@free.fr> 20050905-0.9mdk
- Separate common part

* Mon Feb 06 2006 Frederic Crozat <fcrozat@mandriva.com> 20050905-0.8mdk
- fix restart in initscript
- allow to configure port for vlc http server

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 20050905-0.7mdk
- fix typo in initscript

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 20050905-0.6mdk
- convert parallel init to LSB

* Tue Jan 03 2006 Frederic Crozat <fcrozat@mandriva.com> 20050905-0.5mdk
- Update source2 to support parallel initscript

* Wed Dec 14 2005 Frederic Crozat <fcrozat@mandriva.com> 20050905-0.4mdk
- Fix build on x86-64 (Mdk bug #20199)

* Tue Oct 04 2005 Frederic Crozat <fcrozat@mandriva.com> 20050905-0.3mdk
- Enforce dependency on vlc >= 0.8.4
- Add initscript for people who don't want to use X11 vlc

* Mon Sep 05 2005 Frederic Crozat <fcrozat@mandriva.com> 20050905-0.2mdk 
- Fix http-fbx path

* Mon Sep 05 2005 Frederic Crozat <fcrozat@mandriva.com> 20050905-0.1mdk 
- Release 20050905
- Regenerate patch0

* Thu Jul 07 2005 Frederic Crozat <fcrozat@mandriva.com> 20050701-0.4mdk 
- Arg, install compiled version of fbx-playlist

* Wed Jul 06 2005 Frederic Crozat <fcrozat@mandriva.com> 20050701-0.3mdk 
- Remove dependency on transcode (not needed, vlc does the job)
- Patch0 : allow many playlists to be used as argument for vlc-fbx scripts,
  merge previous patches 0 and 1 in it.
- Clean specfile
- Drop menu for vlc-fbx, can't be used that way (yet)

* Sat Jul 02 2005 Sebastien Savarin <plouf@mandriva.org> 20050701-0.2mdk
- Spec file corrections

* Fri Jul 01 2005 Sebastien Savarin <plouf@mandriva.org> 20050701-0.1mdk
- First Mandriva Linux release

