%define artifact_name mt-wwe
%define current_directory %(echo $PWD)
%define unmangled_version %(hero describe rpm version)
%define release %(hero describe rpm release)
%define python_version %(python --version 2>&1 | cut -d. -f1,2 | sed 's/ //' | tr A-Z a-z)
%define install_prefix /opt/lrms
%define site_pkg %{install_prefix}/lib/%{python_version}/site-packages
%define summary wwe - Word/Word Perfect Extractor & Conversion tool

Summary: %{summary}
Name: %{artifact_name}
Version: %{unmangled_version}
Release: %{release}
Source0: %{artifact_name}-%{unmangled_version}
License: Commercial
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Requires: mt-models, lrms-bash-profile, lrms-joplin, lrms-requests
Provides: %{artifact_name}
Vendor: Propylon
AutoReqProv: no

%description
%{summary}

%prep
rm -rf %{SOURCE0}
rsync -ra --exclude='SOURCES/' --exclude='.env*/' %{current_directory}/ %{SOURCE0}/

%build
cd %{SOURCE0}
%{python_version} setup.py build
cd docs
rm -rf _build
rm -rf build
make clean && make man
cd ..

%install
cd %{SOURCE0}
%{python_version} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES --prefix=%{install_prefix}

mkdir -p %{buildroot}%{_mandir}/man1/
cp %{SOURCE0}/docs/build/man/wwe.1* %{buildroot}%{_mandir}/man1/

for f in $(ls %{buildroot}%{install_prefix}/bin/ || :)
do
  sed -i 's|#!.*|#!/usr/bin/env python|' "%{buildroot}%{install_prefix}/bin/$f"
done

%clean
rm -rf %{_sourcedir}/*
rm -rf %{_builddir}/*
rm -rf %{buildroot}/*
rm -rf %{_srcrpmdir}/*

%files -f %{SOURCE0}/INSTALLED_FILES
%{_mandir}/man1/wwe.1*
%{site_pkg}/wwe*.egg-info
%defattr(-,root,root)

%changelog
%(hero describe rpm changelog)
