Summary:	File archiver with highest compression ratio
Summary(pl):	Paker plików z najwy¿szym stopniem kompresji
Name:		p7zip
Version:	0.91
Release:	2
License:	LGPL
Group:		Applications/Archiving
Source0:	http://dl.sourceforge.net/p7zip/%{name}_%{version}.tar.bz2
# Source0-md5:	8c6a7b49f360917cbdd8391f3a926a19
Patch0:		%{name}-opt.patch
URL:		http://sourceforge.net/projects/p7zip
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

%description -l pl
7-Zip jest pakerem plików z najwy¿szym stopniem kompresji.

G³ówne cechy formatu 7z:
- Otwarta architektura,
- Wysoki stopieñ kompresji,
- Silne kodowanie AES-256,
- Mo¿liwo¶æ u¿ywania dowolnych metod kodowania, kompresji, konwersji,
- Obs³uga bardzo du¿ych plików,
- Obs³uga nazw plików w unikodzie,
- Kompresja upakowana,
- Kompresja nag³ówków archiwum.

%package stand-alone
Summary:	Stand-alone 7zip executable
Summary(pl):	Samodzielny plik wykonywalny 7zip
Group:		Applications/Archiving

%description stand-alone
Stand-alone version of 7zip. It handles less archive formats than
plugin capable version.

%description stand-alone -l pl
Samodzielna wersja 7zip-a. Obs³uguje mniej formatów archiw ni¿
wersja obs³uguj±ca wtyczki.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1

cd 7zip/UI/Common
sed -e "s@Formats@%{_libdir}/%{name}/&@" ArchiverInfo.cpp > tmp
mv -f tmp ArchiverInfo.cpp
cd ../../Archive/Common
sed -e "s@return GetBaseFolderPrefix() + TEXT(\"Codecs\\\\\\\\\");@return TEXT(\"%{_libdir}/%{name}/Codecs/\");@" CodecsPath.cpp > tmp
mv -f tmp CodecsPath.cpp

%build
%{__make} \
	CC_="%{__cc}" \
	CXX_="%{__cxx}" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/{Codecs,Formats}}

install bin/7z{,a} $RPM_BUILD_ROOT%{_bindir}
install bin/Codecs/* $RPM_BUILD_ROOT%{_libdir}/%{name}/Codecs
install bin/Formats/* $RPM_BUILD_ROOT%{_libdir}/%{name}/Formats

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc html ChangeLog README TODO
%attr(755,root,root) %{_bindir}/7z
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/Codecs
%attr(755,root,root) %{_libdir}/%{name}/Codecs/*
%dir %{_libdir}/%{name}/Formats
%attr(755,root,root) %{_libdir}/%{name}/Formats/*

%files stand-alone
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/7za
