%global pymajor 3
%global pyminor 2
%global pyver %{pymajor}.%{pyminor}
%global iusver %{pymajor}%{pyminor}
%global __python3 %{_bindir}/python%{pyver}
%global python3_sitelib  %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global srcname mod_wsgi
%global src %(echo %{srcname} | cut -c1)

Name:           python%{iusver}-%{srcname}
Version:        4.2.8
Release:        1.ius%{?dist}
Summary:        A WSGI interface for Python web applications in Apache
Vendor:         IUS Community Project
Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://modwsgi.readthedocs.org
Source0:        https://pypi.python.org/packages/source/%{src}/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        %{name}.conf
BuildRequires:  httpd-devel
BuildRequires:  python%{iusver}-devel
Requires:       httpd
Requires:       python%{iusver}
Provides:       %{srcname} = %{version}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -q -n %{srcname}-%{version}


%build
%configure --with-python=%{__python3}
%{__make} LDFLAGS="-L%{_libdir}" %{?_smp_mflags}


%install
%{__make} install DESTDIR=%{buildroot}
%{__install} -Dpm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__mv} %{buildroot}%{_libdir}/httpd/modules/{%{srcname},%{name}}.so


%posttrans
# hack for previous ius/rackspace mod_wsgi-python32 installs
if [ -e '/etc/httpd/conf.d/wsgi.conf.rpmsave' ]; then
    mv  /etc/httpd/conf.d/python32-mod_wsgi.conf \
        /etc/httpd/conf.d/python32-mod_wsgi.conf.rpmnew
    mv  /etc/httpd/conf.d/wsgi.conf.rpmsave \
        /etc/httpd/conf.d/python32-mod_wsgi.conf

    sed  --in-place=".bak" "s/mod_wsgi.so/python32-mod_wsgi.so/g" \
        /etc/httpd/conf.d/python32-mod_wsgi.conf

    /etc/init.d/httpd graceful
fi


%files
%defattr(-,root,root,-)
%doc LICENCE README.rst
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_libdir}/httpd/modules/%{name}.so


%changelog
* Wed Aug 27 2014 Carl George <carl.george@rackspace.com> - 4.2.8-1.ius
- Latest upstream

* Mon Aug 04 2014 Ben Harper <ben.harper@rackspace.com> - 4.2.7-1.ius
- Latest upstream

* Wed Jul 16 2014 Carl George <carl.george@rackspace.com> - 4.2.6-1.ius
- Latest upstream

* Mon Jul 07 2014 Carl George <carl.george@rackspace.com> - 4.2.5-1.ius
- Latest upstream

* Thu Jun 19 2014 Carl George <carl.george@rackspace.com> - 4.2.4-1.ius
- Get source from pypi instead of github
- Latest sources from upstream

* Thu Jun 05 2014 Carl George <carl.george@rackspace.com> - 4.1.3-1.ius
- Latest sources from upstream

* Mon Jun 02 2014 Carl George <carl.george@rackspace.com> - 4.1.2-1.ius
- Latest sources from upstream
- Implement python packaging best practices
- Fix missing requirements
- Simplify install section

* Fri May 30 2014 Ben Harper <ben.harper@rackspace.com> - 4.1.1-1.ius
- Latest sources from upstream

* Tue Sep 04 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-1.ius
- Latest sources
- See if 3.4 resolves https://bugs.launchpad.net/ius/+bug/1045118

* Mon Jul 30 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.3-4.ius
- New build for python32
