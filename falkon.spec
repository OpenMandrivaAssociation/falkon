%define oname falkon
%define major 2
%global optflags %{optflags} -O3 -Wno-error=return-type-c-linkage -I%(python -c "from distutils.sysconfig import get_python_inc; print (get_python_inc());")
%ifarch %{aarch64}
%bcond_with pyside2
%else
%bcond_without pyside2
%endif

%global __provides_exclude_from ^%{_qt5_plugindir}/falkon/.*$

Summary:	Fast, lightweight web browser based on QtWebEngine
Name:		falkon
Version:	23.04.2
Release:	1
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
Source0:	https://download.kde.org/%{stable}/release-service/%{version}/src/falkon-%{version}.tar.xz
License:	GPLv3+ and BSD and LGPLv2.1 and GPLv2+ and MPL
Group:		Networking/WWW
Url:		https://github.com/KDE/falkon
Source100:	falkon.rpmlintrc
Patch0:		falkon-3.0.1-webinspector.patch
Patch1:		falkon-3.1.0-not-in-More-menu.patch
# Running a browser as root may not be the smartest thing to do,
# but calamares does it during installation, so let's make it work...
Patch2:		falkon-3.1.0-fix-running-as-root.patch
Patch3:		falkon-3.1.0-native-scrollbars.patch
Patch4:		falkon-3.1.0-omdv-settings.patch
Patch5:		falkon-3.1.0-menuentry.patch
Patch9:		falkon-3.1.0-compile.patch

BuildRequires:	cmake(ECM)
BuildRequires:	qt5-linguist-tools
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5WebEngine)
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5Script)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(python3)
BuildRequires:	cmake(KF5Wallet)
BuildRequires:	cmake(KF5I18n)
# Optional -- having them enables KDE integration
BuildRequires:	cmake(KF5KIO)
BuildRequires:	cmake(KF5Crash)
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5Purpose)
%if %{with pyside2}
BuildRequires:	cmake(PySide2)
BuildRequires:	cmake(Shiboken2)
%endif
BuildRequires:	gettext-devel
Requires:	%{name}-core = %{EVRD}
Suggests:	%{name}-plugins = %{EVRD}
Requires:	qt5-qtbase-database-plugin-sqlite
Requires:	%{_lib}qt5-output-driver-default
Provides:	webclient
Requires:	distro-release-indexhtml
Requires:	xdg-utils
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
%{_datadir}/applications/org.kde.falkon.desktop
%{_datadir}/metainfo/org.kde.falkon.appdata.xml
%dir %{_qt5_plugindir}/%{name}

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
%{_qt5_plugindir}/%{name}/*.so
%exclude %{_qt5_plugindir}/%{name}/GnomeKeyringPasswords.so
%exclude %{_qt5_plugindir}/%{name}/KDEFrameworksIntegration.so
%if %{with pyside2}
%{_qt5_plugindir}/%{name}/middleclickloader
%{_qt5_plugindir}/%{name}/runaction
%endif

#----------------------------------------------------------------------------

%package gnome-keyring
Summary:	GNOME Keyring integration plugin for %{name}
Group:		Networking/WWW
Requires:	%{name} = %{EVRD}
Conflicts:	%{name}-plugins < 3.1.0-5

%description gnome-keyring
GNOME Keyring integration plugin.

%files gnome-keyring
%{_qt5_plugindir}/%{name}/GnomeKeyringPasswords.so

#----------------------------------------------------------------------------

%package kde
Summary:	KDE Frameworks Integration plugin for %{name}
Group:		Networking/WWW
Requires:	%{name} = %{EVRD}
Conflicts:	%{name}-plugins < 3.1.0-5

%description kde
Plugin for Falkon adding support for:
- storing passwords securely in KWallet,
- additional URL protocols using KIO (e.g., man:, info:, gopher:, etc.),
- a "Share page" menu using the KDE Purpose Framework,
- intercepting crashes with KCrash, bringing up the DrKonqi crash handler.

%files kde
%{_qt5_plugindir}/%{name}/KDEFrameworksIntegration.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{oname}-%{version}
dos2unix README.md

%build
export PORTABLE_BUILD="false"

%cmake_kde5 -DDISABLE_DBUS:BOOL=FALSE \
	-DSHIBOKEN_BINARY=%{_bindir}/shiboken2 \
	-DSHIBOKEN_INCLUDE_DIR=%{_includedir}/shiboken2 \
	-DSHIBOKEN_PYTHON_INCLUDE_DIR=%{_includedir}/python3.7m \
	-DSHIBOKEN_LIBRARY=$(ls %{_libdir}/libshiboken2.cpython-3*.so) \
	-DPYSIDE_LIBRARY=$(ls %{_libdir}/libpyside2.cpython-3*.so) \
	-DPYSIDE_INCLUDE_DIR=%{_includedir}/PySide2

%ninja_build

%install
%ninja_install -C build

# remove useless plugins
rm -fv %{buildroot}%{_qt5_plugindir}/%{name}/TestPlugin.so
rm -rfv %{buildroot}%{_qt5_plugindir}/%{name}/qml/helloqml

# find_lang can't deal with the strange mix of .mo and .qm style
# translations all put in the same place, so let's do the right thing
# manually
TOPDIR="$(pwd)"
cd %{buildroot}
find .%{_datadir}/locale -type f -name "*.qm" -o -name "*.mo" |while read r; do
    printf '%%%%lang(%%s) %%s\n' $(echo $r |cut -d/ -f5) $(echo $r |cut -b2-) >>"$TOPDIR"/%{name}.lang
done
