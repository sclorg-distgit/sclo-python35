# centos/sclo spec file for python-urllib3, from:
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

%{?scl:          %scl_package        python-mock}
%{!?scl:         %global pkg_name    %{name}}

%global srcname urllib3

Name:           %{?sub_prefix}python-%{srcname}
Version:        1.15.1
Release:        1%{?dist}
Summary:        Python HTTP library with thread-safe connection pooling and file post

License:        MIT
URL:            http://urllib3.readthedocs.org/
Source0:        https://pypi.io/packages/source/u/%{srcname}/%{srcname}-%{version}.tar.gz

# Only used for python3 (and for python2 on F22 and newer)
Source1:        ssl_match_hostname_py3.py

# Only used for F21.
Patch0:         python-urllib3-pyopenssl.patch

# Remove logging-clear-handlers from setup.cfg because it's not available in RHEL6's nose
Patch100:       python-urllib3-old-nose-compat.patch

BuildArch:      noarch

Requires:       ca-certificates

# Previously bundled things:
Requires:       %{?scl_prefix}python-six

Requires:       %{?scl_prefix}python-pysocks

# See comment-block in the %%install section.
# https://bugzilla.redhat.com/show_bug.cgi?id=1231381
#if 0%{?fedora} && 0%{?fedora} <= 21
Requires:       python-backports-ssl_match_hostname
BuildRequires:  python-backports-ssl_match_hostname
#endif

#if 0%{?rhel} && 0%{?rhel} <= 6
#BuildRequires:  python-ordereddict
#Requires:       python-ordereddict
#endif

BuildRequires:  %{?scl_prefix}python-devel
# For unittests
#BuildRequires:  python-nose
#BuildRequires:  python-mock
#BuildRequires:  python-six
#BuildRequires:  python-pysocks
#BuildRequires:  python-tornado


#if 0%{?fedora} == 21
#BuildRequires:  pyOpenSSL
#BuildRequires:  python-ndg_httpsclient
#BuildRequires:  python-pyasn1
#equires:       pyOpenSSL
#Requires:       python-ndg_httpsclient
#Requires:       python-pyasn1
#endif

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-%{srcname} = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-%{srcname} = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-%{srcname} = %{version}-%{release}
%endif
%endif



%description
Python HTTP module with connection pooling and file POST abilities.


%prep
%setup -q -n %{srcname}-%{version}

# Drop the dummyserver tests in koji.  They fail there in real builds, but not
# in scratch builds (weird).
rm -rf test/with_dummyserver/

#if 0%{?rhel} && 0%{?rhel} <= 6
#patch100 -p1
#endif

%if 0%{?fedora} == 21
%patch0 -p1
%endif

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} - << \EOF}

%{__python} setup.py install --skip-build --root %{buildroot}

rm -rf %{buildroot}/%{python_sitelib}/urllib3/packages/six.py*
rm -rf %{buildroot}/%{python_sitelib}/urllib3/packages/ssl_match_hostname/

mkdir -p %{buildroot}/%{python_sitelib}/urllib3/packages/
ln -s ../../six.py %{buildroot}/%{python_sitelib}/urllib3/packages/six.py
ln -s ../../six.pyc %{buildroot}/%{python_sitelib}/urllib3/packages/six.pyc
ln -s ../../six.pyo %{buildroot}/%{python_sitelib}/urllib3/packages/six.pyo

# In Fedora 22 and later, we ship Python 2.7.9 which carries an ssl module that
# does what we need, so we replace urllib3's bundled ssl_match_hostname module
# with our own that just proxies to the stdlib ssl module (to avoid carrying an
# unnecessary dep on the backports.ssl_match_hostname module).
# In Fedora 21 and earlier, we have an older Python 2.7, and so we require and
# symlink in that backports.ssl_match_hostname module.
#   https://bugzilla.redhat.com/show_bug.cgi?id=1231381

%if %{?with_python3}
cp %{SOURCE1} %{buildroot}/%{python_sitelib}/urllib3/packages/ssl_match_hostname.py
%else
ln -s ../../backports/ssl_match_hostname %{buildroot}/%{python_sitelib}/urllib3/packages/ssl_match_hostname
%endif

# Copy in six.py just for the test suite.
%if 0%{?fedora} >= 22
cp %{python_sitelib}/six.* %{buildroot}/%{python_sitelib}/.
%else
cp %{python_sitelib}/six.* %{buildroot}/%{python_sitelib}/.
cp -r %{python_sitelib}/backports %{buildroot}/%{python_sitelib}/.
%endif

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python_sitelib}/dummyserver

%{?scl:EOF}

%check
#nosetests

