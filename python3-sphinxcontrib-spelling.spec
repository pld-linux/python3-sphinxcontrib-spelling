#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Sphinx spell checking extension
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do sprawdzania pisowni
Name:		python3-sphinxcontrib-spelling
Version:	5.0.0
Release:	5
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-spelling/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-spelling/sphinxcontrib-spelling-%{version}.tar.gz
# Source0-md5:	48a3197bd3bf3c4ebc407433263b5cd5
URL:		https://pypi.org/project/sphinxcontrib-spelling/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-pbr
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 2.0.0
BuildRequires:	python3-fixtures >= 3.0.0
BuildRequires:	python3-pyenchant >= 1.6.5
BuildRequires:	python3-pytest
BuildRequires:	python3-six
BuildRequires:	python3-subunit >= 0.0.18
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 1.4.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc} || %{with tests}
# en_US dict for enchant
BuildRequires:	aspell-en
BuildRequires:	enchant-aspell
%endif
%if %{with doc}
BuildRequires:	python3-pyenchant
BuildRequires:	sphinx-pdg >= 2.0.0
%endif
Requires:	python3-modules >= 1:3.5
Requires:	python3-sphinxcontrib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains sphinxcontrib.spelling, a spelling checker for
Sphinx-based documentation. It uses PyEnchant to produce a report
showing misspelled words.

%description -l pl.UTF-8
Ten pakiet zawiera sphinxcontrib.spelling - rozszerzenie do
sprawdzania pisowni w dokumentacji opartej na Sphinksie. Wykorzystuje
PyEnchant do tworzenia raportu wskazującego błędnie napisane słowa.

%package apidocs
Summary:	API documentation for Python sphinxcontrib-spelling module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinxcontrib-spelling
Group:		Documentation

%description apidocs
API documentation for Python sphinxcontrib-spelling module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinxcontrib-spelling.

%prep
%setup -q -n sphinxcontrib-spelling-%{version}

%build
%py3_build %{?with_tests:test}

%if %{with doc}
# enable spell checking to additionally verify particular
# python+sphinx+sphinxcontrib.spelling combo
ENABLE_SPELLING=1 \
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README
%{py3_sitescriptdir}/sphinxcontrib/spelling
%{py3_sitescriptdir}/sphinxcontrib_spelling-%{version}-py*.egg-info
%{py3_sitescriptdir}/sphinxcontrib_spelling-%{version}-py*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
