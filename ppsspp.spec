%define native_snapshot 02.02.2015
%define lang_snapshot 02.02.2015
%define armips_snapshot 20.01.2015

Summary:	Sony PlayStation Portable (PSP) emulator
Name:		ppsspp
Version:	1.13.2
Release:	1
License:	GPLv2+
Group:		Emulators
Url:		http://www.ppsspp.org
Source0:	https://github.com/hrydgard/ppsspp/releases/download/v%{version}/ppsspp-%{version}.tar.xz
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	ffmpeg4-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:  pkgconfig(glew)
#Requires system libpng17, otherwise uses internal static build
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(snappy)
BuildRequires:  pkgconfig(RapidJSON)

%description
PPSSPP is a cross-platform Sony PlayStation Portable (PSP) emulator.

PPSSPP can run your PSP games on your PC in full HD resolution, and play
them on Android too. It can even upscale textures that would otherwise be
too blurry as they were made for the small screen of the original PSP.

%files
%{_gamesbindir}/%{name}-sdl
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_gamesdatadir}/%{name}

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# Fix version string
sed s,"unknown_version","%{version}-%{release}",g -i git-version.cmake

%build

%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DHEADLESS=OFF \
  -DUSE_FFMPEG=ON \
  -DUSE_SYSTEM_FFMPEG=ON \
  -DUSE_SYSTEM_LIBZIP=ON \
  -DUSE_SYSTEM_SNAPPY=ON
%make_build

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

