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

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
pulp_file A Pulp plugin to support hosting arbitrary files.For more
information, please see the documentation < or the Pulp project page <>_.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       (python3dist(pulpcore-plugin) >= 0.1rc2 with python3dist(pulpcore-plugin) < 0.2)
Requires:       python3dist(setuptools)
%description -n python3-%{pypi_name}
pulp_file A Pulp plugin to support hosting arbitrary files.For more
information, please see the documentation < or the Pulp project page <>_.


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
*  - 0.1.0-1
- Initial package.
