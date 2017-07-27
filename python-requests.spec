# centos/sclo spec file for python-mock, from:
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

%{?scl:          %scl_package        python-requests}
%{!?scl:         %global pkg_name    %{name}}


%global urllib3_unbundled_version 1.15.1

Name:           %{?sub_prefix}python-requests
Version:        2.10.0
Release:        4%{?dist}
Summary:        HTTP library, written in Python, for human beings

License:        ASL 2.0
URL:            https://pypi.io/project/requests
Source0:        https://pypi.io/packages/source/r/requests/requests-%{version}.tar.gz
# Explicitly use the system certificates in ca-certificates.
# https://bugzilla.redhat.com/show_bug.cgi?id=904614
Patch0:         python-requests-system-cert-bundle.patch

# Remove an unnecessary reference to a bundled compat lib in urllib3
# Some discussion with upstream:
# - https://twitter.com/sigmavirus24/status/529816751651819520
# - https://github.com/kennethreitz/requests/issues/1811
# - https://github.com/kennethreitz/requests/pull/1812
Patch1:         python-requests-remove-nested-bundling-dep.patch

# Tell setuptools about what version of urllib3 we're unbundling
# - https://github.com/kennethreitz/requests/issues/2816
Patch2:         python-requests-urllib3-at-%{urllib3_unbundled_version}.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-chardet
BuildRequires:  %{?scl_prefix}python-urllib3 >= %{urllib3_unbundled_version}

Requires:       ca-certificates
Requires:       %{?scl_prefix}python-chardet
Requires:       %{?scl_prefix}python-urllib3 >= %{urllib3_unbundled_version}

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-requests = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-requests = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-requests = %{version}-%{release}
%endif
%endif

#if 0%{?rhel} && 0%{?rhel} <= 6
#BuildRequires:  python-ordereddict
#Requires:       python-ordereddict
#endif

%description
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.

%prep
%setup -q -n requests-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

# Unbundle the certificate bundle from mozilla.
rm -rf requests/cacert.pem

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build

# Unbundle chardet and urllib3.  We replace these with symlinks to system libs.
rm -rf build/lib/requests/packages/chardet
rm -rf build/lib/requests/packages/urllib3
%{?scl:EOF}

%install
rm -rf $RPM_BUILD_ROOT
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
ln -s ../../chardet %{buildroot}/%{python_sitelib}/requests/packages/chardet
ln -s ../../urllib3 %{buildroot}/%{python_sitelib}/requests/packages/urllib3
%{?scl:EOF}

## The tests succeed if run locally, but fail in koji.
## They require an active network connection to query httpbin.org
%check

#%%{__python} test_requests.py
#%%if 0%%{?_with_python3}
#pushd %%{py3dir}
#%%{__python3} test_requests.py
#popd
#%%endif