# And after its done, remove our copied in bits
rm -rf %{buildroot}/%{python_sitelib}/six*
rm -rf %{buildroot}/%{python_sitelib}/backports*

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc CHANGES.rst README.rst CONTRIBUTORS.txt
# For noarch packages: sitelib
%{python_sitelib}/urllib3/
%{python_sitelib}/urllib3-*.egg-info

%changelog
* Thu Jul 27 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Fri Apr 29 2016 Ralph Bean <rbean@redhat.com> - 1.15.1-1
- Removed patch for ipv6 support, now applied upstream.
- Latest version.
- New dep on pysocks.

* Fri Feb 26 2016 Ralph Bean <rbean@redhat.com> - 1.13.1-3
- Apply patch from upstream to fix ipv6.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Ralph Bean <rbean@redhat.com> - 1.13.1-1
- new version

* Fri Dec 18 2015 Ralph Bean <rbean@redhat.com> - 1.13-1
- new version

* Mon Dec 14 2015 Ralph Bean <rbean@redhat.com> - 1.12-1
- new version

* Thu Oct 15 2015 Robert Kuska <rkuska@redhat.com> - 1.10.4-7
- Rebuilt for Python3.5 rebuild

* Sat Oct 10 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-6
- Sync from PyPI instead of a git checkout.

* Tue Sep 08 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-5.20150503gita91975b
- Drop requirement on python-backports-ssl_match_hostname on F22 and newer.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.4-4.20150503gita91975b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-3.20150503gita91975b
- Apply pyopenssl injection for an outdated cpython as per upstream advice
  https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
  https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl

* Tue May 19 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-2.20150503gita91975b
- Specify symlinks for six.py{c,o}, fixing rhbz #1222142.

* Sun May 03 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-1.20150503gita91975b
- Latest release for python-requests-2.7.0

* Wed Apr 29 2015 Ralph Bean <rbean@redhat.com> - 1.10.3-2.20150429git585983a
- Grab a git snapshot to get around this chunked encoding failure.

* Wed Apr 22 2015 Ralph Bean <rbean@redhat.com> - 1.10.3-1
- new version

* Thu Feb 26 2015 Ralph Bean <rbean@redhat.com> - 1.10.2-1
- new version

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 1.10.1-1
- new version

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 1.10.1-1
- new version

* Mon Jan 05 2015 Ralph Bean <rbean@redhat.com> - 1.10-2
- Copy in a shim for ssl_match_hostname on python3.

* Sun Dec 14 2014 Ralph Bean <rbean@redhat.com> - 1.10-1
- Latest upstream 1.10, for python-requests-2.5.0.
- Re-do unbundling without patch, with symlinks.
- Modernize python2 macros.
- Remove the with_dummyserver tests which fail only sometimes.

* Wed Nov 05 2014 Ralph Bean <rbean@redhat.com> - 1.9.1-1
- Latest upstream, 1.9.1 for latest python-requests.

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 1.8.2-4
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 21 2014 Arun S A G <sagarun@gmail.com> - 1.8.2-1
- Update to latest upstream version

* Mon Oct 28 2013 Ralph Bean <rbean@redhat.com> - 1.7.1-2
- Update patch to find ca_certs in the correct location.

* Wed Sep 25 2013 Ralph Bean <rbean@redhat.com> - 1.7.1-1
- Latest upstream with support for a new timeout class and py3.4.

* Wed Aug 28 2013 Ralph Bean <rbean@redhat.com> - 1.7-3
- Bump release again, just to push an unpaired update.

* Mon Aug 26 2013 Ralph Bean <rbean@redhat.com> - 1.7-2
- Bump release to pair an update with python-requests.

* Thu Aug 22 2013 Ralph Bean <rbean@redhat.com> - 1.7-1
- Update to latest upstream.
- Removed the accept-header proxy patch which is included in upstream now.
- Removed py2.6 compat patch which is included in upstream now.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-6
- Fix Requires of python-ordereddict to only apply to RHEL

* Fri Mar  1 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-5
- Unbundling finished!

* Fri Mar 01 2013 Ralph Bean <rbean@redhat.com> - 1.5-4
- Upstream patch to fix Accept header when behind a proxy.
- Reorganize patch numbers to more clearly distinguish them.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 1.5-3
- Renamed patches to python-urllib3-*
- Fixed ssl check patch to use the correct cert path for Fedora.
- Included dependency on ca-certificates
- Cosmetic indentation changes to the .spec file.

* Tue Feb  5 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-2
- python3-tornado BR and run all unittests on python3

* Mon Feb 04 2013 Toshio Kuratomi <toshio@fedoraproject.org> 1.5-1
- Initial fedora build.
