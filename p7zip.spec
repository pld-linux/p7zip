Summary:	File archiver with highest compression ratio
Summary(pl):	Paker plików z najwy¿szym stopniem kompresji
Name:		p7zip
Version:	0.81
Release:	1
License:	LGPL
Group:		Applications/Archiving
Source0:	http://dl.sourceforge.net/p7zip/%{name}_%{version}.tar.bz2
# Source0-md5:	2a4f8e1c2ae8635cc98a0016f3fdb578
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
- Mo¿liwo¶æ u¿ywania dowelnych metod kodowania, kompresji, konwersji,
- Obs³uga bardzo du¿ych plików,
- Obs³uga nazw plików w unikodzie,
- Kompresja upakowana,
- Kompresja nag³ówków archiwum.

%prep
%setup -q -n %{name}_%{version}_a014

%build
%{__make} \
	CC="%{__cc} %{rpmcflags}" \
	CXX="%{__cxx} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install 7z $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc html ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
