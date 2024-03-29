%global commit          c786ac0d7010598f596d948e2e844448b8185b73
%global checkout_date   20230922
%global short_commit    %(c=%{commit}; echo ${c:0:7})
%global snapshot        %{checkout_date}git%{short_commit}

%global src_name stake-o-matic

Name:       solana-%{src_name}
Epoch:      1
# git 94aa5c3d10a1037acabafe55ce2796cd0f766dd2
Version:    0
Release:    1.%{snapshot}%{?dist}
Summary:    Utility and daemon for Solana Foundation Delegation Program

License:    Apache-2.0
URL:        https://github.com/solana-labs/stake-o-matic/
Source0:    https://github.com/solana-labs/stake-o-matic/archive/%{commit}/%{src_name}-%{snapshot}.tar.gz

# $ cargo vendor
# Contains solana-$VERSION/vendor/*.
Source1:    %{src_name}-%{snapshot}.cargo-vendor.tar.xz
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
%autosetup -b1 -n %{src_name}-%{commit}

mkdir .cargo
cp %{SOURCE2} .cargo/

# Fix Fedora's shebang mangling errors:
#     *** ERROR: ./usr/src/debug/solana-testnet-1.10.0-1.fc35.x86_64/vendor/ascii/src/ascii_char.rs has shebang which doesn't start with '/' ([cfg_attr(rustfmt, rustfmt_skip)])
find . -type f -name "*.rs" -exec chmod 0644 "{}" ";"


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
* Fri Sep 22 2023 Ivan Mironov <mironov.ivan@gmail.com> - 1:0-1.20230922gitc786ac0
- Bump version to current git

* Sun Sep 11 2022 Ivan Mironov <mironov.ivan@gmail.com> - 1:0-1.20220911git534f159
- Build from git snapshot

* Tue May 10 2022 Ivan Mironov <mironov.ivan@gmail.com> - 12-2
- Fix build on Fedora 36

* Sun Sep 19 2021 Ivan Mironov <mironov.ivan@gmail.com> - 12-1
- Update to v12

* Sat Jun 5 2021 Ivan Mironov <mironov.ivan@gmail.com> - 11-1
- Initial packaging
