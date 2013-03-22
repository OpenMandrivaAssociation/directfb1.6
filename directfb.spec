%define	oname	DirectFB
%define api	1.6
%define major	0
%define libname	%mklibname %{name} %{api} %{major}
%define develname %mklibname %{name} -d

# Multiple applications support
# Requires fusion kernel module
%define build_multi	0
%{?_without_multi: %{expand: %%global build_multi 0}}
%{?_with_multi: %{expand: %%global build_multi 1}}

Summary:	Hardware graphics acceleration library
Name:		directfb
Version:	1.6.3
Release:	2
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.directfb.org/
Source0:	http://directfb.org/downloads/Core/%{oname}-1.6/%{oname}-%{version}.tar.gz
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
Patch7:		DirectFB-1.6.1-svg-includedir.patch
Patch8:		DirectFB-1.6.1-zlib.patch
Patch9:		DirectFB-1.5.3-add-missing-davinci-files.patch
Patch10:	DirectFB-1.6.1-gcc-atomics-on-arm.patch
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libsvg-cairo)
BuildRequires:	pkgconfig(vdpau)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	libvncserver-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(jasper)
BuildRequires:	sysfsutils-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(xproto)
BuildRequires:	bzip2-devel

%if %{build_multi}
BuildRequires:	fusion-devel >= 3.0
%endif

%description
DirectFB hardware graphics acceleration - libraries.

%package -n %{libname}
Summary:	Shared library part of %{oname}
Group:		System/Libraries

%description -n %{libname}
DirectFB hardware graphics acceleration - libraries.

This package contains the %{oname} shared library and interface modules.
It's required for running apps based on %{oname}.


%package -n %{develname}
Group:		Development/C
Summary:	Header files for compiling DirectFB applications
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
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
%patch6 -p1 -b .unicode
%patch7 -p0 -b .svgdir
%patch8 -p1 -b .zlib
%patch9 -p1 -b .davinci
%patch10 -p1 -b .atomic

# Needed for Qt 5 as of Qt 5.0.1:
sed -i -e '/define __typeof/d' lib/direct/os/linux/glibc/types.h
find . -name "*.h" |xargs sed -i -e 's,__typeof__,typeof,g'

autoreconf -if

%build
%configure2_5x \
	--disable-maintainer-mode \
	--enable-shared \
	--disable-static \
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

%files -n %{libname}
%{_libdir}/lib*%{api}.so.%{major}*
%{_libdir}/directfb-%{api}-%{major}
%ifarch %{arm}
%{_libdir}/libdavinci_c64x.so.*
%endif
%{_datadir}/directfb-%{version}

%files -n %{develname}
%ifarch %{arm}
%{_bindir}/c64xdump
%endif
%{_bindir}/dfb*
%{_bindir}/directfb*
%{_bindir}/mkd*
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


%changelog
* Sun May 13 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.3-2
+ Revision: 798654
- enable zlib and v4l support
- update to new version 1.5.3
- drop pacthes 9 and 10
- add patch 12 fix string format
- disable static libraries
- enable support for vdpau
- fix file list
- spec file clean

* Wed Apr 04 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.4.13-4
+ Revision: 789204
- Rebuild for .la files removal.
- Rebuild for .la files removal.

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.13-3
+ Revision: 702704
- rebuild

* Mon Sep 12 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.13-2
+ Revision: 699480
- Patch11: add support against libpng-1.5 (patch from Gentoo)

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - rebuild

* Mon Jul 18 2011 Funda Wang <fwang@mandriva.org> 1.4.13-1
+ Revision: 690216
- new version 1.4.13

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.12-2
+ Revision: 661657
- multiarch fixes

* Mon Apr 18 2011 Funda Wang <fwang@mandriva.org> 1.4.12-1
+ Revision: 655719
- new version 1.4.12

* Thu Dec 16 2010 Funda Wang <fwang@mandriva.org> 1.4.11-1mdv2011.0
+ Revision: 622403
- build x11 backend rather than SDL backend
- new version 1.4.11 ( LIBMAJOR 0->5 )

* Fri Dec 03 2010 Funda Wang <fwang@mandriva.org> 1.4.3-3mdv2011.0
+ Revision: 605773
- disable png14 patch at the time
- add archlinux patch to build with png14

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Wed Feb 17 2010 Frederic Crozat <fcrozat@mandriva.com> 1.4.3-2mdv2010.1
+ Revision: 507128
- Force rebuild

  + Funda Wang <fwang@mandriva.org>
    - update file list

