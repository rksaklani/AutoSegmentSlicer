# Build and Package AutoSegmentSlicer

This document summarizes how to build and package AutoSegmentSlicer on Windows.

**First-time build?** See **[SUPERBUILD_FIRST_TIME.md](SUPERBUILD_FIRST_TIME.md)** for the full SuperBuild workflow (install Qt/CMake/VS, configure, then build). You can also use the script: `scripts\SuperBuild.ps1`.

AutoSegmentSlicer is a custom Slicer application. Reading the [3D Slicer Developer Documentation](https://slicer.readthedocs.io/en/latest/developer_guide/index.html) may help answer additional questions.

The initial source files were created using [KitwareMedical/SlicerCustomAppTemplate](https://github.com/KitwareMedical/SlicerCustomAppTemplate).

## Prerequisites

- Setting up your git account:

  - Create a [Github](https://github.com) account.

  - Setup your SSH keys following [these](https://help.github.com/articles/generating-ssh-keys) instructions.

  - Setup [your git username](https://help.github.com/articles/setting-your-username-in-git) and [your git email](https://help.github.com/articles/setting-your-email-in-git).

## Checkout

1. Start `Git Bash`
2. Checkout the source code into a directory `C:\W\` by typing the following commands:

```bat
cd /c
mkdir W
cd /c/W
git clone https://github.com/Kitware/AutoSegmentSlicer.git A
```

Note: use short source and build directory names to avoid the [maximum path length limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file#maximum-path-length-limitation).

**MSB8066 (Custom build exited with code 1) / VTK install step:** This usually happens when the **build directory path is too long** (e.g. `M:\RKDrive\rk\AutoSegmentSlicer\AutoSegmentSlicer-Build`). VTK and other ExternalProjects can hit Windows path limits during the install step. **Fix:** Use a short build path. Run the script with a short path, e.g. `.\SuperBuild.ps1 -BuildDir "M:\ASS-Build"` or `.\SuperBuild.ps1 -BuildDir "C:\ASS-Build"`. The script now defaults to `M:\ASS-Build` if you do not pass `-BuildDir`. If you already started a build in a long path, delete that build folder and reconfigure with the short path.

**MSB8028 (shared intermediate directory):** The project applies a VTK patch so VTK is built with `CMAKE_INTERMEDIATE_DIR_STRATEGY=SHORT`. If you already had a build and see MSB8028, force VTK to reconfigure: delete the `VTK-build` folder and the `slicersources-build/VTK-prefix/src/VTK-stamp` folder in your build tree, then run the build again.

**ITK path length (59 > 50):** If you see "ITK source code directory path length is too long", the project applies an ITK patch and passes `-DITK_SKIP_PATH_LENGTH_CHECKS=ON`. If you had an existing build before this fix, delete the build directory (or at least `_deps/slicersources-src`) and reconfigure so the patch is applied.

## Build

Note: The build process can take hours.

<b>Option 1: CMake GUI and Visual Studio (Recommended)</b>

1. Start [CMake GUI](https://cmake.org/runningcmake/), select source directory `C:\W\A` and set build directory to `C:\W\AR`.
2. Add an entry `Qt5_DIR` pointing to `C:/Qt/${QT_VERSION}/${COMPILER}/lib/cmake/Qt5`.
3. Generate the project.
4. Open `C:\W\AR\AutoSegmentSlicer.sln`, select `Release` and build the project.

<b>Option 2: Command Line</b>

1. Start the [Command Line Prompt](http://windows.microsoft.com/en-us/windows/command-prompt-faq)
2. Configure and build the project in `C:\W\AR` by typing the following commands:

```bat
cd C:\W\
mkdir AR
cd AR
cmake -G "Visual Studio 17 2022" -A x64 -DQt5_DIR:PATH=`C:/Qt/${QT_VERSION}/${COMPILER}/lib/cmake/Qt5 ..\A
cmake --build . --config Release -- /maxcpucount:4
```

## Package

Install [NSIS 2](http://sourceforge.net/projects/nsis/files/)

<b>Option 1: CMake and Visual Studio</b>

1. In the `C:\W\AR\Slicer-build` directory, open `Slicer.sln` and build the `PACKAGE` target

<b>Option 2: Command Line</b>

1. Start the [Command Line Prompt](http://windows.microsoft.com/en-us/windows/command-prompt-faq)
2. Build the `PACKAGE` target by typing the following commands:

```bat
cd C:\W\AR\Slicer-build
cmake --build . --config Release --target PACKAGE
```
