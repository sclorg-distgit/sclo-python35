# centos/sclo spec file for python-pysocks, from:
#
# Fedora spec file
#

%if 0%{?scl:1}
 %if "%{scl}" == "rh-python34"
  %global sub_prefix sclo-python34-
  %global with_python3 1
 %else
  %if "%{scl}" == "rh-python35"
   %global sub_prefix sclo-python35-
   %global with_python3 1
  %else 
   %global sub_prefix sclo-%{scl_prefix}
   %global with_python3 0	
  %endif
 %endif
%endif

%{?scl:          %scl_package        python-pysocks}
%{!?scl:         %global pkg_name    %{name}}


%{!?_licensedir: %global license %%doc}

%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#FIXME: junk in %{buildroot}/%{python_sitelib}/__pycache__
%define _unpackaged_files_terminate_build 0


%global distname PySocks
%global flatname pysocks
%global sum     A Python SOCKS client module

Name:               %{?sub_prefix}python-pysocks
Version:            1.5.7
Release:            4%{?dist}
Summary:            %{sum}

License:            BSD
URL:                https://github.com/Anorov/PySocks
Source0:            https://github.com/Anorov/PySocks/archive/%{version}.tar.gz
BuildArch:          noarch

BuildRequires:      %{?scl_prefix}python-devel

Requires:    %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-pysocks = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-pysocks = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-pysocks = %{version}-%{release}
%endif
%endif

%description
A fork of SocksiPy with bug fixes and extra features.

Acts as a drop-in replacement to the socket module. Featuring:

- SOCKS proxy client for Python 2.6 - 3.x
- TCP and UDP both supported
- HTTP proxy client included but not supported or recommended (you should use
  urllib2's or requests' own HTTP proxy interface)
- urllib2 handler included.

%prep
%autosetup -n %{distname}-%{version}

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
rm -rvf %{buildroot}/%{python_sitelib}/__pycache__
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rvf %{buildroot}/%{python_sitelib}/__pycache__
%{?scl:EOF}

#%%check
## No tests included in the tarball...
## https://github.com/Anorov/PySocks/issues/37
#%%{__python2} setup.py test

%files 
# https://github.com/Anorov/PySocks/issues/42
#%%doc README.md
# https://github.com/Anorov/PySocks/issues/43
#%%license LICENSE
%{python_sitelib}/socks.py*
%{python_sitelib}/sockshandler.py*
%{python_sitelib}/%{distname}-%{version}*


%changelog
* Thu Jul 27 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.5.7-3
- Rebuild for Python 3.6

* Mon Nov 28 2016 Tim Orling <ticotimo@gmail.com> - 1.5.7-2
- Ship python34-pysocks in EL6

* Sat Sep 17 2016 Kevin Fenzi <kevin@scrye.com> - 1.5.7-1
- Update to 1.5.7

* Fri Sep 16 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.6-6
- Ship python34-pysocks in EPEL7

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-4
- Change our conflicts on python-SocksiPy to an obsoletes/provides.
  https://bugzilla.redhat.com/show_bug.cgi?id=1334407

* Mon May 09 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-3
- Fix typo in explicit conflicts.

* Tue May 03 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-2
- We don't actually need setuptools here.

* Mon May 02 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-1
- Initial package for Fedora
