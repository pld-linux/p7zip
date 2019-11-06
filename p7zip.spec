Summary:	File archiver with highest compression ratio
Summary(pl.UTF-8):	Paker plików z najwyższym stopniem kompresji
Name:		p7zip
Version:	16.02
Release:	2
License:	LGPL v2.1+
Group:		Applications/Archiving
Source0:	http://downloads.sourceforge.net/p7zip/%{name}_%{version}_src_all.tar.bz2
# Source0-md5:	a0128d661cfe7cc8c121e73519c54fbf
Patch0:		05-hardening-flags.patch
Patch1:		14-Fix-g++-warning.patch
Patch2:		CVE-2016-9296.patch
Patch3:		CVE-2017-17969.patch
Patch4:		gcc10-conversion.patch
URL:		http://p7zip.sourceforge.net/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
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
Standalone version of 7zip. It handles less archive formats than
plugin capable version.

%description standalone -l pl.UTF-8
Samodzielna wersja 7zip-a. Obsługuje mniej formatów archiwów niż
wersja obsługująca wtyczki.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__sed} -i -e 's/ -s / /' makefile.machine

find . -name '*.cpp' -exec %{__sed} -i -e 's@getenv("P7ZIP_HOME_DIR")@"%{_libdir}/%{name}/"@g' {} \;

%build
#%%{__make} all2 test \
%{__make} all2 \
	CC="%{__cc} \$(ALLFLAGS)" \
	CXX="%{__cxx} \$(ALLFLAGS)" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	OPTFLAGS="%{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/{Codecs,Formats},%{_mandir}/man1}

install bin/{7z,7za} $RPM_BUILD_ROOT%{_bindir}
install bin/7z.so $RPM_BUILD_ROOT%{_libdir}/%{name}
install bin/Codecs/* $RPM_BUILD_ROOT%{_libdir}/%{name}/Codecs
install bin/7zCon.sfx $RPM_BUILD_ROOT%{_libdir}/%{name}

install man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
# 7zr is not packaged (subset of 7za functionality)
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/7zr.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc DOC/{MANUAL,{7zFormat,License,Methods,lzma,readme,src-history}.txt} ChangeLog README TODO
# devel: %doc DOC/7zC.txt
%attr(755,root,root) %{_bindir}/7z
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/7zCon.sfx
%attr(755,root,root) %{_libdir}/%{name}/7z.so
%dir %{_libdir}/%{name}/Codecs
%attr(755,root,root) %{_libdir}/%{name}/Codecs/*
%{_mandir}/man1/7z.1*

%files standalone
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/7za
%{_mandir}/man1/7za.1*
