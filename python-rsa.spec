# centos/sclo spec file for python-rsa, from:
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

%{?scl:          %scl_package        python-rsa}
%{!?scl:         %global pkg_name    %{name}}

%global pypi_name rsa

Name:           %{?sub_prefix}python-%{pypi_name}
Version:        3.4.2
Release:        4%{?dist}
Summary:        Pure-Python RSA implementation

License:        ASL 2.0
URL:            http://stuvel.eu/rsa
Source0:        https://pypi.python.org/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  %{?scl_prefix}python-pyasn1
Requires:       %{?scl_prefix}python-pyasn1
Requires:       %{?scl_prefix}python-setuptools


%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{pypi_name} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{pypi_name} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{pypi_name} = %{version}-%{release}
%endif
%endif

%description
Python-RSA is a pure-Python RSA implementation. It supports encryption
and decryption, signing and verifying signatures, and key generation
according to PKCS#1 version 1.5. It can be used as a Python library as
well as on the command-line.

%prep
%setup -q -n %{pypi_name}-%{version}
# This is a dirty workaround for EL6
#{?el6:rm -rf %{pypi_name}.egg-info}
#{?el6:sed -i "s/pyasn1 >= 0.1.3/pyasn1 >= 0/" setup.py}

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{?scl:EOF}

%files 
%{!?_licensedir:%global license %doc}
%doc README.md
%license LICENSE

%{_bindir}/pyrsa-priv2pub
%{_bindir}/pyrsa-keygen
%{_bindir}/pyrsa-encrypt
%{_bindir}/pyrsa-decrypt
%{_bindir}/pyrsa-sign
%{_bindir}/pyrsa-verify
%{_bindir}/pyrsa-encrypt-bigfile
%{_bindir}/pyrsa-decrypt-bigfile
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%check
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py test
%{?scl:EOF}

%changelog
* Mon Jul 31 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.4.2-2
- Rebuild for Python 3.6

* Sat Oct 29 2016 Fabio Alessnadro Locati <fale@fedoraproject.org> - 3.4.2-1
- Update to 3.4.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Mar 26 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1

* Fri Mar 18 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 3.4-1
- Bump to 3.4
- Remove the patch that is no longer needed since it has been merged upstream

* Tue Feb 09 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 3.3-5
- Fix bug #1305644

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 3.3-3
- Fix bug #1303660

* Wed Jan 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 3.3-2
- Fix for EL6 and EPEL7

* Wed Jan 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 3.3-1
- Update to current upstream
- Fix CVE-2016-1494
- Bring spec compliant with current policy

* Tue Dec  8 2015 Paul Howarth <paul@city-fan.org> - 3.1.4-3
- Fix FTBFS (Debian Bug #804430)
- Run the tests for both python2 and python3

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 13 2015 Paul Howarth <paul@city-fan.org> - 3.1.4-1
- Update to 3.1.4 (#1226667)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.1.1-6
- Add Python 3 subpackage

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-4
- Fix build in F20
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-2
- Change license name, remove MANIFEST.in

* Sun May 19 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-1
- Initial packaging
