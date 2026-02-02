# AutoSegmentSlicer by Kitware, Inc.

AutoSegmentSlicer is a specialized medical imaging application designed to eliminate the bottleneck of manual organ and lesion contouring. By integrating state-of-the-art Artificial Intelligence with the robust 3D Slicer engine, it transforms raw volumetric data (CT/MRI) into high-fidelity, annotated 3D models with a single click.

_This project is in active development and may change from version to version without notice,_

## Table of contents

- [Features](#features)
- [Development](#development)

## Features

- **Home** – Welcome screen with quick actions (Add Data, DICOM, Load volume by path, etc.) and Four Up layout.
- **Auto-contouring (Option A)** – “Auto-contour (via extension)” opens the Extensions Manager to install an AI segmentation extension (e.g. TotalSegmentator, MONAI Label).
- **Auto-contouring (Option B)** – Built-in **AutoContour** module: select a volume and run (add your PyTorch/MONAI/ONNX model in the logic).
- **Annotations by default** – Loaded segmentations and second volumes (e.g. label maps) are shown in 2D/3D by default.
- **DICOM, Segment Editor, Segment Statistics** – Preloaded and available from Home.

## Development

- [Contributing](CONTRIBUTING.md)
- [Building on Windows](BUILD_WINDOWS.md)
- [Building on Linux](BUILD_LINUX.md)

![AutoSegmentSlicer by Kitware, Inc.](Applications/AutoSegmentSlicerApp/Resources/Images/LogoFull.png?raw=true)
