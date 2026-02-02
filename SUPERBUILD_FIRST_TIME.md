# SuperBuild – First-Time Build (AutoSegmentSlicer)

Follow every step below in order. The first build takes **1–3 hours** and downloads ~5GB; you only do this once. After that you get **AutoSegmentSlicer.exe**.

---

## Part A: Install the builders (one-time)

Do Part A once before Part B and Part C.

---

### Step A1: Download Qt Online Installer

**Option A – Run the project script (easiest):**  
Open PowerShell, go to the project scripts folder, and run:
```powershell
cd "M:\RK Drive\rk\AutoSegmentSlicer\AutoSegmentSlicer\scripts"
.\Install-Qt5152.ps1
```
The script downloads the installer (if needed) and starts it with install path `C:\Qt`. Then do steps A2–A4 in the installer window.

**Option B – Manual download:**  
1. Open a browser and go to: **https://www.qt.io/download-qt-installer**  
   Or direct: **https://download.qt.io/official_releases/online_installers/qt-online-installer-windows-x64-online.exe**  
2. Download the **Qt Online Installer for Windows** (e.g. `qt-online-installer-windows-x64-online.exe`).  
3. Run the downloaded installer.

---

### Step A2: Sign in to Qt

4. When the installer opens, **Sign in** with your Qt account, or **Sign up** to create one (required).
5. Accept the open-source license if prompted and continue.

---

### Step A3: Choose installation path

6. On the **Installation folder** screen, leave the default **`C:\Qt`** (recommended), or choose another folder. Click **Next**.

---

### Step A4: Select Qt version and compiler

7. On the **Select Components** screen, under **Qt**, expand the list.
8. Find **Qt 5.15.2** (or latest 5.15.x) and check the box next to it.
9. Under **Qt 5.15.2**, check **one** of these (must match your Visual Studio):
   - **MSVC 2019 64-bit** — if you have or will install Visual Studio 2019
   - **MSVC 2022 64-bit** — if you have or will install Visual Studio 2022
10. Under **Qt 5.15.2**, expand **Additional Libraries**.
11. Check **Qt WebEngine** (required for this project).
12. Click **Next**, then **Install**, and wait for the download and install to finish.
13. Click **Finish** when done.

**Write down your Qt5_DIR path** (you will use it in Part B):

- If you used **MSVC 2019 64-bit** and default path: **`C:/Qt/5.15.2/msvc2019_64/lib/cmake/Qt5`**
- If you used **MSVC 2022 64-bit** and default path: **`C:/Qt/5.15.2/msvc2022_64/lib/cmake/Qt5`**
- If you chose a different install folder, replace `C:/Qt` with your path.

---

### Step A5: Install CMake

14. Go to **https://cmake.org/download/**.
15. Download **Windows x64 Installer** (e.g. `cmake-3.x.x-windows-x86_64.msi`).
16. Run the installer.
17. When asked, choose **"Add CMake to the system PATH for all users"** (or "for current user").
18. Complete the installation.

---

### Step A6: Install Visual Studio (if not already installed)

19. Download **Visual Studio 2022** or **Visual Studio 2019** from https://visualstudio.microsoft.com/downloads/ (Community is free).
20. Run the installer.
21. On the **Workloads** tab, check **"Desktop development with C++"**.
22. Install. This installs the compiler and **x64** toolset.  
    Use **VS 2022** if you selected Qt **MSVC 2022 64-bit** in Step A4; use **VS 2019** if you selected **MSVC 2019 64-bit**.

---

## Part B: Configure the project with CMake

Do this only after Part A is complete. Use either **CMake GUI** (steps B1–B8) or **command line** (steps B9–B10).

**Path with spaces:** If your path contains a space (e.g. `M:\RK Drive\rk\...`), some build steps may fail. For a reliable build, use a path without spaces (e.g. `C:\Build\AutoSegmentSlicer-Build`).

---

### Step B1: Create the build folder (if not already created)

1. Open **File Explorer**.
2. Go to **`M:\RK Drive\rk`**.
3. If the folder **`AutoSegmentSlicer-Build`** does not exist, right‑click → **New** → **Folder** and name it **`AutoSegmentSlicer-Build`**.  
   The build folder must be **outside** the source folder (not inside `AutoSegmentSlicer`).

---

### Step B2: Open CMake GUI

4. Press **Windows key**, type **cmake**, and open **CMake (cmake-gui)**.

---

### Step B3: Set the source directory

5. In CMake GUI, next to **"Where is the source code"**, click **Browse Source**.
6. Go to **`M:\RK Drive\rk\AutoSegmentSlicer\AutoSegmentSlicer`** and select that folder (the one that contains `CMakeLists.txt`).
7. Click **OK**.

---

### Step B4: Set the build directory

8. Next to **"Where to build the binaries"**, click **Browse Build**.
9. Go to **`M:\RK Drive\rk\AutoSegmentSlicer-Build`** and select that folder.
10. Click **OK**.

---

### Step B5: Add Qt5_DIR

11. Click **Add Entry**.
12. In **Name**, type: **`Qt5_DIR`**
13. In **Type**, choose: **PATH**
14. In **Value**, enter one of these (use the path you wrote down in Step A4):
    - For **Visual Studio 2019** / Qt MSVC 2019: **`C:/Qt/5.15.2/msvc2019_64/lib/cmake/Qt5`**
    - For **Visual Studio 2022** / Qt MSVC 2022: **`C:/Qt/5.15.2/msvc2022_64/lib/cmake/Qt5`**
15. Click **OK** to close the Add Entry dialog.

