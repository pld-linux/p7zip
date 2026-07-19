Summary:	File archiver with highest compression ratio
Summary(pl.UTF-8):	Paker plików z najwyższym stopniem kompresji
Name:		p7zip
Version:	26.02
Release:	1
License:	LGPL v2.1+ with unRAR restriction (RAR decoder), BSD (Lzfse, Zstd, Xxh64)
Group:		Applications/Archiving
#Source0Download: https://github.com/ip7z/7zip/releases
Source0:	https://github.com/ip7z/7zip/archive/%{version}/7zip-%{version}.tar.gz
# Source0-md5:	29f692dc18d150acbbd31a86e3ffe610
# upstream ships no manual pages; these are from Debian's 7zip packaging (LGPL v2.1+)
Source1:	7z.1
Source2:	7zz.1
Patch0:		%{name}-sfx-module-dir.patch
URL:		https://7-zip.org/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
7-Zip is a file archiver with highest compression ratio.

The main features of 7z format:
- Open architecture
- High compression ratio
- Strong AES-256 encryption
- Ability of using any compression, conversion or encryption method
- Supporting files with sizes up to 16000000000 GB
- Unicode file names
- Solid compressing
- Archive headers compressing

%description -l pl.UTF-8
7-Zip jest pakerem plików z najwyższym stopniem kompresji.

Główne cechy formatu 7z:
- otwarta architektura,
- wysoki stopień kompresji,
- silne kodowanie AES-256,
- możliwość używania dowolnych metod kodowania, kompresji, konwersji,
- obsługa bardzo dużych plików (powyżej 16000000000 GB),
- obsługa nazw plików w unikodzie,
- kompresja upakowana,
- kompresja nagłówków archiwum.

%package standalone
Summary:	Standalone 7zip executable
Summary(pl.UTF-8):	Samodzielny plik wykonywalny 7zip
Group:		Applications/Archiving
Obsoletes:	p7zip-stand-alone

%description standalone
Standalone version of 7zip. It handles less archive formats than the
full version.

%description standalone -l pl.UTF-8
Samodzielna wersja 7zip-a. Obsługuje mniej formatów archiwów niż wersja
pełna.

%prep
%setup -q -n 7zip-%{version}
%patch -P0 -p1

%build
# LOCAL_FLAGS is not a usable hook - every bundle sets it to its own defines
# (-DZ7_SFX etc.); CFLAGS_BASE2/CXXFLAGS_BASE2 are unused by upstream.
# LFLAGS_STRIP= keeps upstream's -s away from the link so debuginfo survives.
%define		buildflags	CFLAGS_BASE2="%{rpmcppflags} %{rpmcflags}" CXXFLAGS_BASE2="%{rpmcppflags} %{rpmcxxflags} -DZ7_SFX_MODULE_DIR='\\"%{_libdir}/%{name}/\\"'" LDFLAGS_STATIC_3="%{rpmldflags}" LFLAGS_STRIP= -f makefile.gcc

%{__make} -C CPP/7zip/Bundles/Alone2 %{buildflags}
%{__make} -C CPP/7zip/Bundles/Alone %{buildflags}
%{__make} -C CPP/7zip/Bundles/SFXCon %{buildflags}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man1}

install -p CPP/7zip/Bundles/Alone2/_o/7zz $RPM_BUILD_ROOT%{_bindir}/7zz
install -p CPP/7zip/Bundles/Alone/_o/7za $RPM_BUILD_ROOT%{_bindir}/7za
ln -sf 7zz $RPM_BUILD_ROOT%{_bindir}/7z
install -p CPP/7zip/Bundles/SFXCon/_o/7zCon $RPM_BUILD_ROOT%{_libdir}/%{name}/7zCon.sfx

cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1
# Debian ships 7za.1 as a ".so man1/7z.1" redirect, which dangles when
# -standalone is installed without the main package
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/7za.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc DOC/{7zFormat,License,Methods,lzma,readme,src-history,unRarLicense}.txt
%attr(755,root,root) %{_bindir}/7z
%attr(755,root,root) %{_bindir}/7zz
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/7zCon.sfx
%{_mandir}/man1/7z.1*
%{_mandir}/man1/7zz.1*

%files standalone
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/7za
%{_mandir}/man1/7za.1*
