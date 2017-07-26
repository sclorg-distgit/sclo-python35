# centos/sclo spec file for python-unittest2, from:
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

%{?scl:          %scl_package        python-unittest2}
%{!?scl:         %global pkg_name    %{name}}


# Created by pyp2rpm-1.1.1
%global pypi_name unittest2
%global with_python3 1
%global bootstrap_traceback2 1

Name:           %{?sub_prefix}python-%{pypi_name}
Version:        1.1.0
Release:        9%{?dist}
Summary:        The new features in unittest backported to Python 2.4+

License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        https://pypi.python.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# we don't need this in Fedora, since we have Python 2.7, which has argparse
Patch0:         unittest2-1.1.0-remove-argparse-from-requires.patch
# we only apply this if bootstrap_traceback2 == 1
Patch1:         unittest2-1.1.0-remove-traceback2-from-requires.patch
# this patch backports tests from Python 3.5, that weren't yet merged, thus the tests are failing
#  (the test is modified to also pass on Python < 3.5)
#  TODO: submit upstream
Patch2:         unittest2-1.1.0-backport-tests-from-py3.5.patch
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  %{?scl_prefix}python-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  %{?scl_prefix}python-traceback2
Requires:       %{?scl_prefix}python-traceback2
%endif
Requires:       %{?scl_prefix}python-setuptools
Requires:       %{?scl_prefix}python-six
Requires:       %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{pypi_name} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{pypi_name} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{pypi_name} = %{version}-%{release}
%endif
%endif

%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%patch0 -p0
%patch2 -p0
%if 0%{?bootstrap_traceback2}
%patch1 -p0
%endif


%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
pushd %{buildroot}%{_bindir}
mv unit2 unit2-%{python_version}
ln -s unit2-%{python_version} unit2-2
ln -s unit2-2 unit2
popd
%{?scl:EOF}


%check
%if ! 0%{?bootstrap_traceback2}
%{?scl:scl enable %{scl} - << \EOF}
%{__python} -m unittest2
%{?scl:EOF}
%endif # bootstrap_traceback2


%files 
%doc README.txt
%{_bindir}/unit2
%{_bindir}/unit2-2
%{_bindir}/unit2-%{python_version}
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%changelog
* Wed Jul 26 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-8
- Disable bootstrap method

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May 19 2016 Carl George <carl.george@rackspace.com> - 1.1.0-5
- Implement new Python packaging guidelines (python2 subpackage)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.1.0-3
- Fix tests on Python 3.5

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.1.0-2
- traceback2 has been bootstrapped.  Remove the bootstrapping conditional

* Thu Nov 12 2015 bkabrda <bkabrda@redhat.com> - 1.1.0-1
- Update to 1.1.0
- Bootstrap dependency on traceback2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Bump to avoid collision with previously blocked 0.8.0-1

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Unretire the package, create a fresh specfile
