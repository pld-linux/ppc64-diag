# TODO: PLDify init scripts
Summary:	Diagnostics tools for Linux on Power platform
Summary(pl.UTF-8):	Narzędzia diagnostyczne dla Linuksa na platformie Power
Name:		ppc64-diag
Version:	2.7.6
Release:	0.1
License: 	GPL v2+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
# Source0-md5:	06d356203a432720911189919f6fdeec
Patch0:		%{name}-install.patch
URL:		http://linux-diag.sourceforge.net/ppc64-diag/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	librtas-devel
BuildRequires:	libservicelog-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libvpd-devel >= 2
BuildRequires:	ncurses-devel
BuildRequires:	sqlite3-devel
BuildRequires:	udev-devel
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	lsvpd >= 0.14
Requires:	rc-scripts
Requires:	servicelog >= 1.1
Conflicts:	powerpc-utils-ibm < 1.2.15
ExclusiveArch:	ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Platform diagnostics for Linux for Power writes events reported by the
System p or System i platform firmware to the servicelog, provides
automated responses to urgent events such as environmental conditions
and predictive failures, and provides notifications of the event to
system administrators or connected service frameworks. Some error log
analysis parameters can be configured in
/etc/ppc64-diag/ppc64-diag.config.

%description -l pl.UTF-8
System diagnostyczny dla Linuksa na platformie Power zapisuje
zdarzenia zgłaszane przez firmware platformy Systemu p lub Systemu i
do logu serwisowego (servicelog), zapewnia automatyczne odpowiedzi na
pilne zdarzenia (jak np. warunki środowiskowe czy przewidywane awarie)
oraz powiadomienia o zdarzeniach dla administratorów lub podłączonych
systemów serwisowych. Pewne parametry analizy logów błędów można
ustawić w /etc/ppc64-diag/ppc64-diag.config.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ppc64-diag

%clean
rm -rf $RPM_BUILD_ROOT

%post
/etc/ppc64-diag/ppc64_diag_setup --register >/dev/null
/sbin/chkconfig --add rtas_errd
%service rtas_errd restart

%preun
if [ "$1" = "0" ]; then
	%service -q rtas_errd stop
	/sbin/chkconfig --del rtas_errd
	/etc/ppc64-diag/ppc64_diag_setup --unregister >/dev/null
fi
%{nil}

# trigger on librtas upgrades
%triggerin -- librtas
if [ "$2" = "2" ]; then
	/etc/rc.d/init.d/rtas_errd restart
fi

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_sbindir}/add_regex
%attr(755,root,root) %{_sbindir}/convert_dt_node_props
%attr(755,root,root) %{_sbindir}/diag_encl
%attr(755,root,root) %{_sbindir}/encl_led
%attr(755,root,root) %{_sbindir}/explain_syslog
%attr(755,root,root) %{_sbindir}/extract_opal_dump
%attr(755,root,root) %{_sbindir}/extract_platdump
%attr(755,root,root) %{_sbindir}/lp_diag
%attr(755,root,root) %{_sbindir}/opal-dump-parse
%attr(755,root,root) %{_sbindir}/opal-elog-parse
%attr(755,root,root) %{_sbindir}/opal_errd
%attr(755,root,root) %{_sbindir}/rtas_errd
%attr(755,root,root) %{_sbindir}/syslog_to_svclog
%attr(755,root,root) %{_sbindir}/usysattn
%attr(755,root,root) %{_sbindir}/usysfault
%attr(755,root,root) %{_sbindir}/usysident
%dir %{_sysconfdir}/ppc64-diag
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppc64-diag/ppc64-diag.config
%attr(754,root,root) %{_sysconfdir}/ppc64-diag/lp_diag_notify
%attr(754,root,root) %{_sysconfdir}/ppc64-diag/lp_diag_setup
%attr(754,root,root) %{_sysconfdir}/ppc64-diag/ppc64_diag_*
%{_sysconfdir}/ppc64-diag/servevent_parse.pl
%dir %{_sysconfdir}/ppc64-diag/message_catalog
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/cxgb3
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/e1000e
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/exceptions
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/gpfs
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/reporters
%dir %{_sysconfdir}/ppc64-diag/message_catalog/with_regex
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/with_regex/cxgb3
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/with_regex/e1000e
%config(noreplace) %{_sysconfdir}/ppc64-diag/message_catalog/with_regex/gpfs
#/etc/cron.daily/run_diag_encl
%config(noreplace) /etc/rc.powerfail
%config(noreplace) /etc/rc.d/init.d/opal_errd
%config(noreplace) /etc/rc.d/init.d/rtas_errd
%{systemdunitdir}/opal_errd.service
%{systemdunitdir}/rtas_errd.service
%dir /var/log/ppc64-diag
%{_mandir}/man8/diag_encl.8*
%{_mandir}/man8/encl_led.8*
%{_mandir}/man8/explain_syslog.8*
%{_mandir}/man8/lp_diag.8*
%{_mandir}/man8/opal-dump-parse.8*
%{_mandir}/man8/opal-elog-parse.8*
%{_mandir}/man8/opal_errd.8*
%{_mandir}/man8/syslog_to_svclog.8*
%{_mandir}/man8/usysattn.8*
%{_mandir}/man8/usysfault.8*
%{_mandir}/man8/usysident.8*
