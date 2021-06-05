%global src_name stake-o-matic

Name:       solana-%{src_name}
# git f65c3ce97e90db44f747d6533bea78b06dfa66fe
Version:    11
Release:    1%{?dist}
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
BuildRequires:  openssl-devel

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
* Sat Jun 5 2021 Ivan Mironov <mironov.ivan@gmail.com> - 11-1
- Initial packaging
