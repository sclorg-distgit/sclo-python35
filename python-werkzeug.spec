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

%{?scl:          %scl_package        python-werkzeug}
%{!?scl:         %global pkg_name    %{name}}

%global srcname Werkzeug

Name:           %{?sub_prefix}python-werkzeug
Version:        0.10.4
Release:        4%{?dist}
Summary:        The Swiss Army knife of Python web development 

Group:          Development/Libraries
License:        BSD
URL:            http://werkzeug.pocoo.org/
Source0:        http://pypi.python.org/packages/source/W/Werkzeug/%{srcname}-%{version}.tar.gz
# Pypi version of werkzeug is missing _themes folder needed to build werkzeug sphinx docs
# See https://github.com/mitsuhiko/werkzeug/issues/761
Source1:        werkzeug-sphinx-theme.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  %{?scl_prefix}python-sphinx
Requires:       %{?scl_prefix}python

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-werkzeug = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-werkzeug = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-werkzeug = %{version}-%{release}
%endif
%endif


%description
Werkzeug
========

Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules.  It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

Werkzeug is unicode aware and doesn't enforce a specific template
engine, database adapter or anything else.  It doesn't even enforce
a specific way of handling requests and leaves all that up to the
developer. It's most useful for end user applications which should work
on as many server environments as possible (such as blogs, wikis,
bulletin boards, etc.).


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%if 0%{?scl:1}
Provides: %{?scl_prefix}python-werkzeug-doc = %{version}-%{release}
%if %{?with_python3}
Provides: %{?scl_prefix}python3-werkzeug-doc = %{version}-%{release}
%else
Provides: %{?scl_prefix}python2-werkzeug-doc = %{version}-%{release}
%endif
%endif

%description doc
Documentation and examples for %{name}.

%prep
%setup -q -n %{srcname}-%{version}
%{__sed} -i 's/\r//' LICENSE
%{__sed} -i '1d' tests/multipart/test_collect.py
tar -xf %{SOURCE1}

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
make html
popd
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc
%{?scl:EOF}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE PKG-INFO CHANGES
%{python_sitelib}/*

%files doc
%defattr(-,root,root,-)
%doc docs/_build/html examples

%changelog
* Fri Jul 28 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch>
- SCLo build.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.10.4-3
- Rebuilt for Python3.5 rebuild
- Add werkzeug sphinx theme as a Source1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 30 2015 Ricky Elrod <relrod@redhat.com> - 0.10.4-1
- Upstream 0.10.4.

* Fri Jul 18 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.6-1
- Upstream 0.9.6
- Fixes RHBZ #1105819

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Aug 26 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.4-1
- Upstream 0.9.4

* Thu Jul 25 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.3-1
- Upstream 0.9.3

* Tue Jul 23 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9.2-1
- Upstream 0.9.2 release.

* Sat Jun 15 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.1-1
- upstream 0.9.1
- add python3 flavor

* Fri Jun 14 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-1
- Upstream 0.9.0 release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.3-1
- upstream 0.8.3 (fixes XSS security issues)

* Wed Jan 25 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.2-1
- upstream 0.8.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.2-1
- Updating because upstream release of Werkzeug 0.6.2

* Fri Mar 05 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6-1
- Updating because upstream release of Werkzeug 0.6

* Tue Aug 25 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.5.1-1
- Initial package
