%define native_snapshot 21.08.2013
%define lang_snapshot 21.08.2013

Summary:	Sony PlayStation Portable (PSP) emulator
Name:		ppsspp
Version:	0.9
Release:	2
License:	GPLv2+
Group:		Emulators
Url:		http://www.ppsspp.org
# From git by tag https://github.com/hrydgard/ppsspp
Source0:	%{name}-%{version}.tar.gz
# From git https://github.com/hrydgard/native
Source1:	native-%{native_snapshot}.tar.bz2
# From git https://github.com/hrydgard/ppsspp-lang
Source2:	ppsspp-lang-%{lang_snapshot}.tar.bz2
Patch0:		ppsspp-0.8-git-version.patch
Patch1:		ppsspp-0.9-datapath.patch
Patch2:		ppsspp-0.9-ffmpeg.patch
Patch3:		ppsspp-0.9-linkage.patch
Patch4:		ppsspp-0.9-atrac3.patch
Patch5:		ppsspp-0.9-controls.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(sdl)
# Possibly created with reverse engineering
Suggests:	ppsspp-at3plus-plugin

%description
PPSSPP is a cross-platform Sony PlayStation Portable (PSP) emulator.

PPSSPP can run your PSP games on your PC in full HD resolution, and play
them on Android too. It can even upscale textures that would otherwise be
too blurry as they were made for the small screen of the original PSP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
sed s,"unknown_version","%{version}",g -i git-version.cmake

# Unpack external libraries from Native sub-project
rm -rf native lang
tar -xf %{SOURCE1}
mv native-%{native_snapshot} native
tar -xf %{SOURCE2}
mv ppsspp-lang-%{lang_snapshot} lang

%build
# segfaults with default -O2 optimization
%global optflags %{optflags} -O0
%cmake \
	-DHEADLESS:BOOL=OFF \
	-DUSE_FFMPEG:BOOL=ON
%make

%install
mkdir -p %{buildroot}%{_gamesbindir}
install -m 0755 build/PPSSPPSDL %{buildroot}%{_gamesbindir}/%{name}-sdl
mkdir -p %{buildroot}%{_gamesdatadir}/%{name}
cp -r build/assets %{buildroot}%{_gamesdatadir}/%{name}
cp -r lang %{buildroot}%{_gamesdatadir}/%{name}/assets/

# install menu entry
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=PPSSPP
Comment=Sony PSP emulator
Exec=%{_gamesbindir}/%{name}-sdl
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF

# install menu icons
for N in 16 32 48 64 128;
do
convert assets/icon-114.png -scale ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

%files
%{_gamesbindir}/%{name}-sdl
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_gamesdatadir}/%{name}
