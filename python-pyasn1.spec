# centos/sclo spec file for python-pyasn1, from:
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

%{?scl:          %scl_package        python-pyasn1}
%{!?scl:         %global pkg_name    %{name}}

%global module pyasn1
%global modules_version 0.0.8

Name:           %{?sub_prefix}python-pyasn1
Version:        0.2.3
Release:        2%{?dist}
Summary:        ASN.1 tools for Python
License:        BSD
Group:          System Environment/Libraries
Source0:        https://github.com/etingof/pyasn1/archive/v%{version}.tar.gz
# Modules have not been moved to GitHub AFAICT
Source1:        http://downloads.sourceforge.net/pyasn1/pyasn1-modules-%{modules_version}.tar.gz
URL:            http://pyasn1.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python-devel %{?scl_prefix}python-setuptools

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{module} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{module} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{module} = %{version}-%{release}
%endif
%endif

%description
This is an implementation of ASN.1 types and codecs in the Python programming
language.

%package modules
Summary:    Modules for pyasn1
Requires:   %{?scl_prefix}python-pyasn1 >= %{version}-%{release}

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{module}-modules = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{module}-modules = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{module}-modules = %{version}-%{release}
%endif
%endif

%description modules
ASN.1 types modules for python-pyasn1.

%package doc
Summary:        Documentation for pyasn1
BuildRequires:  %{?scl_prefix}python-sphinx
Requires:   %{?scl_prefix}python-pyasn1 >= %{version}-%{release}

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{module}-doc = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{module}-doc = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{module}-doc = %{version}-%{release}
%endif
%endif

%description doc
%{summary}.


%prep
%setup -n %{module}-%{version} -q -b1

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
pushd ../pyasn1-modules-%{modules_version}
%{__python} setup.py build
popd
%{?scl:EOF}

%install
rm -rf $RPM_BUILD_ROOT
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
pushd ../pyasn1-modules-%{modules_version}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd

pushd doc
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitelib}:$PYTHONPATH" make html
rm -f build/html/.buildinfo
popd
%{?scl:EOF}

%check
%{?scl:scl enable %{scl} - << \EOF}
# PYTHONPATH is required because the the tests expect python{,3}-pyasn1
# to be installed.
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitelib}:$PYTHONPATH" %{__python} setup.py test
%{?scl:EOF}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%{!?_licensedir:%global license %%doc}
%defattr(-,root,root,-)
%doc README.md
%license LICENSE.rst
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}-*.egg-info/

%files modules
%defattr(-,root,root,-)
%{python_sitelib}/%{module}_modules/
%{python_sitelib}/%{module}_modules-%{modules_version}-*.egg-info/

%files doc
%{!?_licensedir:%global license %%doc}
%license LICENSE.rst
#FIXME
#doc doc/build/html/*

%changelog
* Mon Jul 31 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Rob Crittenden <rcritten@redhat.com> - 0.2.3-1
- Update to upstream release 0.2.3 (#1426979)
- Adapt to the way upstream changed the way tests are executed
- Pass PYTHONPATH when building the documentation

* Mon Feb  6 2017 Rob Crittenden <rcritten@redhat.com> - 0.2.1-1
- Update to upstream release 0.2.1 (#1419310)
- Added doc subpackage and moved documentation there

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.1.9-8.1
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-7.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Rob Crittenden <rcritten@redhat.com> - 0.1.9-5.1
- Add in missing colon after Provides

* Mon Jan 11 2016 Rob Crittenden <rcritten@redhat.com> - 0.1.9-5
- If python_provide wasn't defined then the python2 subpackages
  didn't provide python-pyasn1-*

* Tue Jan  5 2016 Martin Kosek <mkosek@redhat.com> - 0.1.9-4
- Fix python2 provides for pyasn1 modules (#1295693)

* Mon Jan  4 2016 Rob Crittenden <rcritten@redhat.com> - 0.1.9-3
- Explicitly provide python2 subpackages, use python_provide macro

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 0.1.9-2
- Rebuilt for Python3.5 rebuild

* Mon Oct 19 2015 Rob Crittenden <rcritten@redhat.com> - 0.1.9-1
- Update to new upstream release 0.1.9, modules 0.0.8.

* Sat Aug 15 2015 Rob Crittenden <rcritten@redhat.com> - 0.1.8-2
- Move LICENSE to the license tag instead of doc.

* Wed Jul 15 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.1.8-1
- Update to new upstream release 0.1.8, modules 0.0.6.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Rob Crittenden <rcritten@redhat.com> - 0.1.7-1
- update to upstream release 0.1.7
- update modules to 0.0.5

* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.1.6-1
- update to upstream release 0.1.6
- update modules to 0.0.4
- update description
- add python3-pyasn1 subpackage
- add versioned Requires for the module subpackages
- add %%check section

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 02 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.2-1
- New upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Rob Crittenden <rcritten@redhat.com> - 0.0.12a-1
- Update to upstream version 0.0.12a

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.0.9a-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov 16 2009 Rob Crittenden <rcritten@redhat.com> - 0.0.9a-1
- Update to upstream version 0.0.9a
- Include patch that adds parsing for the Any type

* Wed Sep  2 2009 Rob Crittenden <rcritten@redhat.com> - 0.0.8a-5
- Include doc/notes.html in the package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.0.8a-2
- Rebuild for Python 2.6

* Tue Sep  9 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.8a-1
- Update to upstream version 0.0.8a

* Wed Jan 16 2008 Rob Crittenden <rcritten@redhat.com> - 0.0.7a-4
- Use setuptools to install the package
- simplify the files included in the rpm so it includes the .egg-info

* Mon Jan 14 2008 Rob Crittenden <rcritten@redhat.com> - 0.0.7a-3
- Rename to python-pyasn1
- Spec file cleanups

* Mon Nov 19 2007 Karl MacMillan <kmacmill@redhat.com> - 0.0.7a-2
- Update rpm to be more fedora friendly

* Thu Nov 8 2007 Simo Sorce <ssorce@redhat.com> 0.0.7a-1
- New release

* Mon May 28 2007 Andreas Hasenack <andreas@mandriva.com> 0.0.6a-1mdv2008.0
+ Revision: 31989
- fixed (build)requires
- Import pyasn1

