# centos/sclo spec file for python-tox, from:
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

%{?scl:          %scl_package        python-tox}
%{!?scl:         %global pkg_name    %{name}}

# Tests requiring Internet connections are disabled by default
# pass --with internet to run them (e.g. when doing a local rebuild
# for sanity checks before committing)
%bcond_with internet


%global pypiname tox
Name:           %{?sub_prefix}python-tox
Version:        1.8.1
Release:        2%{?dist}
Summary:        Virtualenv-based automation of test activities

# file toxbootstrap.py is licensed under MIT License
License:        GPLv2+ and MIT
URL:            http://codespeak.net/tox
Source0:        http://pypi.python.org/packages/source/t/%{pypiname}/%{pypiname}-%{version}.tar.gz


BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
Requires:  %{?scl_prefix}python-py
Requires:  %{?scl_prefix}python-virtualenv >= 1.11.2
# required for check
%if 0%{?fedora}
BuildRequires:  %{?scl_prefix}python-py
BuildRequires:  %{?scl_prefix}pytest
BuildRequires:  %{?scl_prefix}python-virtualenv >= 1.11.2
%endif

Requires:    %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{pypiname} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{pypiname} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{pypiname} = %{version}-%{release}
%endif
%endif


%description
Tox as is a generic virtualenv management and test command line tool you 
can use for:

 - checking your package installs correctly with different Python versions 
   and interpreters
 - running your tests in each of the environments, configuring your test tool 
   of choice
 - acting as a frontend to Continuous Integration servers, greatly reducing 
   boilerplate and merging CI and shell-based testing.

%prep
%setup -q -n %{pypiname}-%{version}

# remove bundled egg-info
rm -rf %{pypiname}.egg-info

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{?scl:EOF}

# if internet connection available, run tests
%if %{with internet}
%check
# python 2.7: fedora 17, fedora 18
# python 3.2: fedora 17
# python 3.3: fedora 18

# el6: buildrequirements missing
#%if 0%{?rhel}==6
#TOXENV=py26 %{__python} setup.py test
#%endif

%if 0%{?fedora}>=17 
%{?scl:scl enable %{scl} - << \EOF}
TOXENV=py27 %{__python} setup.py test
%{?scl:EOF}
%endif

%endif
 
%files
%{!?_licensedir:%global license %%doc}
%doc LICENSE ISSUES.txt doc
%{_bindir}/%{pypiname}
%{_bindir}/%{pypiname}-quickstart
%{python_sitelib}/%{pypiname}
%{python_sitelib}/%{pypiname}-%{version}-py*egg-info


%changelog
* Thu Jul 27 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 16 2014 Matthias Runge <mrunge@redhat.com> - 1.8.1-1
- update to 1.8.1

* Wed Aug 13 2014 Matthias Runge <mrunge@redhat.com> - 1.7.1-3
- Fix ConfigError: ConfigError: substitution key 'posargs' not found
  (rhbz#1127961, rhbz#1128562)

* Wed Jul 30 2014 Matthias Runge <mrunge@redhat.com> - 1.7.1-2
- require virtualenv >= 1.11.2 (rhbz#1122603)

* Tue Jul 08 2014 Matthias Runge <mrunge@redhat.com> - 1.7.1-1
- update to 1.7.1 (rhbz#111797)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 24 2013 Matthias Runge <mrunge@redhat.com> - 1.6.1-1
- update to 1.6.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-7
- add requires python-py, python-virtualenv (rhbz#876246)

* Thu Oct 18 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-6
- change license to GPLv2+ and MIT

* Tue Oct 16 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-5
- totally disable python3 support for now

* Fri Oct 12 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-4
- conditionalize checks, as internet connection required, not available on koji

* Thu Oct 11 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-3
- buildrequirement: virtualenv
- disable python3-tests because of missing build-requirement python3-virtualenv

* Wed Oct 10 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-2
- include tests

* Tue Oct 09 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-1
- initial packaging
