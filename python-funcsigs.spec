# centos/sclo spec file for python-funcsigs, from:
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

%{?scl:          %scl_package        python-funcsigs}
%{!?scl:         %global pkg_name    %{name}}

%global pypi_name funcsigs

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           %{?sub_prefix}python-%{pypi_name}
Version:        1.0.2
Release:        5%{?dist}
Summary:        Python function signatures from PEP362 for Python 2.6, 2.7 and 3.2+

License:        ASL 2.0
URL:            https://github.com/testing-cabal/funcsigs?
Source0:        https://pypi.io/packages/source/f/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  %{?scl_prefix}python-sphinx
#BuildRequires:  %{?scl_prefix}python-unittest2

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
funcsigs is a backport of the PEP 362 function signature features from
Python 3.3's inspect module. The backport is compatible with Python 2.6, 2.7
as well as 3.2 and up.

%package -n %{?sub_prefix}python-%{pypi_name}-doc
Summary:        funcsigs documentation

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{pypi_name}-doc = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{pypi_name}-doc = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{pypi_name}-doc = %{version}-%{release}
%endif
%endif

%description -n %{?sub_prefix}python-%{pypi_name}-doc
Documentation for funcsigs

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%if 0%{?rhel} && 0%{?rhel} <= 7
sed -i '/extras_require/,+3d' setup.py
%endif

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build

# generate html docs
sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{?scl:EOF}


%check
#{?scl:scl enable %{scl} - << \EOF}
#{__python} setup.py test
#{?scl:EOF}

%files
%{!?_licensedir:%global license %%doc}
%doc README.rst
%license LICENSE
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n %{?sub_prefix}python-%{pypi_name}-doc
%{!?_licensedir:%global license %%doc}
%doc html
%license LICENSE

%changelog
* Wed Jul 26 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.0.2-4
- Enable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.0.2-3
- Rebuild for Python 3.6
- Disable python3 tests for now

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Jun 11 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.2-1
- Upstream 1.0.2 (RHBZ#1341262)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec  4 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.4-2
- Add license file in doc subpackage

* Wed Dec 02 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.4-1
- Initial package.
