%define debug_package %{nil}
%define major %(echo %{version}|cut -d. -f1)

%define libname %mklibname imgui
%define devname %mklibname -d imgui

Name:           imgui
Version:        1.92.5
Release:        1
Summary:        Immediate Mode Graphical User interface for C++ with minimal dependencies
License:        MIT
Group:          System/Libraries
URL:            https://www.dearimgui.org
Source:         https://github.com/ocornut/imgui/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  make
BuildRequires:	vulkan-headers

%description
ImGui is a bloat-free graphical user interface library for C++. It outputs
optimized vertex buffers that you can render anytime in your 3D-pipeline
enabled application. It is fast, portable, renderer agnostic and
self-contained (no external dependencies).

ImGui is designed to enable fast iteration and empower programmers to create
content creation tools and visualization/ debug tools (as opposed to UI for the
average end-user). It favors simplicity and productivity toward this goal, and
thus lacks certain features normally found in more high-level libraries.

ImGui is particularly suited to integration in realtime 3D applications,
fullscreen applications, embedded applications, games, or any applications on
consoles platforms where operating system features are non-standard.

%package -n %{libname}
Summary:	Graphical user interface library for C++
Group:		System/Libraries

%description -n %{libname}
ImGui is a bloat-free graphical user interface library for C++. It outputs
optimized vertex buffers that you can render anytime in your 3D-pipeline
enabled application. It is fast, portable, renderer agnostic and
self-contained (no external dependencies).

ImGui is designed to enable fast iteration and empower programmers to create
content creation tools and visualization/ debug tools (as opposed to UI for the
average end-user). It favors simplicity and productivity toward this goal, and
thus lacks certain features normally found in more high-level libraries.

ImGui is particularly suited to integration in realtime 3D applications,
fullscreen applications, embedded applications, games, or any applications on
consoles platforms where operating system features are non-standard.

%package -n %{devname}
Summary:        Development files for ImGui
Group:          Development/Libraries/C and C++
Requires:	%{libname} = %{EVRD}
%rename imgui-devel

%description -n %{devname}
ImGui is self-contained within a few files that you can easily copy and compile
into your application/engine.

No specific build process is required. You can add the .cpp files to your
project or #include them from an existing file.

%prep
%autosetup -p1

%build
%{__cxx} -o libimgui.so.%{version} -shared -Wl,-soname,libimgui.so.%{major} %{optflags} -I. -fPIC $(ls *.cpp |grep -v imgui_demo.cpp) backends/imgui_impl_vulkan.cpp

%install
mkdir -p %{buildroot}%{_includedir}/imgui
cp *.h %{buildroot}%{_includedir}/imgui

mkdir -p %{buildroot}%{_libdir}
cp libimgui.so.%{version} %{buildroot}%{_libdir}
ln -s libimgui.so.%{version} %{buildroot}%{_libdir}/libimgui.so.%{major}
ln -s libimgui.so.%{version} %{buildroot}%{_libdir}/libimgui.so

mkdir -p %{buildroot}%{_libdir}/cmake/imgui
cat >%{buildroot}%{_libdir}/cmake/imgui/imguiConfig.cmake <<EOF
set(IMGUI_INCLUDE_DIR "%{_includedir}/imgui")
EOF

%files -n %{libname}
%{_libdir}/libimgui.so.*

%files -n %{devname}
%{_includedir}/imgui
%{_libdir}/cmake/imgui
%{_libdir}/libimgui.so
