%define	oname	DirectFB
%define api	1.7
%define major	3
%define libdirectfb	%mklibname %{name} %{api} %{major}
%define	libdirect	%mklibname direct %{api} %{major}
%define	libppdfb	%mklibname ++dfb %{api} %{major}
%define	libfusion	%mklibname fusion %{api} %{major}
%define	libdavinci	%mklibname davinci %{api} %{major}
%define devname %mklibname %{name} %{api} -d

# Multiple applications support
# Requires fusion kernel module
%define build_multi	0
%{?_without_multi: %{expand: %%global build_multi 0}}
%{?_with_multi: %{expand: %%global build_multi 1}}

Summary:	Hardware graphics acceleration library
Name:		directfb
Version:	1.7.3
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.directfb.org/
Source0:	http://www.directfb.org/downloads/Core/%{oname}-%{api}/%{oname}-%{version}.tar.xz
# from Debian
Patch0:		03_link_static_sysfs.patch
Patch1:		DirectFB-1.6.1-link-static-ar.patch
# Explicitly link with -lm. Was failing only on x86_64, but not on i586,
# apparently because -O3 was generating code to bypass libm on i586.
Patch3:		DirectFB-1.2.7-sincos-x86_64.patch
# remove common linkage of x11 system and x11 input driver
# it makes directfb segfault
# (this is a workaround, not a proper upstreamable fix)
Patch4:		DirectFB-1.4.2-x11-linkage.patch
# from Debian #401296, 93_fix_unicode_key_handling.patch
Patch6:		DirectFB-1.4.2-unicode.patch
Patch7:		DirectFB-1.7.3-svg-includedir.patch
Patch8:		DirectFB-1.6.1-zlib.patch
Patch9:		DirectFB-1.5.3-add-missing-davinci-files.patch
Patch10:	DirectFB-1.6.1-gcc-atomics-on-arm.patch
Patch11:	DirectFB-1.6.3-atomic-fix-compiler-error-when-building-for-thumb2.patch

Conflicts:	%mklibname directfb -d < 1.7
BuildRequires:	bzip2-devel
BuildRequires:	jpeg-devel
BuildRequires:	sysfsutils-devel
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libsvg-cairo)
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	pkgconfig(tslib-0.0)
BuildRequires:	pkgconfig(vdpau)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(zlib)
%if %{build_multi}
BuildRequires:	fusion-devel >= 3.0
%endif

%description
DirectFB hardware graphics acceleration - libraries.

%package -n %{libdirectfb}
Summary:	Shared library part of %{oname}
Group:		System/Libraries

%description -n %{libdirectfb}
DirectFB hardware graphics acceleration - libraries.

This package contains the %{oname} shared library and interface modules.
It's required for running apps based on %{oname}.


%package -n	%{libdirect}
Summary:	The direct library, a part of directfb
Group:		System/Libraries

%description -n	%{libdirect}
The direct library, a part of directfb


%package -n	%{libppdfb}
Summary:	The ++dfb library, a part of directfb
Group:		System/Libraries

%description -n	%{libppdfb}
The ++dfb library, a part of directfb


%package -n	%{libfusion}
Summary:	The fusion library, a part of directfb
Group:		System/Libraries

%description -n	%{libfusion}
The fusion library, a part of directfb

%package -n	%{libdavinci}
Summary:	The davinci library, a part of directfb
Group:		System/Libraries

%description -n	%{libdavinci}
The davinci library, a part of directfb

%package -n %{devname}
Group:		Development/C
Summary:	Header files for compiling DirectFB applications
Requires:	%{libdirectfb} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
DirectFB header files for building applications based on %{oname}.

%package doc
Summary:	DirectFB - documentation
Group:		Books/Computer books

%description doc
DirectFB documentation and examples.

%prep
%setup  -q -n %{oname}-%{version}
%patch0 -p1 -b .sysfs~
%patch1 -p1 -b .link-static-ar~
%patch3 -p1
%patch4 -p1 -b .x11-linkage~
%patch6 -p1 -b .unicode~
%patch7 -p1 -b .svgdir~
%patch8 -p1 -b .zlib~
%patch9 -p1 -b .davinci~
%patch10 -p1 -b .atomic~
%patch11 -p1 -b .thumb~

# Needed for Qt 5 as of Qt 5.0.1:
sed -i -e '/define __typeof/d' lib/direct/os/linux/glibc/types.h
find . -name "*.h" |xargs sed -i -e 's,__typeof__,typeof,g'

autoreconf -if

%build
%configure2_5x \
	--disable-maintainer-mode \
	--enable-shared \
	--disable-fast-install \
	--disable-debug \
	--enable-zlib \
%ifarch %{ix86}
	--disable-mmx \
	--disable-sse \
%endif
%if %build_multi
	--enable-multi
%else
	--disable-multi
%endif

%make LIBS="-lbz2 -ldl -pthread -lpthread"

%install
%makeinstall_std

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/directfb-config


%files
%ifarch %{arm}
%{_bindir}/c64xdump
%endif
%{_bindir}/dfb*
%{_bindir}/directfb*
%{_bindir}/mkd*
%{_bindir}/pxa3xx_dump
%{_datadir}/%{name}-%{version}
%{_libdir}/%{name}-%{api}-%{major}

%files -n %{devname}
%{multiarch_bindir}/directfb-config
%{_includedir}/directfb
%{_includedir}/directfb-internal
%{_includedir}/++dfb
%{_mandir}/man1/directfb-csource.1*
%{_mandir}/man1/dfbg.1*
%{_mandir}/man5/directfbrc.5*
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%files -n %{libdirectfb}
%{_libdir}/libdirectfb-%{api}.so.%{major}*

%files -n %{libdirect}
%{_libdir}/libdirect-%{api}.so.%{major}*

%files -n %{libppdfb}
%{_libdir}/lib++dfb-%{api}.so.%{major}*

%files -n %{libfusion}
%{_libdir}/libfusion-%{api}.so.%{major}*

%ifarch %{armx}
%files -n %{libdavinci}
%{_libdir}/libdavinci-%{api}.so.%{major}*
%endif

%files doc
%doc docs/html/*
%doc README* AUTHORS NEWS TODO
