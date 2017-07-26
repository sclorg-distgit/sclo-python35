# centos/sclo spec file for python-chardet, from:
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

%{?scl:          %scl_package        python-chardet}
%{!?scl:         %global pkg_name    %{name}}

%{?scl:
%filter_from_provides s|/opt/rh/.*/root/usr/bin/python.*||g;s|python.*abi.*$||g
%filter_from_requires s|/opt/rh/.*/root/usr/bin/python.*||g;s|python.*abi.*$||g
%filter_setup
}


%global pypi_name chardet
Name:           %{?sub_prefix}python-%{pypi_name}
Version:        2.3.0
Release:        3%{?dist}
Summary:        Character encoding auto-detection in Python

Group:          Development/Languages
License:        LGPLv2
URL:            https://github.com/%{pypi_name}/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools

Requires: 		%{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{pypi_name} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{pypi_name} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{pypi_name} = %{version}-%{release}
%endif
%endif

%description
Character encoding auto-detection in Python. As 
smart as your browser. Open source.

%prep
%setup -q -n %{pypi_name}-%{version}
sed -ie '1d' %{pypi_name}/chardetect.py

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{?scl:EOF}

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python_sitelib}/*
%{_bindir}/chardetect

%changelog
* Wed Jul 26 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.3.0-2
- Rebuild for Python 3.6

* Wed Jul 27 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-1
- Update to 2.3.0 (#1150536)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 2.2.1-4
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.2.1-2
- fix license handling

* Wed Jul 02 2014 Miro Hrončok <mhroncok@redhat.com> - 2.2.1-1
- Updated to 2.2.1
- Introduced Python 3 subpackage (upstream has merged the codebase)
- Removed BuildRoot and python_sitelib definition
- Use python2 macros instead of just python

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan 13 2010 Kushal Das <kushal@fedoraproject.org> 2.0.1-1
- New release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Aug 04 2008 Kushal Das <kushal@fedoraproject.org> 1.0.1-1
- Initial release

