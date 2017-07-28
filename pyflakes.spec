# centos/sclo spec file for pyflakes, from:
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

%{?scl:          %scl_package        pyflakes}
%{!?scl:         %global pkg_name    %{name}}

%{?scl:
%filter_from_provides s|/opt/rh/.*/root/usr/bin/python.*||g;s|python.*abi.*$||g;
%filter_from_requires s|/opt/rh/.*/root/usr/bin/python.*||g;s|python.*abi.*$||g;
%filter_setup
}

Name:           %{?sub_prefix}pyflakes
Version:        1.5.0
Release:        4.1%{?dist}
Summary:        A simple program which checks Python source files for errors

License:        MIT
URL:            https://github.com/PyCQA/pyflakes

Source0:        https://files.pythonhosted.org/packages/source/p/%{name}/%{pkg_name}-%{version}.tar.gz
Source1:        http://cdn.debian.net/debian/pool/main/p/pyflakes/pyflakes_1.3.0-1.debian.tar.xz
Patch0:         %{pkg_name}-1.1.0-python3-man.patch

BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python-devel >= 2.5
BuildRequires:  %{?scl_prefix}python-setuptools
Requires:       %{?scl_prefix}python-setuptools
Requires:        %{?scl_prefix}python

Provides:       %{?scl_prefix}python-pyflakes = %{version}-%{release}

%if 0%{?scl:1}
Provides: %{?scl_prefix}pyflakes = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-pyflakes = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-pyflakes = %{version}-%{release}
%endif
%endif

%global desc Pyflakes is similar to PyChecker in scope, but differs in that it does\
not execute the modules to check them. This is both safer and faster,\
although it does not perform as many checks. Unlike PyLint, Pyflakes\
checks only for logical errors in programs; it does not perform any\
check on style.

%description
%{desc}

%prep
%setup -q -a 1 -n %{pkg_name}-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
rm -rf %{buildroot}

%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mv %{buildroot}%{_bindir}/pyflakes %{buildroot}%{_bindir}/pyflakes-%{python_version}
ln -s pyflakes-%{python_version} %{buildroot}%{_bindir}/pyflakes-2
install -Dpm 644 debian/pyflakes.1 %{buildroot}%{_mandir}/man1/pyflakes-%{python_version}.1
ln -s pyflakes-%{python_version}.1 %{buildroot}%{_mandir}/man1/pyflakes-2.1

ln -s pyflakes-%{python_version} %{buildroot}%{_bindir}/pyflakes
ln -s pyflakes-%{python_version}.1 %{buildroot}%{_mandir}/man1/pyflakes.1

%{?scl:EOF}


%check
%{?scl:scl enable %{scl} - << \EOF}
%{__python} -Wall setup.py test
%{?scl:EOF}


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc AUTHORS NEWS.txt README.rst
%{_bindir}/pyflakes-%{python_version}
%{_bindir}/pyflakes-2
%{python_sitelib}/pyflakes*
%exclude %{python_sitelib}/pyflakes/test/
%{_mandir}/man1/pyflakes-%{python_version}.1*
%{_mandir}/man1/pyflakes-2.1*
%{_bindir}/pyflakes
%{_mandir}/man1/pyflakes.1*

%changelog
* Fri Jul 28 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Fri Jun 30 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-4
- Point unversioned pyflakes executable to Python 3 in F27+ and EL8+
- Provide python2-pyflakes

* Fri May 26 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-3
- Run tests with -Wall

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-1
- Update to 1.5.0

* Sun Jan  1 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.4.0-1
- Update to 1.4.0

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.3.0-4
- Rebuild for Python 3.6

* Thu Dec  8 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.3.0-3
- Unconditionalize python3 build

* Wed Sep 14 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.3.0-2
- Add standard versioned names for executables and man pages (#1374381)

* Fri Sep  2 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.3.0-1
- Update to 1.3.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May 13 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.3-1
- Update to 1.2.3
- Build python3 on EL7

* Sat May  7 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-1
- Update to 1.2.2

* Fri May  6 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.1-1
- Update to 1.2.1

* Wed May  4 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.0-1
- Update to 1.2.0

* Tue Mar  1 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-1
- Update to 1.1.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.0.0-2
- Rebuild

* Mon Sep 21 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.0.0-1
- Update to 1.0.0
- Specfile cleanups per current guidelines

* Wed Jun 17 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.9.2-1
- Update to 0.9.2

* Wed Jun 10 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.9.1-1
- Update to 0.9.1

* Mon Jun  1 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.9.0-1
- Update to 0.9.0
- Specfile cleanup and guidelines update
- Improve python3-pyflakes manpage

* Sat Jan 31 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.8.1-4
- Ship LICENSE as %%license where available
- Don't try to build with python3 on EL7 by default

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 31 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.8.1-1
- Update to 0.8.1

* Wed Mar 26 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.8-1
- Update to 0.8

* Wed Dec 11 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-4
- Avoid interfering with pies in version check (#1039706, Timothy Crosley).
- Refresh Debian additions tarball.

* Mon Sep  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-3
- Build Python 3 version (#1004668).
- Add dependency on setuptools.
- Update summary and description.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-1
- Update to 0.7.3.

* Mon Apr 29 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.2-1
- Update to 0.7.2.

* Tue Apr 23 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.1-1
- Update to 0.7.1.

* Thu Apr 18 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7-1
- Update to 0.7.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Feb  5 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.6.1-1
- Update to 0.6.1.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep  5 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.5.0-2
- Bring back null byte input traceback patch.
- Include LICENSE and NEWS.txt in docs.

* Sun Sep  4 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.0-1
- Update to 0.5.0
- Remove patches that no longer apply

* Mon Apr  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-5
- Avoid traceback on input with null bytes (#691164).

* Sun Feb 13 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-4
- Backport upstream changes for set and dict comprehension support (#677032).
- Add man page and file descriptor close patch from Debian.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Mar 19 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-1
- Update to 0.4.0.

* Wed Nov  4 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.3.0-1
- Update to 0.3.0 (#533015).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.1-4
- Rebuild for Python 2.6

* Sat Dec  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-3
- Correctly identify the license

* Sat Dec  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-2
- Revert to released tarball

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-1.10526svn
- Fix version number

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-1.10526svn
- Fix up versioning

* Tue Dec  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.1.10526
- First version for Fedora Extras
