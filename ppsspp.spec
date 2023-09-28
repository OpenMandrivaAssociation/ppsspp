%define _disable_ld_no_undefined 1

Summary:	Sony PlayStation Portable (PSP) emulator
Name:		ppsspp
Version:	1.16.5
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

Provides: %{name}-sdl = %{version}-%{release}

%description
PPSSPP is a cross-platform Sony PlayStation Portable (PSP) emulator.

PPSSPP can run your PSP games on your PC in full HD resolution, and play
them on Android too. It can even upscale textures that would otherwise be
too blurry as they were made for the small screen of the original PSP.

%package qt
Summary:        PPSSPP Qt backend
Group:          System/Emulators/Other
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-qt = %{version}-%{release}

%description qt
PPSSPP build using the Qt framework

%prep
%autosetup -p1

# Fix version string
sed s,"unknown_version","%{version}-%{release}",g -i git-version.cmake

%build

export CMAKE_BUILD_DIR=build-headless
%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DHEADLESS=ON \
  -DUSE_FFMPEG=ON \
  -DUSE_SYSTEM_FFMPEG=ON \
  -DUSE_SYSTEM_LIBZIP=ON \
  -DUSE_SYSTEM_SNAPPY=ON
cd ..

export CMAKE_BUILD_DIR=build-qt
%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DUSING_QT_UI=ON \
  -DUSE_FFMPEG=ON \
  -DUSE_SYSTEM_FFMPEG=ON \
  -DUSE_SYSTEM_LIBZIP=ON \
  -DUSE_SYSTEM_SNAPPY=ON
cd ..

export CMAKE_BUILD_DIR=build
%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DUSE_FFMPEG=ON \
  -DUSE_SYSTEM_FFMPEG=ON \
  -DUSE_SYSTEM_LIBZIP=ON \
  -DUSE_SYSTEM_SNAPPY=ON
cd ..

%make_build -C build-headless

%make_build -C build-qt

%make_build -C build

%install
%make_install -C build-headless

%make_install -C build-qt

%make_install -C build
#----------------------------------------------------------------------------

%files
%{_bindir}/PPSSPPSDL
%{_datadir}/applications/PPSSPPSDL.desktop
%{_iconsdir}/hicolor/*x*/apps/ppsspp.png
%{_iconsdir}/hicolor/scalable/apps/ppsspp.svg
%{_datadir}/mime/packages/ppsspp.xml
%{_datadir}/ppsspp/assets/

#----------------------------------------------------------------------------
%files qt
%{_bindir}/PPSSPPQt
%{_datadir}/applications/PPSSPPQt.desktop
