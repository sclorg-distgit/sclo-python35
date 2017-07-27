# centos/sclo spec file for python-pbr, from:
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

%{?scl:          %scl_package        python-pbr}
%{!?scl:         %global pkg_name    %{name}}

%global pypi_name pbr
%global do_test 0

Name:           %{?sub_prefix}python-%{pypi_name}
Version:        1.10.0
Release:        4.1%{?dist}
Summary:        Python Build Reasonableness

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/pbr
Source0:        https://pypi.io/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

# not in a released version yet https://review.openstack.org/413795
Patch0001:      0001-Don-t-raise-exception-on-missing-man-pages.patch

BuildArch:      noarch

BuildRequires: %{?scl_prefix}python-sphinx >= 1.1.3
BuildRequires: %{?scl_prefix}python-devel
Requires:      %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{pypi_name} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{pypi_name} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{pypi_name} = %{version}-%{release}
%endif
%endif

%if 0%{?do_test} == 1
BuildRequires:  %{?scl_prefix}python-coverage
BuildRequires:  %{?scl_prefix}python-hacking
BuildRequires:  %{?scl_prefix}python-mock
BuildRequires:  %{?scl_prefix}python-testrepository
BuildRequires:  %{?scl_prefix}python-testresources
BuildRequires:  %{?scl_prefix}python-testscenarios
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gnupg
%endif


%description
PBR is a library that injects some useful and sensible default behaviors into 
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18 
different projects each with at least 3 active branches, it seems like a good 
time to make that code into a proper re-usable library.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch0001 -p1

rm -rf {test-,}requirements.txt pbr.egg-info/requires.txt

%build
%{?scl:scl enable %{scl} - << \EOF}
export SKIP_PIP_INSTALL=1
%{__python} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/pbr/tests
%{?scl:EOF}

%if 0%{?do_test}
%check
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py test
%{?scl:EOF}
%endif

%files 
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc html README.rst
%{_bindir}/pbr
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{pypi_name}

%changelog
* Thu Jul 27 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 18 2017 Alan Pevec <apevec AT redhat.com> - 1.10.0-4
- Fix newer Sphinx and Python 3.5 support LP#1379998

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.10.0-2
- Rebuild for Python 3.6

* Wed Oct 12 2016 Alan Pevec <apevec AT redhat.com> - 1.10.0-1
- Update to 1.10.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4 2016 Paul Belanger <pabelanger@redhat.com> 1.8.1-3
- Provide python2-pbr (rhbz#1282126)
- minor spec cleanup

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 12 2015 Alan Pevec <alan.pevec@redhat.com> 1.8.1-1
- Update to 1.8.1

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 14 2015 Alan Pevec <alan.pevec@redhat.com> 1.8.0-1
- Update to upstream 1.8.0

* Tue Sep 08 2015 Alan Pevec <alan.pevec@redhat.com> 1.7.0-1
- Update to upstream 1.7.0

* Mon Aug 31 2015 Matthias Runge <mrunge@redhat.com> - 1.6.0-1
- update to upstream 1.6.0 (rhbz#1249840)

* Sat Aug 15 2015 Alan Pevec <alan.pevec@redhat.com> 1.5.0-1
- Update to upstream 1.5.0

* Wed Jul 15 2015 Alan Pevec <alan.pevec@redhat.com> 1.3.0-1
- Update to upstream 1.3.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Alan Pevec <apevec@redhat.com> - 0.11.0-1
- update to 0.11.0

* Fri Mar 20 2015 Alan Pevec <apevec@redhat.com> - 0.10.8-1
- update to 0.10.8

* Mon Dec 29 2014 Alan Pevec <apevec@redhat.com> - 0.10.7-1
- update to 0.10.7

* Tue Nov 25 2014 Matthias Runge <mrunge@redhat.com> - 0.10.0-1
- update to 0.10.0 (rhbz#1191232)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 30 2014 Matthias Runge <mrunge@redhat.com> - 0.8.0-1
- update to 0.8.0 (rhbz#1078761)

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-2
- Added python3 subpackage.
- slight modification of Ralph Beans proposal

* Mon Mar 24 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-1
- update to 0.7.0 (rhbz#1078761)

* Tue Feb 11 2014 Matthias Runge <mrunge@redhat.com> - 0.6.0-1
- update to 0.6.0 (rhbz#1061124)

* Fri Nov 01 2013 Matthias Runge <mrunge@redhat.com> - 0.5.23-1
- update to 0.5.23 (rhbz#1023926)

* Tue Aug 13 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-2
- add requirement python-pip (rhbz#996192)
- remove requirements.txt

* Thu Aug 08 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-1
- update to 0.5.21 (rhbz#990008)

* Fri Jul 26 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-2
- remove one buildrequires: python-sphinx

* Mon Jul 22 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-1
- update to python-pbr-0.5.19 (rhbz#983008)

* Mon Jun 24 2013 Matthias Runge <mrunge@redhat.com> - 0.5.17-1
- update to python-pbr-0.5.17 (rhbz#976026)

* Wed Jun 12 2013 Matthias Runge <mrunge@redhat.com> - 0.5.16-1
- update to 0.5.16 (rhbz#973553)

* Tue Jun 11 2013 Matthias Runge <mrunge@redhat.com> - 0.5.14-1
- update to 0.5.14 (rhbz#971736)

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-2
- remove requirement setuptools_git
- fix docs build under rhel

* Fri May 17 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-1
- update to 0.5.11 (rhbz#962132)
- disable tests, as requirements can not be fulfilled right now

* Thu Apr 25 2013 Matthias Runge <mrunge@redhat.com> - 0.5.8-1
- Initial package.
