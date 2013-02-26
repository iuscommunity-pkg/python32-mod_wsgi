
%global pybasever 3.2
%global pyver 32
%global real_name mod_wsgi

# not supported by python32 in IUS currently
#%%global __os_install_post %{__python26_os_install_post}
%global __python %{_bindir}/python%{pybasever}

Name:           python%{pyver}-mod_wsgi
Version:        3.4
Release:        1.ius%{?dist}
Summary:        A WSGI interface for Python web applications in Apache

Group:          System Environment/Libraries
License:        ASL 2.0
Vendor:         IUS Community Project
URL:            http://modwsgi.org
Source0:        http://modwsgi.googlecode.com/files/%{real_name}-%{version}.tar.gz 
Source1:        python32-mod_wsgi.conf 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
BuildRequires:  python%{pyver}, python%{pyver}-devel
Provides:       %{real_name} = %{version}

Obsoletes:      mod_wsgi-python%{pyver} < 3.2-2
Provides:       mod_wsgi-python%{pyver} = %{version}-%{release}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep 
%setup -q -n %{real_name}-%{version}


%build
%configure --with-python=python%{pybasever}
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
%doc LICENCE README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_libdir}/httpd/modules/%{name}.so


%changelog
* Tue Sep 04 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-1.ius
- Latest sources
- See if 3.4 resolves https://bugs.launchpad.net/ius/+bug/1045118

* Mon Jul 30 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.3-4.ius
- New build for python32
