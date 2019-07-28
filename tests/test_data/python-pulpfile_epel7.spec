# Created by pyp2rpm-3.3.2
%global pypi_name pulpfile

Name:           python-%{pypi_name}
Version:        0.1.0
Release:        1%{?dist}
Summary:        File plugin for the Pulp Project

License:        GPLv2+
URL:            http://www.pulpproject.org/
Source0:        %{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
pulp_file A Pulp plugin to support hosting arbitrary files.For more
information, please see the documentation < or the Pulp project page <>_.

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        File plugin for the Pulp Project

Requires:       python%{python3_pkgversion}-pulpcore-plugin >= 0.1rc2
Conflicts:      python%{python3_pkgversion}-pulpcore-plugin >= 0.2
Requires:       python%{python3_pkgversion}-setuptools
%description -n python%{python3_pkgversion}-%{pypi_name}
pulp_file A Pulp plugin to support hosting arbitrary files.For more
information, please see the documentation < or the Pulp project page <>_.


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
*  - 0.1.0-1
- Initial package.
