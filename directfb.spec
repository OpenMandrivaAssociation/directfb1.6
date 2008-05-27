%define	name	directfb
%define version 1.0.1
%define release %mkrel 2
%define	oname	DirectFB
%define api 1.0
%define	major	0
%define	libname	%mklibname %{name} %{api}_%{major}
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
License:	GPL
Group:		System/Libraries
Source0:	http://www.directfb.org/downloads/Core/%{oname}-%{version}.tar.gz
# from Debian
Patch0:		03_link_static_sysfs.patch
Patch1:		08_link_static_ar.patch
Patch2:		DirectFB-1.0.1-underlink.patch
URL:		http://www.directfb.org/
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	freetype2-devel >= 2.0.2
BuildRequires:	libsysfs2-devel
BuildRequires:  kernel-source
BuildRequires:  automake1.8
BuildRequires:	SDL-devel
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
# required for systems/libdirectfb_fbdev.{so,a} (find-requires does not look in subdirs)
Requires:	libsysfs-static-devel
Obsoletes:	%mklibname %name 1.0_0 -d

%description -n	%develname
DirectFB header files for building applications based on %oname. 

%package	doc
Summary:	DirectFB - documentation
Group:		Books/Computer books

%description	doc
DirectFB documentation and examples.

%prep
%setup  -q -n %{oname}-%{version}
%patch0 -p0 -b .sysfs
%patch1 -p0 -b .ar
%patch2 -p1

perl -p -i -e 's@-L/usr/X11R6/lib@@;s@-I/usr/X11R6/include@@' \
    configure.in directfb-config.in

aclocal-1.8
autoconf
automake-1.8 -a -c

%build
CFLAGS="$RPM_OPT_FLAGS -O3" \
%configure2_5x \
	--disable-maintainer-mode \
	--enable-shared \
	--enable-static \
	--disable-fast-install \
	--disable-avifile \
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
# we don't ship these ATM, libtool relink problem
#rm -f %buildroot/%_bindir/dfbg
#rm -f %buildroot/%_mandir/man1/dfbg.1
#rm -f %buildroot/%_bindir/dfbdump
#rm -f %buildroot/%_bindir/dfbinfo
#rm -f %buildroot/%_bindir/dfblayer

# multiarch policy
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/directfb-config

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(644,root,root,755)
%doc README* AUTHORS NEWS TODO
%attr(755,root,root) %{_libdir}/lib*%{api}.so.%{major}*
%exclude %{_libdir}/directfb-%{api}-%major/*/*.a
%exclude %{_libdir}/directfb-%{api}-%major/*/*/*.a
%{_libdir}/directfb-%{api}-%major
%{_datadir}/directfb-%{version}


%files -n %develname
%defattr(755,root,root,755)
%{_bindir}/directfb-config
%multiarch %{multiarch_bindir}/directfb-config
%{_bindir}/directfb-csource
%{_bindir}/dfblayer
%{_bindir}/dfbdump
%{_bindir}/dfbg
%{_bindir}/dfbinfo
%{_bindir}/dfbinput
%{_bindir}/dfbpenmount
%{_bindir}/dfbscreen
%{_bindir}/dfbsummon
%{_bindir}/mkdfiff
%{_bindir}/mkdgiff
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
%{_libdir}/*.la
%{_libdir}/directfb-%{api}-%major/*/*.a
%{_libdir}/directfb-%{api}-%major/*/*/*.a

%files doc
%defattr(644,root,root,755)
%doc docs/html/*


