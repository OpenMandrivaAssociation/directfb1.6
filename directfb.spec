%define	name	directfb
%define	oname	DirectFB
%define api	1.5
%define	major	0
%define	libname	%mklibname %{name} %{api} %{major}
%define develname %mklibname %name -d

# Multiple applications support
# Requires fusion kernel module
%define build_multi	0
%{?_without_multi: %{expand: %%global build_multi 0}}
%{?_with_multi: %{expand: %%global build_multi 1}}

Summary:	Hardware graphics acceleration library
Name:		%{name}
Version:	1.5.3
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.directfb.org/
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
# (tpg) add support for libpng-1.5 patch comes from gentoo
Patch11:	DirectFB-1.4.9-libpng-1.5.patch
Patch12:	DirectFB-1.5.1-str-fmt.patch
BuildRequires:	libvncserver-devel
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	freetype2-devel >= 2.0.2
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libsysfs2-devel
BuildRequires:	libvdpau-devel
BuildRequires:	libv4l-devel
BuildRequires:	zlib-devel
%if %{build_multi}
BuildRequires:	fusion-devel >= 3.0
%endif
# prevent linking devel subpackage with older libraries:
# (blino) please uncomment when major is changed
BuildConflicts: directfb-devel

%description
DirectFB hardware graphics acceleration - libraries.

%package -n %{libname}
Summary:	Shared library part of %{oname}
Group:		System/Libraries

%description -n	%{libname}
DirectFB hardware graphics acceleration - libraries.

This package contains the %{oname} shared library and interface modules.
It's required for running apps based on %{oname}.


%package -n %{develname}
Group:		Development/C
Summary:	Header files for compiling DirectFB applications
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}
Provides:	libdirectfb0.9-devel = %{version}-%{release}
Conflicts:	%mklibname -d directfb 0.9_20
Conflicts:	%mklibname -d directfb 0.9_21
Conflicts:	%mklibname -d directfb 0.9_25
Conflicts:	%mklibname -d directfb 1.0_0
Conflicts:	%mklibname -d directfb 1.4_5

%description -n	%{develname}
DirectFB header files for building applications based on %{oname}.

%package doc
Summary:	DirectFB - documentation
Group:		Books/Computer books

%description doc
DirectFB documentation and examples.

%prep
%setup  -q -n %{oname}-%{version}
%patch0 -p1 -b .sysfs
%patch1 -p1 -b .link-static-ar
%patch3 -p1
%patch4 -p1 -b .x11-linkage
#patch5 -p1 -b .reopen
%patch6 -p1 -b .unicode
%patch11 -p1 -b .libpng15
%patch12 -p0 -b .strfmt
autoreconf -if

%build
%configure2_5x \
	--disable-maintainer-mode \
	--enable-shared \
	--disable-static \
	--disable-fast-install \
	--disable-debug \
	--enable-video4linux2 \
	--enable-zlib \
%if %build_multi
	--enable-multi
%else
	--disable-multi
%endif

%make

%install
%makeinstall_std

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/directfb-config

%files -n %{libname}
%{_libdir}/lib*%{api}.so.%{major}*
%{_libdir}/directfb-%{api}-%{major}
%{_datadir}/directfb-%{version}

%files -n %{develname}
%{_bindir}/dfb*
%{_bindir}/directfb*
%{_bindir}/mkd*
%{_bindir}/fluxcomp
%{_bindir}/pxa3xx_dump
%{multiarch_bindir}/directfb-config
%{_includedir}/directfb
%{_includedir}/directfb-internal
%{_mandir}/man1/directfb-csource.1*
%{_mandir}/man1/dfbg.1*
%{_mandir}/man5/directfbrc.5*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%files doc
%doc docs/html/*
%doc README* AUTHORS NEWS TODO
