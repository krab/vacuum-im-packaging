%define cmake_build_dir build
%define sname vacuum
%define libname libvacuumutils36

Name:             #PKGNAME#
Version:          #VER#+git#CDATE#
Release:          #REL#
Summary:          Client application for the Jabber network

License:          GPLv3
Group:            Applications/Internet
URL:              https://github.com/Vacuum-IM/vacuum-im
Source0:          #SRC#

BuildRequires:    cmake
BuildRequires:    hunspell-devel
BuildRequires:    libidn-devel
BuildRequires:    libXScrnSaver-devel
BuildRequires:    minizip-devel
BuildRequires:    openssl-devel
BuildRequires:    qt-devel
BuildRequires:    qt-webkit-devel
BuildRequires:    qtlockedfile-devel
BuildRequires:    zlib-devel

%description
The core program is just a plugin loader - all functionality is made available
via plugins. This enforces modularity and ensures well defined component
interaction via interfaces. Supported XMPP extension protocols.

%package -n %{libname}
Summary:          Shared library libvacuumutils for Vacuum-IM
License:          GPLv3
Group:            System/Libraries
Conflicts:        libvacuumutils1_7

%description -n %{libname}
This package includes shared libraris needed to work Vacuum-IM program.

%package devel
Summary:          Shared library and header files for the %{name}
License:          GPLv3
Group:            Development/Libraries
Requires:         %{name} = %{version}
Requires:         %{libname} = %{version}

%description devel
The %{name}-devel package contains API documentation for developing %{name}.

%prep
%setup -q -n %{name}

%build
mkdir %{cmake_build_dir}
pushd %{cmake_build_dir}
    cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo\
             -DGIT_HASH=#GIT_HASH#\
             -DGIT_DATE=#GIT_DATE#\
             -DINSTALL_SDK=1\
             -DCMAKE_INSTALL_PREFIX=%{_prefix}\
             -DINSTALL_APP_DIR=%{name}\
             -DINSTALL_LIB_DIR=%{_lib}\
             -DINSTALL_DOC_DIR=%{_defaultdocdir}\
             -DSPELLCHECKER_BACKEND=HUNSPELL
    make %{?_smp_mflags}
popd

%install
pushd %{cmake_build_dir}
    make install DESTDIR=$RPM_BUILD_ROOT
popd

#remove unversion doc
rm -rf %{buildroot}%{_datadir}/doc/%{name}

install -D -m644 %{buildroot}%{_datadir}/%{name}/resources/menuicons/shared/mainwindowlogo128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png 
install -D -m644 %{buildroot}%{_datadir}/%{name}/resources/menuicons/shared/mainwindowlogo96.png %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/%{name}.png 
install -D -m644 %{buildroot}%{_datadir}/%{name}/resources/menuicons/shared/mainwindowlogo64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png 
install -D -m644 %{buildroot}%{_datadir}/%{name}/resources/menuicons/shared/mainwindowlogo48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png 
install -D -m644 %{buildroot}%{_datadir}/%{name}/resources/menuicons/shared/mainwindowlogo32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png 
install -D -m644 %{buildroot}%{_datadir}/%{name}/resources/menuicons/shared/mainwindowlogo24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png 
install -D -m644 %{buildroot}%{_datadir}/%{name}/resources/menuicons/shared/mainwindowlogo16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
sed -i "s/Exec=%{sname}/Exec=%{name}/;s/Icon=%{sname}/Icon=%{name}/" %{buildroot}%{_datadir}/applications/%{sname}.desktop
mv %{buildroot}%{_datadir}/applications/%{sname}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
mv %{buildroot}%{_datadir}/pixmaps/%{sname}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
mv %{buildroot}%{_bindir}/%{sname} %{buildroot}%{_bindir}/%{name}

%post
/sbin/ldconfig
touch --no-create /usr/share/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create /usr/share/icons/hicolor &>/dev/null
    gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc COPYING CHANGELOG AUTHORS README TRANSLATORS
%{_bindir}/%{name}
%{_libdir}/%{name}/plugins
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/*.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libvacuumutils.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/%{name}
%{_libdir}/libvacuumutils.so

%changelog
* #DATE# Alexey N. Ivanov <alexey.ivanes@gmail.com> - #VER#+git#CDATE#-#REL#
- Build git commit hash #GIT_HASH# 
