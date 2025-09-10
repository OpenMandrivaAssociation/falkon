%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 70 ] && echo -n un; echo -n stable)
%define major 2
%global optflags %{optflags} -O3 -Wno-error=return-type-c-linkage -I%(python -c "from distutils.sysconfig import get_python_inc; print (get_python_inc());")
%bcond_with pyside6

%global __provides_exclude_from ^%{_qtdir}/plugins/falkon/.*$

Summary:	Fast, lightweight web browser based on QtWebEngine
Name:		falkon
Version:	25.08.0
Release:	1
Source0:	https://download.kde.org/%{stable}/release-service/%{version}/src/falkon-%{version}.tar.xz
License:	GPLv3+ and BSD and LGPLv2.1 and GPLv2+ and MPL
Group:		Networking/WWW
Url:		https://github.com/KDE/falkon

BuildRequires:	cmake(ECM)
BuildRequires:	qt6-qttools-linguist-tools
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6WebEngineCore)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	pkgconfig(python3)
BuildRequires:	cmake(KF6Wallet)
BuildRequires:	cmake(KF6I18n)
# Optional -- having them enables KDE integration
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6Crash)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6Purpose)
%if %{with pyside6}
BuildRequires:	cmake(PySide6)
BuildRequires:	cmake(Shiboken6)
%endif
BuildRequires:	gettext-devel
Requires:	%{name}-core = %{EVRD}
Suggests:	%{name}-plugins = %{EVRD}
Requires:	qt6-qtbase-sql-sqlite
Provides:	webclient
Requires:	distro-release-indexhtml
Requires:	xdg-utils
%rename qupzilla
# We use the P6 version of Falkon even for P5 these days.
# The qt5 version of QtWebEngine is too far behind to be useful
# these days. Lots of sites reject it as "browser too old".
%rename plasma6-falkon

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

%patchlist
falkon-3.0.1-webinspector.patch
falkon-3.1.0-not-in-More-menu.patch
# Running a browser as root may not be the smartest thing to do,
# but calamares does it during installation, so let's make it work...
falkon-3.1.0-fix-running-as-root.patch
falkon-3.1.0-native-scrollbars.patch
falkon-3.1.0-omdv-settings.patch
falkon-3.1.0-menuentry.patch
falkon-3.1.0-compile.patch

%files

#----------------------------------------------------------------------------

%package core
Summary:	%{name} web browser core package
Group:		Networking/WWW
Obsoletes:	%{_lib}QupZilla1
Obsoletes:	%{_lib}QupZilla2
%rename qupzilla-core
%rename plasma6-falkon-core
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

%files core -f falkon.lang
%{_bindir}/falkon
# No need to create a separate libpackage for a "library"
# that can't be used by anything else...
%{_libdir}/libFalkonPrivate.so.*
%dir %{_datadir}/falkon
%{_datadir}/falkon/themes
%{_datadir}/bash-completion/completions/*
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/applications/org.kde.falkon.desktop
%{_datadir}/metainfo/org.kde.falkon.appdata.xml
%dir %{_qtdir}/plugins/falkon

#----------------------------------------------------------------------------

%package plugins
Summary:	Various plugins for %{name} web browser
Group:		Networking/WWW
Requires:	%{name} = %{EVRD}
%rename qupzilla-plugins
%rename plasma6-falkon-plugins

%description plugins
QupZilla Plugins are dynamically loaded shared libraries (*.so) that can extend
application in almost any way. This package contains the following plugins:

* Mouse Gestures
* Access Keys Navigation
* Personal Information Manager
* GreaseMonkey

%files plugins
%{_qtdir}/plugins/falkon/*.so
%exclude %{_qtdir}/plugins/falkon/KDEFrameworksIntegration.so
%if %{with pyside6}
%{_qtdir}/plugins/falkon/middleclickloader
%{_qtdir}/plugins/falkon/runaction
%endif

#----------------------------------------------------------------------------

%package kde
Summary:	KDE Frameworks Integration plugin for falkon
Group:		Networking/WWW
Requires:	%{name} = %{EVRD}
%rename plasma6-falkon-kde

%description kde
Plugin for Falkon adding support for:
- storing passwords securely in KWallet,
- additional URL protocols using KIO (e.g., man:, info:, gopher:, etc.),
- a "Share page" menu using the KDE Purpose Framework,
- intercepting crashes with KCrash, bringing up the DrKonqi crash handler.

%files kde
%{_qtdir}/plugins/falkon/KDEFrameworksIntegration.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}
dos2unix README.md

%build
export PORTABLE_BUILD="false"

%cmake \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DDISABLE_DBUS:BOOL=FALSE \
	-DSHIBOKEN_BINARY=%{_bindir}/shiboken6 \
	-DSHIBOKEN_INCLUDE_DIR=%{_includedir}/shiboken6 \
	-DSHIBOKEN_PYTHON_INCLUDE_DIR=%{_includedir}/python3.11 \
	-DSHIBOKEN_LIBRARY=$(ls %{_libdir}/libshiboken6.cpython-3*.so) \
	-DPYSIDE_LIBRARY=$(ls %{_libdir}/libpyside6.cpython-3*.so) \
	-DPYSIDE_INCLUDE_DIR=%{_includedir}/PySide6 \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# remove useless plugins
rm -fv %{buildroot}%{_qtdir}/plugins/falkon/TestPlugin.so
rm -rfv %{buildroot}%{_qtdir}/plugins/falkon/qml/helloqml

# find_lang can't deal with the strange mix of .mo and .qm style
# translations all put in the same place, so let's do the right thing
# manually
TOPDIR="$(pwd)"
cd %{buildroot}
find .%{_datadir}/locale -type f -name "*.qm" -o -name "*.mo" |while read r; do
    printf '%%%%lang(%%s) %%s\n' $(echo $r |cut -d/ -f5) $(echo $r |cut -b2-) >>"$TOPDIR"/falkon.lang
done
