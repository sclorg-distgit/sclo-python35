# centos/sclo spec file for python-kerberos, from:
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

%{?scl:          %scl_package        python-kerberos}
%{!?scl:         %global pkg_name    %{name}}


%global srcname kerberos
%global sum A high-level wrapper for Kerberos (GSSAPI) operations

Name:           %{?sub_prefix}python-%{srcname}
Version:        1.2.5
Release:        3%{?dist}
Summary:        %{sum}

Group:          System Environment/Libraries
License:        ASL 2.0
# SVN browser is at https://trac.calendarserver.org/browser/PyKerberos
URL:            https://pypi.python.org/pypi/kerberos
Source0:        https://pypi.python.org/packages/source/k/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        LICENSE

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  krb5-devel

# Accept principal=None in authGSSClientInit. Upstream ticket
# https://www.calendarserver.org/ticket/942
Patch1:         python-kerberos-942.patch

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{srcname} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{srcname} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{srcname} = %{version}-%{release}
%endif
%endif

%global desc This Python package is a high-level wrapper for Kerberos (GSSAPI) operations.\
The goal is to avoid having to build a module that wraps the entire\
Kerberos framework, and instead offer a limited set of functions that do what\
is needed for client/server Kerberos authentication based on\
<http://www.ietf.org/rfc/rfc4559.txt>.

%description
%{desc}

%prep
%setup -q -n %{srcname}-%{version}
%patch1 -p1

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
install -m 644 $RPM_SOURCE_DIR/LICENSE LICENSE 

%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{?scl:EOF}

%files 
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python_sitearch}/*

%changelog
* Fri Jul 28 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.5-2
- Rebuild for Python 3.6

* Tue Jul 19 2016 Rob Crittenden <rcritten@redhat.com> - 1.2.5-1
- Update to upstream 1.2.5. Fixes single bug,
  http://www.calendarserver.org/changeset/15659
- Include LICENSE since upstream dropped it from the tarball

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 11 2016 Rob Crittenden <rcritten@redhat.com> - 1.2.4-2
- Accept principal=None in authGSSClientInit, upstream issue 942 (#1354334)

* Thu Feb 18 2016 Michal Schmidt <mschmidt@redhat.com> - 1.2.4-1
- Update to current upstream release.
- Build for both python2 and python3.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 15 2015 Rob Crittenden <rcritten@redhat.com> - 1.1-18
- Move LICENSE to the license tag instead of doc.
 
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Rob Crittenden <rcritten@redhat.com> - 1.1-14
- Fix calculation of username string length in authenticate_gss_client_wrap
  (#1057338)

* Fri Jan 17 2014 Rob Crittenden <rcritten@redhat.com> - 1.1-13
- Add patch to allow inquiring the current client credentials

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Rob Crittenden <rcritten@redhat.com> - 1.1-11
- Fix version in setup.py so egg information is correct (#975202)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Simo Sorce <ssorce@redhat.com> - 1.1-3.1
- Fix minor issue with delegation patch

* Fri Dec 12 2008 Simo Sorce <ssorce@redhat.com> - 1.1-3
- Add delegation patch

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1-2
- Rebuild for Python 2.6

* Thu Nov 27 2008 Simo Sorce <ssorce@redhat.com> - 1.1-1
- New Upstream Release
- Remove patches as this version has them included already

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-6
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Rob Crittenden <rcritten@redhat.com> - 1.0-5
- Package the egg-info too

* Wed Jan 16 2008 Rob Crittenden <rcritten@redhat.com> - 1.0-4
- Switch from python_sitelib macro to python_sitearch
- Add python-setuptools to BuildRequires

* Wed Jan 16 2008 Rob Crittenden <rcritten@redhat.com> - 1.0-3
- Use the setup.py install target in order to generate debuginfo.

* Thu Jan  3 2008 Rob Crittenden <rcritten@redhat.com> - 1.0-2
- Add krb5-devel to BuildRequires

* Wed Jan  2 2008 Rob Crittenden <rcritten@redhat.com> - 1.0-1
- Change name to python-kerberos from PyKerberos
- Change license from "Apache License" to ASL 2.0 per guidelines
- Upstream released 1.0 which is equivalent to version 1541. Reverting
  to that.

* Tue Aug 28 2007 Rob Crittenden <rcritten@redhat.com> - 0.1735-2
- Include GSS_C_DELEG_FLAG in gss_init_sec_context() so the command-line
  tools can do kerberos ticket forwarding.

* Tue Jul 31 2007 Rob Crittenden <rcritten@redhat.com> - 0.1735-1
- Initial rpm version
