# centos/sclo spec file for python-bottle, from:
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

%{?scl:          %scl_package        python-bottle}
%{!?scl:         %global pkg_name    %{name}}

%global srcname bottle

Name:           %{?sub_prefix}python-%{srcname}
Version:        0.12.9
Release:        5%{?dist}
Summary:        Fast and simple WSGI-framework for small web-applications

Group:          Development/Languages
License:        MIT
URL:            http://bottlepy.org
Source0:        https://github.com/bottlepy/%{srcname}/archive/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools

Requires:    %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{srcname} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{srcname} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{srcname} = %{version}-%{release}
%endif
%endif


%description
Bottle is a fast and simple micro-framework for small web-applications. 
It offers request dispatching (Routes) with URL parameter support, Templates, 
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and 
template engines. All in a single file and with no dependencies other than the 
Python Standard Library.

%prep
%setup -q -n %{srcname}-%{version}
sed -i '/^#!/d' bottle.py

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/bottle.py
%{?scl:EOF}

%check
%{?scl:scl enable %{scl} - << \EOF}
%{__python} test/testall.py verbose
%{?scl:EOF}

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc AUTHORS README.rst
%{python_sitelib}/*

%changelog
* Fri Jul 28 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.12.9-4
- Rebuild for Python 3.6

* Wed Nov 16 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.9-3
- Do not own __pycache__ dir

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.9-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 12 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.9-1
- Update to 0.12.9
- Run tests but ignore python3 failure for now

* Tue Jul 12 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.6-5
- Use modern python packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jul 12 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 0.12.6-1
- resolves rhbz#1093257 - JSON content type not restrictive enough

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.11.6-1
- upstream release 0.11.6
- add python3 subpackage. resolves rhbz#949240
- spec file patch from Haïkel Guémar <hguemar@fedoraproject.org>

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Ian Weller <iweller@redhat.com> - 0.10.7-1
- Update to 0.10.7 (required by python-mwlib)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9.5-1
- Initial spec
