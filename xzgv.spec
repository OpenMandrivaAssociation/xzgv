Summary:	A GTK+/Imlib-based picture viewer for X
Name:		xzgv
Version: 0.8
Release: %mkrel 2
License:	GPL
Group:		Graphics

Source0:	%{name}-%{version}.tar.bz2

URL:		http://xzgv.browser.org/#download
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
#ExclusiveArch:	%ix86
BuildRequires:	jpeg-devel tiff-devel imlib-devel gtk-devel gdkimlib-devel

%description
xzgv is a picture viewer for X, with a thumbnail-based file selector. 
It uses GTK+ and Imlib. Most file formats are supported, and the thumbnails 
used are compatible with xv, zgv, and the Gimp. 

xzgv differs from other picture viewers for X in that it uses one window 
for both the file selector and viewer, it (unlike xv) allows both scrolling 
and fit-to-window methods of viewing large pictures, and it (unlike xv and
some others) doesn't ever mangle the picture's aspect ratio without you telling
it to. It also provides extensive keyboard support; if you prefer using the 
keyboard, this is almost certainly the best viewer for you. But it doesn't 
skimp on the mousey stuff, either - you can click on a picture to view it, 
drag the picture around to scroll (or use the scrollbars), it has menus, all 
that. So anyway, it's just terribly great. :-) 

%prep
%setup -q

%build
#(peroyvind) does amd64 and ia64 support mmx?
%ifarch %ix86 amd64 ia64
%make CFLAGS="$RPM_OPT_FLAGS -DINTERP_MMX -DBACKEND_IMLIB1 `gtk-config --cflags`"
%else
%make CFLAGS="$RPM_OPT_FLAGS -DBACKEND_IMLIB1 `gtk-config --cflags`"
%endif

%install
make prefix=%buildroot/%_prefix \
     BINDIR=%buildroot/%_bindir \
     MANDIR=%buildroot/%_mandir/man1 \
     INFODIR=%buildroot/%_infodir install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%name.desktop
[Desktop Entry]
Type=Application
Exec=xzgv
Name=Xzgv
Comment=Image viewer
Icon=graphics_section
Categories=Graphics;Viewer;
EOF
 
chmod 0644 README COPYING TODO ChangeLog
 
%post
%if %mdkversion < 200900
%update_menus
%endif
%_install_info %name.info
 
%postun
%if %mdkversion < 200900
%clean_menus
%endif
%_remove_install_info %name.info

%clean
rm -fr %buildroot

%files
%defattr (-,root,root)
%doc README COPYING TODO ChangeLog
%_bindir/*
%{_datadir}/applications/mandriva-*.desktop
%_mandir/man1/*
%_infodir/*.bz2
# Laurent 0.7-3 don"t add dir conflict with info-install
#%_infodir/dir