* Mon Feb 15 2010 Funda Wang <fwang@mandriva.org> 1.4.3-1mdv2010.1
+ Revision: 506343
- new version 1.4.3

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-3mdv2010.1
+ Revision: 488746
- rebuilt against libjpeg v8

* Sun Nov 08 2009 Funda Wang <fwang@mandriva.org> 1.4.2-2mdv2010.1
+ Revision: 463046
- rebuild for new sdl

* Sun Nov 08 2009 Funda Wang <fwang@mandriva.org> 1.4.2-1mdv2010.1
+ Revision: 462881
- rediff unicode patch from debian
- New version 1.4.2 (new apiver 1.2->1.4)
- New version 1.2.9

* Thu Sep 24 2009 Olivier Blin <blino@mandriva.org> 1.2.8-4mdv2010.0
+ Revision: 448234
- allow to bootstrap build because of directfb<->sdl (from Arnaud Patard)

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.8-3mdv2010.0
+ Revision: 416611
- rebuilt against libjpeg v7

* Fri Jun 12 2009 Funda Wang <fwang@mandriva.org> 1.2.8-2mdv2010.0
+ Revision: 385364
- fix mis use of ldflags and libadd

* Fri Jun 12 2009 Funda Wang <fwang@mandriva.org> 1.2.8-1mdv2010.0
+ Revision: 385355
- New version 1.2.8

* Wed Mar 25 2009 Olivier Blin <blino@mandriva.org> 1.2.7-2mdv2009.1
+ Revision: 361123
- fix race condition when switching vt and exiting splashy at the same
  time (happens at One shutdown, reproducible using:
   splashy shutdown; sleep 1; splashy_update exit; chvt 1)

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - use default optimization, a.k.a. disable -O3

* Fri Feb 27 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.2.7-1mdv2009.1
+ Revision: 345448
- remove kernel-source dep
- new version
- drop patch 2
- rediff patches 1,3,4,5
- fix format strings

* Sat Oct 11 2008 Funda Wang <fwang@mandriva.org> 1.2.6-1mdv2009.1
+ Revision: 292188
- New version 1.2.6

