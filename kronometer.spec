# uncomment to enable bootstrap mode
%global bootstrap 1

%if !0%{?bootstrap}
%global tests 1
%endif


Name:    kronometer
Summary: A stopwatch application by KDE
Version: 2.2.3
Release: 2%{?dist}

# code (generally) GPLv2, docs GFDL
License: GPLv2 and GFDL
URL:     https://userbase.kde.org/Kronometer

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: https://download.kde.org/%{stable}/%{name}/%{version}/src/%{name}-%{version}.tar.xz


BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: extra-cmake-modules

BuildRequires: cmake(Qt5Core) >= 5.9.0
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5Widgets)

# kf5
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5Crash)
BuildRequires: cmake(KF5DocTools)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5WidgetsAddons)
BuildRequires: cmake(KF5XmlGui)

%if 0%{?tests}
BuildRequires: dbus-x11
BuildRequires: xorg-x11-server-Xvfb
%endif

%description
Kronometer is a stopwatch application.

%prep
%autosetup -p1


%build
%{cmake_kf5} \
  -DBUILD_TESTING:BOOL=%{?tests:ON}%{!?tests:OFF}

%cmake_build


%install
%cmake_install

%find_lang %{name} --all-name --with-html --with-man


%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop ||:
appstream-util validate-relax --nonet %{buildroot}%{_kf5_metainfodir}/org.kde.%{name}.appdata.xml ||:
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a \
dbus-launch --exit-with-session \
make test ARGS="--output-on-failure --timeout 20" -C %{_target_platform} ||:
%endif


%files -f %{name}.lang
%license COPYING*
%{_kf5_datadir}/applications/org.kde.kronometer.desktop
%{_kf5_bindir}/kronometer
%{_kf5_datadir}/config.kcfg/kronometer.kcfg
%{_kf5_metainfodir}/org.kde.kronometer.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/apps/kronometer.*
%{_mandir}/man1/kronometer.1*
%{_mandir}/*/man1/kronometer.1*

%changelog
* Tue Aug 17 2021 Andrea Perotti <aperotti@redhat.com> - 2.2.3-2
- spec cleanup and rebuild for Fedora 34/35

* Sat May 2 2020 Andrea Perotti <aperotti@redhat.com> - 2.2.3-1
- first attempt
  
