# centos/sclo spec file for python-requests-kerberos, from:
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

%{?scl:          %scl_package        python-requests-kerberos}
%{!?scl:         %global pkg_name    %{name}}

%global upstream_name requests-kerberos
%global module_name requests_kerberos
%global commit0 75d29584a0c40a17a0bed8f228707bf53f703fdc
%global gittag0 v0.10.0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           %{?sub_prefix}python-%{upstream_name}
Version:        0.10.0
Release:        4%{?dist}
Summary:        A Kerberos authentication handler for python-requests
License:        MIT
URL:            https://github.com/requests/requests-kerberos
# Upstream considers Github not PyPI to be the authoritative source tarballs:
# https://github.com/requests/requests-kerberos/pull/78
Source0:        https://github.com/requests/requests-kerberos/archive/%{commit0}.tar.gz#/%{upstream_name}-%{shortcommit0}.tar.gz
# Upstream has switched their requirement to the "pykerberos" fork, but for now 
# we still have the original "kerberos" module in Fedora.
Patch1:         0001-switch-requirement-from-pykerberos-back-to-kerberos.patch
BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
#BuildRequires:  %{?scl_prefix}python-pytest
BuildRequires:  %{?scl_prefix}python-mock

Requires:       %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{upstream_name} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{upstream_name} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{upstream_name} = %{version}-%{release}
%endif
%endif

Requires:       %{?scl_prefix}python-requests >= 1.1
Requires:       %{?scl_prefix}python-kerberos
# runtime requirements are needed for tests also
BuildRequires:  %{?scl_prefix}python-requests >= 1.1
BuildRequires:  %{?scl_prefix}python-kerberos


%description
Requests is an HTTP library, written in Python, for human beings. This library 
adds optional Kerberos/GSSAPI authentication support and supports mutual 
authentication.


%prep
%setup -q -n %{upstream_name}-%{commit0}
%patch1 -p1

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%check
#{?scl:scl enable %{scl} - << \EOF}
#py.test-2 test_requests_kerberos.py
#%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{?scl:EOF}

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst AUTHORS HISTORY.rst
%{python_sitelib}/%{module_name}
%{python_sitelib}/%{module_name}*.egg-info

%changelog
* Fri Jul 28 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 12 2016 Dan Callaghan <dcallagh@redhat.com> - 0.10.0-1
- upstream bug fix release 0.10.0:
  https://github.com/requests/requests-kerberos/blob/v0.10.0/HISTORY.rst#0100-2016-05-18

* Fri Jul 01 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-5
- add Obsoletes for python -> python2 rename

* Fri Jul 01 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-4
- build for Python 2 and 3 (RHBZ#1334415)
- use %%license
- run tests in %%check

* Thu Feb 11 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-3
- really fix requirements for kerberos module (#1305986)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Dan Callaghan <dcallagh@redhat.com> - 0.8.0-1
- upstream release 0.8.0 (#1296743)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dan Callaghan <dcallagh@redhat.com> - 0.7.0-2
- relaxed version in kerberos module requirement, to work with
  python-kerberos 1.1 (#1215565)

* Tue May 05 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0 (#1164464)

* Fri Nov 07 2014 Dan Callaghan <dcallagh@redhat.com> - 0.6-1
- fix for mutual authentication handling (RHBZ#1160545, CVE-2014-8650)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Dan Callaghan <dcallagh@redhat.com> - 0.5-1
- upstream bug fix release 0.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Dan Callaghan <dcallagh@redhat.com> - 0.3-1
- upstream bug fix release 0.3

* Mon May 27 2013 Dan Callaghan <dcallagh@redhat.com> - 0.2-2
- require requests >= 1.0

* Tue May 14 2013 Dan Callaghan <dcallagh@redhat.com> - 0.2-1
- initial version
