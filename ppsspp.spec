%define native_snapshot 02.02.2015
%define lang_snapshot 02.02.2015
%define armips_snapshot 20.01.2015

%define _disable_ld_no_undefined 1

Summary:	Sony PlayStation Portable (PSP) emulator
Name:		ppsspp
Version:	1.14.1
Release:	1
License:	GPLv2+
Group:		Emulators
Url:		http://www.ppsspp.org
Source0:	https://github.com/hrydgard/ppsspp/releases/download/v%{version}/ppsspp-%{version}.tar.xz
BuildRequires:	cmake
BuildRequires:  qmake5
BuildRequires:	imagemagick
BuildRequires:	ffmpeg4-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:  pkgconfig(glew)
#Requires system libpng17, otherwise uses internal static build
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SPIRV-Tools)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libzip)
BuildRequires:  pkgconfig(snappy)
BuildRequires:  pkgconfig(RapidJSON)

BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5OpenGL)

%description
PPSSPP is a cross-platform Sony PlayStation Portable (PSP) emulator.

PPSSPP can run your PSP games on your PC in full HD resolution, and play
them on Android too. It can even upscale textures that would otherwise be
too blurry as they were made for the small screen of the original PSP.

%files
#{_bindir}/PPSSPPSDL
#{_datadir}/applications/PPSSPPSDL.desktop
%{_datadir}/applications/ppsspp.desktop
%{_iconsdir}/hicolor/*x*/apps/ppsspp.png
%{_iconsdir}/hicolor/scalable/apps/ppsspp.svg
%{_datadir}/mime/packages/ppsspp.xml
%{_datadir}/ppsspp/assets/

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# Fix version string
sed s,"unknown_version","%{version}-%{release}",g -i git-version.cmake

%build
mkdir build-headless build-qt build

cd build-headless
%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DHEADLESS=ON \
  -DUSE_FFMPEG=ON \
  -DUSE_SYSTEM_FFMPEG=ON \
  -DUSE_SYSTEM_LIBZIP=ON \
  -DUSE_SYSTEM_SNAPPY=ON
%make_build
cd ../build-qt
%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DUSING_QT_UI=ON \
  -DUSE_FFMPEG=ON \
  -DUSE_SYSTEM_FFMPEG=ON \
  -DUSE_SYSTEM_LIBZIP=ON \
  -DUSE_SYSTEM_SNAPPY=ON
%make_build
cd ../build
%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DUSE_FFMPEG=ON \
  -DUSE_SYSTEM_FFMPEG=ON \
  -DUSE_SYSTEM_LIBZIP=ON \
  -DUSE_SYSTEM_SNAPPY=ON
%make_build

%install
%make_install -C build
#mkdir -p %{buildroot}%{_gamesbindir}
#install -m 0755 build/PPSSPPSDL %{buildroot}%{_gamesbindir}/%{name}-sdl
#mkdir -p %{buildroot}%{_gamesdatadir}/%{name}
#cp -r build/assets %{buildroot}%{_gamesdatadir}/%{name}
#cp -r lang %{buildroot}%{_gamesdatadir}/%{name}/assets/

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
#for N in 16 32 48 64 128;
#do
#convert assets/icon-114.png -scale ${N}x${N} $N.png;
#install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
#done

