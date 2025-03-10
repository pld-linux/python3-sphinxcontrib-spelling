#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (requires package already installed and en_US dictionary available via pyenchant)

Summary:	Sphinx spell checking extension
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do sprawdzania pisowni
Name:		python3-sphinxcontrib-spelling
Version:	8.0.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-spelling/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-spelling/sphinxcontrib-spelling-%{version}.tar.gz
# Source0-md5:	f1ff5b879a09b95297bbb55fd9c93c78
URL:		https://pypi.org/project/sphinxcontrib-spelling/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:61
BuildRequires:	python3-setuptools_scm >= 6.2
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-Sphinx >= 3.0.0
BuildRequires:	python3-fixtures >= 3.0.0
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-importlib_metadata >= 1.7.0
%endif
BuildRequires:	python3-pyenchant >= 3.1.1
BuildRequires:	python3-pytest
BuildRequires:	python3-sphinxcontrib-spelling
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc} || %{with tests}
# en_US dict for enchant
BuildRequires:	aspell-en
%if 0%(rpm -q enchant2 >/dev/null 2>&1 ; echo $?)
BuildRequires:	enchant-aspell
%else
BuildRequires:	enchant2-aspell
%endif
%endif
%if %{with doc}
BuildRequires:	python3-pyenchant >= 3.1.1
BuildRequires:	python3-sphinxcontrib-spelling
BuildRequires:	sphinx-pdg >= 3.0.0
%endif
Requires:	python3-modules >= 1:3.7
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

cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

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
%doc AUTHORS LICENSE README
%{py3_sitescriptdir}/sphinxcontrib/spelling
%{py3_sitescriptdir}/sphinxcontrib_spelling-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
