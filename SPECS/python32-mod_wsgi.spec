%global pymajor 3
%global pyminor 2
%global pyver %{pymajor}.%{pyminor}
%global iusver %{pymajor}%{pyminor}u
%global __python3 %{_bindir}/python%{pyver}
%global python3_sitelib  %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global srcname mod_wsgi

Name:           python%{iusver}-%{srcname}
Version:        4.1.1
Release:        1.ius%{?dist}
Summary:        A WSGI interface for Python web applications in Apache
Vendor:         IUS Community Project
Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://modwsgi.readthedocs.org
Source0:        https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}.tar.gz
Source1:        python32-mod_wsgi.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
make LDFLAGS="-L%{_libdir}" %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf

mv  %{buildroot}%{_libdir}/httpd/modules/mod_wsgi.so \
    %{buildroot}%{_libdir}/httpd/modules/%{name}.so

%clean
rm -rf $RPM_BUILD_ROOT

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
* Fri May 30 2014 Ben Harper <ben.harper@rackspace.com> - 4.1.1-1.ius
- Latest sources from upstream

* Tue Sep 04 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-1.ius
- Latest sources
- See if 3.4 resolves https://bugs.launchpad.net/ius/+bug/1045118

* Mon Jul 30 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.3-4.ius
- New build for python32