# At very, very least, we'll try to start python and import requests
%{?scl:scl enable %{scl} - << \EOF}
PYTHONPATH=. %{__python} -c "import requests"
%{?scl:EOF}

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc NOTICE README.rst HISTORY.rst
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/requests
%{python_sitelib}/requests/*

%changelog
* Thu Jul 27 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Ralph Bean <rbean@redhat.com> - 2.10.0-3
- Update python2 packaging.

* Thu Jun 02 2016 Ralph Bean <rbean@redhat.com> - 2.10.0-2
- Fix python2 subpackage to comply with guidelines.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Ralph Bean <rbean@redhat.com> - 2.9.1-1
- new version

* Fri Dec 18 2015 Ralph Bean <rbean@redhat.com> - 2.9.0-1
- new version

* Mon Dec 14 2015 Ralph Bean <rbean@redhat.com> - 2.8.1-1
- Latest upstream.
- Bump hard dep on urllib3 to 1.12.

* Mon Nov 02 2015 Robert Kuska <rkuska@redhat.com> - 2.7.0-8
- Rebuilt for Python3.5 rebuild

* Sat Oct 10 2015 Ralph Bean <rbean@redhat.com> - 2.7.0-7
- Tell setuptools about what version of urllib3 we're unbundling
  for https://github.com/kennethreitz/requests/issues/2816

* Thu Sep 17 2015 Ralph Bean <rbean@redhat.com> - 2.7.0-6
- Replace the provides macro with a plain provides field for now until we can
  re-organize this package into two different subpackages.

* Thu Sep 17 2015 Ralph Bean <rbean@redhat.com> - 2.7.0-5
- Remove 'provides: python2-requests' from the python3 subpackage, obviously.

* Tue Sep 15 2015 Ralph Bean <rbean@redhat.com> - 2.7.0-4
- Employ %%python_provides macro to provide python2-requests.

* Fri Sep 04 2015 Ralph Bean <rbean@redhat.com> - 2.7.0-3
- Lock down the python-urllib3 version to the specific version we unbundled.
  https://bugzilla.redhat.com/show_bug.cgi?id=1253823

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Ralph Bean <rbean@redhat.com> - 2.7.0-1
- new version

* Wed Apr 29 2015 Ralph Bean <rbean@redhat.com> - 2.6.2-1
- new version

* Thu Apr 23 2015 Ralph Bean <rbean@redhat.com> - 2.6.1-1
- new version

* Wed Apr 22 2015 Ralph Bean <rbean@redhat.com> - 2.6.0-1
- new version
- Remove patch for CVE-2015-2296, now included in the upstream release.

* Mon Mar 16 2015 Ralph Bean <rbean@redhat.com> - 2.5.3-2
- Backport fix for CVE-2015-2296.

* Thu Feb 26 2015 Ralph Bean <rbean@redhat.com> - 2.5.3-1
- new version

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 2.5.1-1
- new version

* Tue Dec 16 2014 Ralph Bean <rbean@redhat.com> - 2.5.0-3
- Pin python-urllib3 requirement at 1.10.
- Fix requirement pinning syntax.

* Thu Dec 11 2014 Ralph Bean <rbean@redhat.com> - 2.5.0-2
- Do the most basic of tests in the check section.

* Thu Dec 11 2014 Ralph Bean <rbean@redhat.com> - 2.5.0-1
- Latest upstream, 2.5.0 for #1171068

* Wed Nov 05 2014 Ralph Bean <rbean@redhat.com> - 2.4.3-1
- Latest upstream, 2.4.3 for #1136283

* Wed Nov 05 2014 Ralph Bean <rbean@redhat.com> - 2.3.0-4
- Re-do unbundling by symlinking system libs into the requests/packages/ dir.

* Sun Aug  3 2014 Tom Callaway <spot@fedoraproject.org> - 2.3.0-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Arun S A G <sagarun@gmail.com> - 2.3.0-1
- Latest upstream

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Sep 25 2013 Ralph Bean <rbean@redhat.com> - 2.0.0-1
- Latest upstream.
- Add doc macro to the python3 files section.
- Require python-urllib3 greater than or at 1.7.1.

* Mon Aug 26 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.3-5
- fix versioned dep on python-urllib3

* Mon Aug 26 2013 Ralph Bean <rbean@redhat.com> - 1.2.3-4
- Explicitly versioned the requirements on python-urllib3.

* Thu Aug 22 2013 Ralph Bean <rbean@redhat.com> - 1.2.3-3
- Release bump for a coupled update with python-urllib3.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 Ralph Bean <rbean@redhat.com> - 1.2.3-1
- Latest upstream.
- Fixed bogus date in changelog.

* Tue Jun 11 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-4
- Correct a rhel conditional on python-ordereddict

* Thu Feb 28 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-3
- Unbundled python-urllib3.  Using system python-urllib3 now.
- Conditionally include python-ordereddict for el6.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-2
- Unbundled python-charade/chardet.  Using system python-chardet now.
- Removed deprecated comments and actions against oauthlib unbundling.
  Those are no longer necessary in 1.1.0.
- Added links to bz tickets over Patch declarations.

* Tue Feb 26 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-1
- Latest upstream.
- Relicense to ASL 2.0 with upstream.
- Removed cookie handling patch (fixed in upstream tarball).
- Updated cert unbundling patch to match upstream.
- Added check section, but left it commented out for koji.

* Fri Feb  8 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.14.1-4
- Let brp_python_bytecompile run again, take care of the non-python{2,3} modules
  by removing them from the python{,3}-requests package that they did not belong
  in.
- Use the certificates in the ca-certificates package instead of the bundled one
  + https://bugzilla.redhat.com/show_bug.cgi?id=904614
- Fix a problem with cookie handling
  + https://bugzilla.redhat.com/show_bug.cgi?id=906924

* Mon Oct 22 2012 Arun S A G <sagarun@gmail.com>  0.14.1-1
- Updated to latest upstream release

* Sun Jun 10 2012 Arun S A G <sagarun@gmail.com> 0.13.1-1
- Updated to latest upstream release 0.13.1
- Use system provided ca-certificates
- No more async requests use grrequests https://github.com/kennethreitz/grequests
- Remove gevent as it is no longer required by requests

* Sun Apr 01 2012 Arun S A G <sagarun@gmail.com> 0.11.1-1
- Updated to upstream release 0.11.1

* Thu Mar 29 2012 Arun S A G <sagarun@gmail.com> 0.10.6-3
- Support building package for EL6

* Tue Mar 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.6-2
- +python3-requests pkg

* Sat Mar 3 2012 Arun SAG <sagarun@gmail.com> - 0.10.6-1
- Updated to new upstream version

* Sat Jan 21 2012 Arun SAG <sagarun@gmail.com> - 0.9.3-1
- Updated to new upstream version 0.9.3
- Include python-gevent as a dependency for requests.async
- Clean up shebangs in requests/setup.py,test_requests.py and test_requests_ext.py

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Arun SAG <sagarun@gmail.com> - 0.8.2-1
- New upstream version
- keep alive support
- complete removal of cookiejar and urllib2

* Thu Nov 10 2011 Arun SAG <sagarun@gmail.com> - 0.7.6-1
- Updated to new upstream release 0.7.6

* Thu Oct 20 2011 Arun SAG <sagarun@gmail.com> - 0.6.6-1
- Updated to version 0.6.6

* Fri Aug 26 2011 Arun SAG <sagarun@gmail.com> - 0.6.1-1
- Updated to version 0.6.1

* Sat Aug 20 2011 Arun SAG <sagarun@gmail.com> - 0.6.0-1
- Updated to latest version 0.6.0

* Mon Aug 15 2011 Arun SAG <sagarun@gmail.com> - 0.5.1-2
- Remove OPT_FLAGS from build section since it is a noarch package
- Fix use of mixed tabs and space
- Remove extra space around the word cumbersome in description

* Sun Aug 14 2011 Arun SAG <sagarun@gmail.com> - 0.5.1-1
- Initial package
