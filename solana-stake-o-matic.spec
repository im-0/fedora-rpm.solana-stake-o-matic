%global src_name stake-o-matic

Name:       solana-%{src_name}
# git 94aa5c3d10a1037acabafe55ce2796cd0f766dd2
Version:    12
Release:    2%{?dist}
Summary:    Utility and daemon for Solana Foundation Delegation Program

License:    Apache-2.0
URL:        https://github.com/solana-labs/stake-o-matic/
Source0:    https://github.com/solana-labs/stake-o-matic/archive/v%{version}/%{src_name}-%{version}.tar.gz

# $ cargo vendor
# Contains solana-$VERSION/vendor/*.
Source1:    %{src_name}-%{version}.cargo-vendor.tar.xz
Source2:    config.toml

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  openssl1.1-devel

# libudev-devel
BuildRequires:  systemd-devel


%description
Utility and daemon for Solana Foundation Delegation Program.


%package cli
Summary: Solana Stake-o-Matic RPC CLI


%description cli
Solana Stake-o-Matic RPC CLI.


%package daemon
Summary: Solana Stake-o-Matic daemon


%description daemon
Solana Stake-o-Matic daemon.


%prep
%autosetup -p1 -b0 -n %{src_name}-%{version}
%autosetup -p1 -b1 -n %{src_name}-%{version}

mkdir .cargo
cp %{SOURCE2} .cargo/


%build
%{__cargo} build %{?_smp_mflags} -Z avoid-dev-deps --frozen --release


%install
mkdir -p %{buildroot}/%{_bindir}

find target/release -mindepth 1 -maxdepth 1 -type d -exec rm -r "{}" \;
rm target/release/*.d
rm target/release/*.rlib
# Excluded.
# TODO: Why? What is this?
rm target/release/libsolana_foundation_delegation_program_registry.so

mv target/release/* \
        %{buildroot}/%{_bindir}/


%files cli
%{_bindir}/solana-foundation-delegation-program


%files daemon
%{_bindir}/solana-stake-o-matic


%changelog
* Tue May 10 2022 Ivan Mironov <mironov.ivan@gmail.com> - 12-2
- Fix build on Fedora 36

* Sun Sep 19 2021 Ivan Mironov <mironov.ivan@gmail.com> - 12-1
- Update to v12

* Sat Jun 5 2021 Ivan Mironov <mironov.ivan@gmail.com> - 11-1
- Initial packaging
