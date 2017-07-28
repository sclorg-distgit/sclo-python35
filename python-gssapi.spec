# centos/sclo spec file for python-gssapi, from:
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

%{?scl:          %scl_package        python-gssapi}
%{!?scl:         %global pkg_name    %{name}}

%{?scl:
%filter_from_provides s|chan_bindings.so.*||g;s|creds.so.*||g;s|cython_converters.so.*||g;s|exceptions.so.*||g;s|ext_.*so.*||g;s|mech_krb5.so.*||g;s|message.so.*||g;s|misc.so.*||g;s|names.so.*||g;s|oids.so.*||g;s|sec_contexts.so.*||g;s|types.so.*||g;
%filter_from_requires s|libpython.*so.*||g;s|python.*abi.*$||g;
%filter_setup
}

# NOTE: tests are disabled since should_be has not yet been packaged.
# To re-enable, uncomment the 'check' section and lines marked 'for tests'
%global run_tests 0

Name:           %{?sub_prefix}python-gssapi
Version:        1.2.0
Release:        5%{?dist}
Summary:        Python Bindings for GSSAPI (RFC 2743/2744 and extensions)

License:        ISC
URL:            https://github.com/pythongssapi/python-gssapi
Source0:        https://github.com/pythongssapi/%{name}/releases/download/v%{version}/%{pkg_name}-%{version}.tar.gz

# Patches
Patch0: Prevent-GSSError-_display_status-infinite-recursion.patch

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  krb5-devel >= 1.10
BuildRequires:  krb5-libs >= 1.10
BuildRequires:  %{?scl_prefix}Cython >= 0.21
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  %{?scl_prefix}python-tox
Requires:       krb5-libs >= 1.10
Requires:       %{?scl_prefix}python-six
%if !0%{?with_python3}
Requires:       %{?scl_prefix}python-enum34
%endif
Requires:       %{?scl_prefix}python-decorator

# For autosetup
BuildRequires: git

%if 0%{?run_tests}
BuildRequires:  %{?scl_prefix}python-nose
BuildRequires:  %{?scl_prefix}python-nose-parameterized
BuildRequires:  %{?scl_prefix}python-shouldbe
BuildRequires:  krb5-server >= 1.10
%endif

Requires:    %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-gssapi = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-gssapi = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-gssapi = %{version}-%{release}
%endif
%endif

%description
A set of Python bindings to the GSSAPI C library providing both
a high-level pythonic interfaces and a low-level interfaces
which more closely matches RFC 2743.  Includes support for
RFC 2743, as well as multiple extensions.

%prep
%define __git git
%autosetup -S git -n %{pkg_name}-%{version}

%build
%{?scl:scl enable %{scl} - << \EOF}
CFLAGS="%{optflags}" %{__python} setup.py build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install --skip-build --root %{buildroot}

# fix permissions on shared objects (mock seems to set them
# to 0775, whereas a normal build gives 0755)
find %{buildroot}%{python_sitearch}/gssapi -name '*.so' \
    -exec chmod 0755 {} \;
%{?scl:EOF}

%check
%if 0%{?run_tests}
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py nosetests
%{?scl:EOF}

%endif


%files
%{!?_licensedir:%global license %%doc}
%doc README.txt
%license LICENSE.txt
%{python_sitearch}/*

%changelog
* Fri Jul 28 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Tue Apr 04 2017 Robbie Harwood <rharwood@redhat.com> 1.2.0-5
- Fix problem where gss_display_status can infinite loop
- Move to autosetup and rpm-git-tree

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 03 2016 Robbie Harwood <rharwood@redhat.com> - 1.2.0-1
- New upstream version 1.2.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Robbie Harwood <rharwood@redhat.com> - 1.1.4-1
- New upstream version 1.1.4
- Resolves #1286458

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.1.3-2
- Rebuilt for Python3.5 rebuild

* Fri Sep 04 2015 Robbie Harwood <rharwood@redhat.com> - 1.1.3-1
- New upstream minor release

* Thu Aug 20 2015 Simo Sorce <simo@redhat.com> - 1.1.2-1
- New minor release.
- Resolves #1254458
- Fixes a crash bug when inquiring incomplete security contexts

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Simo Sorce <simo@redhat.com> - 1.1.1-1
- New minor release.

* Thu Feb 19 2015 Solly Ross <sross@redhat.com> - 1.1.0-1
- Initial Packaging
