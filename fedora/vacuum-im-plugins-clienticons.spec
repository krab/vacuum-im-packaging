%define app_name vacuum-im

Name: #PKGNAME#
Summary: Client Icons plugin for Vacuum-IM
Version: #VER#+git#CDATE#
Release: #REL#
License: GPLv3
Group: System/Libraries
Source: #SRC#
Url: https://github.com/Vacuum-IM/clienticons
BuildRequires: vacuum-im-devel
BuildRequires: qt-devel 
BuildRequires: cmake xz
 
%description
Displays a client icon in the roster.

%prep
%setup -q -n %{name}
 
%build
%{__mkdir} build
cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo\
         -DGIT_HASH=#GIT_HASH#\
         -DGIT_DATE=#GIT_DATE#\
         -DCMAKE_INSTALL_PREFIX=%{_prefix}\
         -DINSTALL_LIB_DIR=%{_lib}\
         -DINSTALL_APP_DIR=%{app_name}\
         -DINSTALL_DOC_DIR=%{_defaultdocdir}\
         -DVACUUM_LIB_PATH=%{_prefix}/%{_lib}\
         -DVACUUM_SDK_PATH=%{_includedir}/%{app_name}
%{__make} %{?_smp_mflags}
 
%install
pushd build
%{make_install}
popd

%files
%defattr(-,root,root)
%{_libdir}/%{app_name}
%dir %{_libdir}/%{app_name}/plugins
%{_datadir}/%{app_name}
 
%changelog
* #DATE# Alexey N. Ivanov <alexey.ivanes@gmail.com> - #VER#+git#CDATE#-#REL#
- Build git commit hash #GIT_HASH# 