**If your source or build path has spaces** (e.g. `M:\RK Drive\rk\...`), add two more entries so the build is allowed:
- **Add Entry** → Name: `Slicer_SKIP_ROOT_DIR_MAX_LENGTH_CHECK`, Type: BOOL, Value: ✓ (checked).
- **Add Entry** → Name: `Slicer_SKIP_DIR_WITH_SPACES_CHECK`, Type: BOOL, Value: ✓ (checked).

---

### Step B6: Configure

16. Click **Configure**.
17. In the generator dialog, choose:
    - **Visual Studio 17 2022** with **x64** (if you use VS 2022), or
    - **Visual Studio 16 2019** with **x64** (if you use VS 2019).
18. Click **Finish**.
19. Wait until configuration finishes (the log will show "Configuring done").
20. If you see **red** rows in the list, check the error message (often wrong `Qt5_DIR`). Fix the value and click **Configure** again.
21. Repeat until there are **no red** entries, then click **Configure** one more time to be sure.

---

### Step B7: Generate

22. Click **Generate**.
23. Wait until the log shows "Generating done".

---

### Step B8: Open the project in Visual Studio

24. Click **Open Project**. Visual Studio will open with the solution.  
    Continue to **Part C** to build.

---

### Alternative: Configure from command line (instead of B2–B8)

25. Open **PowerShell**.
26. Run:
    ```powershell
    cd "M:\RK Drive\rk\AutoSegmentSlicer-Build"
    ```
27. Set Qt5_DIR (use one line; match your Qt/VS version):
    - VS 2019:  
      `$Qt5_DIR = "C:/Qt/5.15.2/msvc2019_64/lib/cmake/Qt5"`
    - VS 2022:  
      `$Qt5_DIR = "C:/Qt/5.15.2/msvc2022_64/lib/cmake/Qt5"`
28. Run CMake (use one line; match your Visual Studio).  
    **If your source or build path has spaces or is long** (e.g. `M:\RK Drive\rk\...`), add these two options:  
    `-DSlicer_SKIP_ROOT_DIR_MAX_LENGTH_CHECK:BOOL=TRUE -DSlicer_SKIP_DIR_WITH_SPACES_CHECK:BOOL=TRUE`
    - VS 2022:  
      `cmake -G "Visual Studio 17 2022" -A x64 -DQt5_DIR:PATH="$Qt5_DIR" -DSlicer_SKIP_ROOT_DIR_MAX_LENGTH_CHECK:BOOL=TRUE -DSlicer_SKIP_DIR_WITH_SPACES_CHECK:BOOL=TRUE "M:\RK Drive\rk\AutoSegmentSlicer\AutoSegmentSlicer"`
    - VS 2019:  
      `cmake -G "Visual Studio 16 2019" -A x64 -DQt5_DIR:PATH="$Qt5_DIR" -DSlicer_SKIP_ROOT_DIR_MAX_LENGTH_CHECK:BOOL=TRUE -DSlicer_SKIP_DIR_WITH_SPACES_CHECK:BOOL=TRUE "M:\RK Drive\rk\AutoSegmentSlicer\AutoSegmentSlicer"`
29. Then open the solution in Visual Studio: go to **`M:\RK Drive\rk\AutoSegmentSlicer-Build`** and double‑click **`AutoSegmentSlicer.sln`**, and continue to Part C.

---

## Part C: Build the project

Do this after Part B (CMake configuration and generate are done).

---

### Step C1: Switch to Release

1. In **Visual Studio**, in the top toolbar, find the configuration dropdown (it usually says **Debug**).
2. Change it to **Release**.

---

### Step C2: Build ALL_BUILD

3. On the right, open **Solution Explorer** (View → Solution Explorer if needed).
4. In the list, find **ALL_BUILD** (it may be under the main solution node).
5. **Right‑click** **ALL_BUILD**.
6. Click **Build**.

---

### Step C3: Wait for the build to finish

7. The first build takes **1–3 hours** and downloads about **5 GB**. Do not close Visual Studio.
8. When it finishes, the bottom status will show **Build succeeded** (or similar).
9. **AutoSegmentSlicer.exe** will be in your build tree, often under a folder like **`Slicer-build`** inside **`M:\RK Drive\rk\AutoSegmentSlicer-Build`**. Use Windows Search in that folder for **`AutoSegmentSlicer.exe`** if needed.

---

### Alternative: Build from command line (instead of C1–C3)

10. Open **PowerShell** and run:
    ```powershell
    cd "M:\RK Drive\rk\AutoSegmentSlicer-Build"
    cmake --build . --config Release -- /maxcpucount:4
    ```
11. Wait for the build to finish. The executable location is the same as in Step C3.

---

## Quick reference (copy‑paste)

| Item | Value |
|------|--------|
| Source folder | `M:\RK Drive\rk\AutoSegmentSlicer\AutoSegmentSlicer` |
| Build folder | `M:\RK Drive\rk\AutoSegmentSlicer-Build` |
| Qt5_DIR (VS 2019) | `C:/Qt/5.15.2/msvc2019_64/lib/cmake/Qt5` |
| Qt5_DIR (VS 2022) | `C:/Qt/5.15.2/msvc2022_64/lib/cmake/Qt5` |

---

## Summary

| Part | What you do |
|------|------------------|
| **A** | Install Qt 5.15.2 (with Qt WebEngine), CMake, and Visual Studio (C++ workload). |
| **B** | Configure: set source and build folders in CMake, add **Qt5_DIR**, Configure, then Generate. Open the solution in Visual Studio. |
| **C** | In Visual Studio: set configuration to **Release**, build **ALL_BUILD**, wait for the first long build. |

After the first successful build, use the same build folder for future builds; only changed parts will be recompiled.





Set-Location "M:\RKDrive\rk\AutoSegmentSlicer\AutoSegmentSlicer\scripts"; .\SuperBuild.ps1 -BuildOnly
