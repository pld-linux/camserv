Summary:	A streaming web video server and utilities
Summary(pl):	Serwer strumieni obrazu z WWW i narzêdzia
Name:		camserv
Version:	0.5.1
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/cserv/%{name}-%{version}.tar.gz
# Source0-md5:	ad6a1c9a5b522a4ee2189c66d7fbda72
Patch0:		%{name}-link.patch
Patch1:		%{name}-errno.patch
URL:		http://cserv.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdk-pixbuf-devel >= 0.14.0
BuildRequires:	imlib2-devel >= 1.0.5
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libltdl-devel
BuildRequires:	libtool
Requires:	gdk-pixbuf >= 0.14.0
Requires:	imlib2 >= 1.0.5
Requires:	libjpeg >= 6b
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Camserv is an extremely modular program for doing streaming video from
your Unix machine to web clients. Filters can be added for text on the
displayed window, and anything else one wants to add.

In addition portability to other unices should be incredibly easy
given the modularity of the camera plugin modules.

Utilities for camera broadcast webserver offloading are also included.

%description -l pl
Camserv jest skrajnie modularnym programem do tworzenia strumieni
obrazu dla klientów sieciowych. Mog± byæ dodane filtry dla tekstu w
wy¶wietlanym okienku, a tak¿e wszystkiego innego, co chcia³oby siê
dodaæ.

Ponadto powinien byæ ³atwo przeno¶ny na inne uniksy dziêki
modularno¶ci wtyczek dla kamer.

Do³±czono tak¿e narzêdzia do obs³ugi serwera obrazu z kamer.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

rm -rf libltdl

%build
%{__libtoolize} --ltdl
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
cd libltdl
%{__autoconf}
cd ..
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO javascript.txt
%attr(755,root,root) %{_bindir}/camserv
%attr(755,root,root) %{_bindir}/relay
%dir %{_datadir}/camserv
%{_datadir}/camserv/camserv.cfg
%{_datadir}/camserv/defpage.html
%dir %{_libdir}/camserv
%attr(755,root,root) %{_libdir}/camserv/libvideo_v4l.so*
%{_libdir}/camserv/libvideo_v4l.la
%attr(755,root,root) %{_libdir}/camserv/libvideo_basic.so*
%{_libdir}/camserv/libvideo_basic.la
%attr(755,root,root) %{_libdir}/camserv/libtext_filter.so*
%{_libdir}/camserv/libtext_filter.la
%attr(755,root,root) %{_libdir}/camserv/librand_filter.so*
%{_libdir}/camserv/librand_filter.la
%attr(755,root,root) %{_libdir}/camserv/libgdk_pixbuf_filter.so*
%{_libdir}/camserv/libgdk_pixbuf_filter.la
%attr(755,root,root) %{_libdir}/camserv/libimlib2_filter.so*
%{_libdir}/camserv/libimlib2_filter.la
%attr(755,root,root) %{_libdir}/camserv/libjpg_filter.so*
%{_libdir}/camserv/libjpg_filter.la
