%define oname falkon
%define major 2
%define snapshot %nil

Summary:	Fast, lightweight web browser based on QtWebEngine
Name:		falkon
Version:	3.0.1
%if 0%snapshot
Release:	0.%{snapshot}.1
Source0:	%{oname}-%{snapshot}.tar.xz
%else
Release:	1
Source0:	http://download.kde.org/stable/falkon/%(echo %{version} |cut -d. -f1-2)/src/falkon-%{version}.tar.xz
%endif
Source100:	falkon.rpmlintrc
License:	GPLv3+ and BSD and LGPLv2.1 and GPLv2+ and MPL
Group:		Networking/WWW
Url:		https://github.com/KDE/falkon
BuildRequires:	cmake cmake(ECM)
BuildRequires:	ninja
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5WebEngine)
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5Script)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	cmake(KF5Wallet)
Requires:	%{name}-core = %{EVRD}
Suggests:	%{name}-plugins = %{EVRD}
Requires:	qt5-qtbase-database-plugin-sqlite
Requires:	%{_lib}qt5-output-driver-default
Conflicts:	rosa-media-player-plugin
Provides:	webclient

%rename qupzilla

%description
Falkon is a very fast and lightweight web browser. It aims to be a lightweight
web browser available through all major platforms. This project has been
originally started only for educational purposes. But from its start, Falkon
has grown into a feature-rich browser.

Falkon has all standard functions you expect from a web browser. It includes
bookmarks, history (both also in sidebar) and tabs. Above that, you can manage
RSS feeds with an included RSS reader, block ads with a builtin AdBlock plugin,
block Flash content with Click2Flash and edit the local CA Certificates
database with an SSL Manager.

Falkon's main aim is to be a very fast and very stable QtWebEngine browser
available to everyone.

%files

#----------------------------------------------------------------------------

%package core
Summary:	%{oname} web browser core package
Group:		Networking/WWW
Obsoletes:	%{_lib}QupZilla1
Obsoletes:	%{_lib}QupZilla2
%rename qupzilla-core
# FIXME move this to a devel subpackage if Falkon ever
# decides to install headers for external plugins
Obsoletes:	%{_lib}QupZilla-devel

%description core
QupZilla is a new and very fast QtWebKit browser. It aims to be a lightweight
web browser available through all major platforms. This project has been
originally started only for educational purposes. But from its start, QupZilla
has grown into a feature-rich browser.

QupZilla has all standard functions you expect from a web browser. It includes
bookmarks, history (both also in sidebar) and tabs. Above that, you can manage
RSS feeds with an included RSS reader, block ads with a builtin AdBlock plugin,
block Flash content with Click2Flash and edit the local CA Certificates
database with an SSL Manager.

QupZilla's main aim is to be a very fast and very stable QtWebEngine browser
available to everyone.

%files core -f %{name}.lang
%{_bindir}/%{name}
# No need to create a separate libpackage for a "library"
# that can't be used by anything else...
%{_libdir}/libFalkonPrivate.so.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/themes
%{_datadir}/bash-completion/completions/*
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/org.kde.falkon.desktop
%{_datadir}/metainfo/org.kde.falkon.appdata.xml
%dir %{_libdir}/plugins
%dir %{_libdir}/plugins/falkon

#----------------------------------------------------------------------------

%package plugins
Summary:	Various plugins for %{oname} web browser
Group:		Networking/WWW
Requires:	%{name} = %{EVRD}
%rename qupzilla-plugins

%description plugins
QupZilla Plugins are dynamically loaded shared libraries (*.so) that can extend
application in almost any way. This package contains the following plugins:

* Mouse Gestures
* Access Keys Navigation
* Personal Information Manager
* GreaseMonkey

%files plugins
%{_libdir}/plugins/falkon/*.so

#----------------------------------------------------------------------------

%prep
%if 0%{snapshot}
%setup -q -n %{oname}-%{snapshot}
%else
%setup -q -n %{oname}-%{version}
%endif
%apply_patches
dos2unix README.md

%build
export USE_LIBPATH=%{_libdir}/
export USE_WEBGL="true"
export DISABLE_UPDATES_CHECK="true"
export DISABLE_DBUS="false"
export PORTABLE_BUILD="false"
export KDE_INTEGRATION="true"

%cmake -G Ninja
%ninja_build

%install
%ninja_install -C build

%find_lang %{name} --all-name --with-qt