* Mon Sep 22 2008 Olivier Blin <blino@mandriva.org> 1.2.3-3mdv2009.0
+ Revision: 286745
- fix unicode key handling (rediffed from Debian #401296)
- rework and reenable patch reopening vt, to fix Esc key handling in
  splashy (#44074), and stop screen corruption as a side-effect (#39971)

* Wed Sep 03 2008 Olivier Blin <blino@mandriva.org> 1.2.3-2mdv2009.0
+ Revision: 279799
- remove common linkage of x11 system and x11 input driver, it makes
  directfb segfault
- remove deprecated configure option (avifile is now in extra)

* Tue Aug 19 2008 Olivier Blin <blino@mandriva.org> 1.2.3-1mdv2009.0
+ Revision: 273978
- 1.2.3

* Sun Aug 17 2008 Funda Wang <fwang@mandriva.org> 1.2.2-2mdv2009.0
+ Revision: 272985
- rebuild for new SDL

* Sun Aug 17 2008 Funda Wang <fwang@mandriva.org> 1.2.2-1mdv2009.0
+ Revision: 272913
- disable patch5, as it breaks diretfb
- rediff patch5
- New version 1.2.2 (new api major)

* Wed Aug 06 2008 Olivier Blin <blino@mandriva.org> 1.1.1-4mdv2009.0
+ Revision: 264262
- move object files in devel package (#39636)

* Wed Jul 23 2008 Olivier Blin <blino@mandriva.org> 1.1.1-3mdv2009.0
+ Revision: 242965
- try to reopen console devices when needed, for example by splashy
  which changes root (from Debian package, Debian #462626)
- fix vnc system build (patch from git)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat May 31 2008 Funda Wang <fwang@mandriva.org> 1.1.1-2mdv2009.0
+ Revision: 213618
- rebuild

* Wed May 28 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.1.1-1mdv2009.0
+ Revision: 212696
- Update to latest upstream release 1.1.1.
  Remake patches to allow static build, as some chunks were already applied.

* Tue May 27 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.0.1-3mdv2009.0
+ Revision: 211828
- Explicitily link with -lm due to link failure on x86_64. Reason of no
  failure on i586 seens to be that the compiler generated direct assembly
  calls for the math routines, bypassing libm.
- o Don't search for headers in /usr/X11R6/include neither link with
  libraries under /usr/X11R6/lib.
  o Correct an underlinking problem in the penmount driver.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 08 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.0.1-1mdv2008.1
+ Revision: 95687
- new version

* Tue Jun 26 2007 Thierry Vignaud <tv@mandriva.org> 1.0.0-7mdv2008.0
+ Revision: 44532
- new devel library policy

* Sat Jun 09 2007 Olivier Blin <blino@mandriva.org> 1.0.0-6mdv2008.0
+ Revision: 37708
- require libsysfs-static-devel in devel package

* Sat Jun 09 2007 Olivier Blin <blino@mandriva.org> 1.0.0-5mdv2008.0
+ Revision: 37693
- use .a archives for static linking instead of the .o files (from Debian, required for splashy)
- add sysfs in directfb-config (patch from Debian)
- require libsysfs-devel in devel package

* Sat Jun 09 2007 Olivier Blin <blino@mandriva.org> 1.0.0-4mdv2008.0
+ Revision: 37601
- build static files in devel package

  + Funda Wang <fwang@mandriva.org>
    - Hardcode buildrequires libmajor

* Mon May 21 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.0.0-2mdv2008.0
+ Revision: 29019
- add conflicts with older devel packages

* Tue May 15 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.0.0-1mdv2008.0
+ Revision: 26888
- new version
- new major
- disable matrox driver


* Thu Mar 15 2007 Olivier Blin <oblin@mandriva.com> 0.9.25.1-4mdv2007.1
+ Revision: 144510
- do not buildconflicts with directfb-devel since this package buildrequires SDL-devel which requires directfb-devel (to restore on major change)

  + Thierry Vignaud <tvignaud@mandriva.com>
    - do not package huge (1.3Mb!) ChangeLog

* Sun Feb 18 2007 Anssi Hannula <anssi@mandriva.org> 0.9.25.1-3mdv2007.1
+ Revision: 122544
- rebuild for new libgii
- Import directfb

* Sat May 06 2006 Anssi Hannula <anssi@mandriva.org> 0.9.25.1-2mdk
- add build switch for multi, default disabled
- BuildRequires SDL-devel

* Sat May 06 2006 Götz Waschk <waschk@mandriva.org> 0.9.25.1-1mdk
- update file list
- new major
- drop patch
- New release 0.9.25.1

* Fri Apr 21 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.9.24-5mdk
- rebuild (fix /usr/lib/pkgconfig/directfb-internal.pc version on x86_64)

* Tue Dec 13 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.9.24-4mdk
- rebuild with new libsysfs

* Fri Nov 18 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.9.24-3mdk
- rebuild because devel subpackage got linked with 0.9.22 instead of 0.9.24
  on x86_64

* Thu Nov 03 2005 GÃ¶tz Waschk <waschk@mandriva.org> 0.9.24-2mdk
- rebuild for new directfb

* Wed Nov 02 2005 Götz Waschk <waschk@mandriva.org> 0.9.24-1mdk
- new major
- drop merged patch 2
- New release 0.9.24

* Sat Jul 09 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.22-5mdk
- rebuild so that devel subpackage got linked with 0.9.22 instead of 0.9.21 on
  x86_64

* Sat Jun 18 2005 Götz Waschk <waschk@mandriva.org> 0.9.22-4mdk
- add conflict to fix upgrade from stable

* Sun May 01 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.22-3mdk
- update patch2 to include i830 driver (fix ppc build)

* Sat Apr 30 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.22-2mdk
- rebuild so that devel subpackage got linked with 0.9.22 instead of 0.9.21

* Tue Apr 26 2005 Götz Waschk <waschk@mandriva.org> 0.9.22-1mdk
- drop patch 0
- new major
- New release 0.9.22

* Sat Feb 19 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.21-3mdk
- Patch2: fix build on ppc (don't build savage driver)
- add BuildRequires: libsysfs-devel

* Tue Feb 15 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.21-2mdk
- nuke lib64 rpaths
- fix build, multiarch

* Wed Dec 22 2004 Per Ãyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.21-1mdk
- 0.9.21 (finally!)
- do libtoolize again
- compile with -O3
- ship all binaries again
- drop P1, P2 & P3 (fixed upstream)
- cosmetics

* Wed Sep 29 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.20-2mdk
- merge patches from Debian:
  * fix matrox driver build
  * fix savage driver build (include <linux/fb.h> adequately)
  * fix IDirectFBVideoProvider build (add <linux/videodev2.h> specifically)

