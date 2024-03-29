Summary:	A streaming web video server and utilities
Summary(pl.UTF-8):	Serwer strumieni obrazu z WWW i narzędzia
Name:		camserv
Version:	0.5.1
Release:	3
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/cserv/%{name}-%{version}.tar.gz
# Source0-md5:	ad6a1c9a5b522a4ee2189c66d7fbda72
Source1:	%{name}.init
Source2:	%{name}-relay.init
Source3:	%{name}-relay.sysconfig
Patch0:		%{name}-link.patch
Patch1:		%{name}-errno.patch
URL:		http://cserv.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdk-pixbuf-devel >= 0.14.0
BuildRequires:	imlib2-devel >= 1.0.6
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	gdk-pixbuf >= 0.14.0
Requires:	imlib2 >= 1.0.5
Requires:	libjpeg >= 6b
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Camserv is an extremely modular program for doing streaming video from
your Unix machine to web clients. Filters can be added for text on the
displayed window, and anything else one wants to add.

In addition portability to other unices should be incredibly easy
given the modularity of the camera plugin modules.

Utilities for camera broadcast webserver offloading are also included.

%description -l pl.UTF-8
Camserv jest skrajnie modularnym programem do tworzenia strumieni
obrazu dla klientów sieciowych. Mogą być dodane filtry dla tekstu w
wyświetlanym okienku, a także wszystkiego innego, co chciałoby się
dodać.

Ponadto powinien być łatwo przenośny na inne uniksy dzięki
modularności wtyczek dla kamer.

Dołączono także narzędzia do obsługi serwera obrazu z kamer.

%package relay
Summary:	Relay for camserv
Summary(pl.UTF-8):	Przekaźnik dla camserva
Group:		Networking
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description relay
Relay for camserv.

%description relay -l pl.UTF-8
Przekaźnik dla camserva.

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
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sysconfdir}/%{name},/etc/{sysconfig,rc.d/init.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-relay
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-relay

mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.cfg
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/defpage.html $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/defpage.html

ln -s %{_sysconfdir}/%{name}/%{name}.cfg $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}.cfg
ln -s %{_sysconfdir}/%{name}/defpage.html $RPM_BUILD_ROOT%{_datadir}/%{name}/defpage.html

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%post relay
/sbin/chkconfig --add %{name}-relay
%service %{name}-relay restart

%preun relay
if [ "$1" = "0" ]; then
	%service %{name}-relay stop
	/sbin/chkconfig --del %{name}-relay
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO javascript.txt
%attr(755,root,root) %{_bindir}/camserv
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/defpage.html
%dir %{_datadir}/camserv
%{_datadir}/camserv/camserv.cfg
%{_datadir}/camserv/defpage.html
%dir %{_libdir}/camserv
%attr(755,root,root) %{_libdir}/camserv/lib*.so*
%{_libdir}/camserv/lib*.la
%attr(754,root,root) /etc/rc.d/init.d/%{name}

%files relay
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/relay
%attr(754,root,root) /etc/rc.d/init.d/%{name}-relay
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}-relay
