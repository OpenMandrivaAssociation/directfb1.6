%define	name	directfb
%define version 1.4.12
%define release %mkrel 1
%define	oname	DirectFB
%define api	1.4
%define	major	5
%define	libname	%mklibname %{name} %{api} %{major}
%define develname %mklibname %name -d

# Multiple applications support
# Requires fusion kernel module
%define build_multi	0
%{?_without_multi: %{expand: %%global build_multi 0}}
%{?_with_multi: %{expand: %%global build_multi 1}}

Summary:	Hardware graphics acceleration library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPLv2+
Group:		System/Libraries
Source0:	http://www.directfb.org/downloads/Core/%{oname}-%{version}.tar.gz
# from Debian
Patch0:		03_link_static_sysfs.patch
Patch1:		DirectFB-1.2.7-link-static-ar.patch
# Explicitly link with -lm. Was failing only on x86_64, but not on i586,
# apparently because -O3 was generating code to bypass libm on i586.
Patch3:		DirectFB-1.2.7-sincos-x86_64.patch
# remove common linkage of x11 system and x11 input driver
# it makes directfb segfault
# (this is a workaround, not a proper upstreamable fix)
Patch4:		DirectFB-1.4.2-x11-linkage.patch
# try to reopen console devices when needed
# (for example with splashy after init steals control of consoles)
# reworked from Debian patch, Debian #462626
# might break other directfb apps, Debian #493899
Patch5:		DirectFB-1.2.7-reopen_vt.patch
# from Debian #401296, 93_fix_unicode_key_handling.patch
Patch6:		DirectFB-1.4.2-unicode.patch
Patch9:		DirectFB-1.4.2-wrong-ldflags.patch
Patch10:	DirectFB-1.4.3-libpng-1.4.patch
URL:		http://www.directfb.org/
BuildRequires:	libvncserver-devel
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	freetype2-devel >= 2.0.2
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libsysfs2-devel
%if %{build_multi}
BuildRequires:	fusion-devel >= 3.0
%endif
# prevent linking devel subpackage with older libraries:
# (blino) please uncomment when major is changed
# BuildConflicts: directfb-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
DirectFB hardware graphics acceleration - libraries.

%package -n	%{libname}
Summary:        Shared library part of %oname
Group:		System/Libraries

%description -n	%{libname}
DirectFB hardware graphics acceleration - libraries.

This package contains the %oname shared library and interface modules.
It's required for running apps based on %oname.


%package -n	%develname
Group:		Development/C
Summary:	Header files for compiling DirectFB applications
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}
Provides:	libdirectfb0.9-devel = %{version}-%{release}
Conflicts:	%mklibname -d directfb 0.9_20
Conflicts:	%mklibname -d directfb 0.9_21
Conflicts:	%mklibname -d directfb 0.9_25
Conflicts:	%mklibname -d directfb 1.0_0
# required for systems/libdirectfb_fbdev.{so,a} (find-requires does not look in subdirs)
Requires:	libsysfs-static-devel

%description -n	%develname
DirectFB header files for building applications based on %oname. 

%package	doc
Summary:	DirectFB - documentation
Group:		Books/Computer books

%description	doc
DirectFB documentation and examples.

%prep
%setup  -q -n %{oname}-%{version}
%patch0 -p1 -b .sysfs
%patch1 -p1 -b .link-static-ar
%patch3 -p1
%patch4 -p1 -b .x11-linkage
#patch5 -p1 -b .reopen
%patch6 -p1 -b .unicode
%patch9 -p0 -b .linkage
#patch10 -p1 -b .libpng14
autoreconf -if

%build
%configure2_5x \
	--disable-maintainer-mode \
	--enable-shared \
	--enable-static \
	--disable-fast-install \
	--disable-debug \
	--with-gfxdrivers=ati128,cle266,cyber5k,i810,i830,mach64,neomagic,nsc,nvidia,radeon,savage,sis315,tdfx,unichrome \
%if %build_multi
	--enable-multi
%else
	--disable-multi
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# multiarch policy
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/directfb-config

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(644,root,root,755)
%doc README* AUTHORS NEWS TODO
%attr(755,root,root) %{_libdir}/lib*%{api}.so.%{major}*
%exclude %{_libdir}/directfb-%{api}-%major/*/*.a
%exclude %{_libdir}/directfb-%{api}-%major/*/*/*.a
%exclude %{_libdir}/directfb-%{api}-%major/*/*.o
%exclude %{_libdir}/directfb-%{api}-%major/*/*/*.o
%{_libdir}/directfb-%{api}-%major
%{_datadir}/directfb-%{version}


%files -n %develname
%defattr(755,root,root,755)
%{_bindir}/dfb*
%{_bindir}/directfb*
%{_bindir}/mkd*
%multiarch %{multiarch_bindir}/directfb-config
%defattr(644,root,root,755)
%{_includedir}/directfb
%{_includedir}/directfb-internal
%{_mandir}/man1/directfb-csource.1*
%{_mandir}/man1/dfbg.1*
%{_mandir}/man5/directfbrc.5*
%{_libdir}/pkgconfig/*
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/directfb-%{api}-%major/*/*.a
%{_libdir}/directfb-%{api}-%major/*/*/*.a
%{_libdir}/directfb-%{api}-%major/*/*.o
%{_libdir}/directfb-%{api}-%major/*/*/*.o

%files doc
%defattr(644,root,root,755)
%doc docs/html/*


