# PES Face/Hair Modifier

PES Face/Hair Modifier is a Blender add-on for importing, editing, and exporting PES face and hair assets.

This **1.0.0 updated edition** was prepared by **Lucky Facemaker** from the original PES Face/Hair Modifier project. Its purpose is to make the original tool compatible with **Blender 4.5 and later**, while preserving the original project, authorship, and credits.

This edition is an update of the existing project, not a claim of authorship over the original work.

## Main features

- Import and export PES FMDL face, hair, and oral meshes.
- Extract and rebuild supported face FPK packages.
- Import `face_diff.bin` data and position the eye objects.
- Edit FMDL material, shader, texture, skeleton, bone-group, and bounding-box settings.
- Transfer, wrap, and clear custom normals.
- Use a unified sidebar interface in current Blender versions.
- Store imported FMDL material metadata inside the `.blend` file as an internal backup.

## Requirements

- Blender 4.5 or later.
- Windows for the original bundled FPK, FTEX, and DDS conversion utilities.

## Installation

1. Remove or disable any previous PES Face/Hair Modifier installation.
2. Restart Blender.
3. Open **Edit > Preferences > Add-ons**.
4. Select **Install from Disk** and choose the add-on ZIP without extracting it.
5. Enable **PES Face/Hair Modifier**.

## Interface

Open the 3D View sidebar with the **N** key and select the **PES Tools** tab.

The tools are organized into expandable sections:

- Import / Export
- Mesh Settings
- Materials and Shaders
- Textures
- Bone Groups
- Skeleton
- Bounding Boxes
- Transfer Normals

## Updated edition

Updated by **Lucky Facemaker**.

Changes in this edition include compatibility work for Blender 4.5+, updates for current material and mesh APIs, automatic eye loading through `face_diff.bin`, safer Alpha/Shadow callbacks, corrected RGBA export, and export behavior that does not depend on the currently selected object.

The add-on version remains **1.0.0** until a new version is explicitly released.

## Original project and authorship

Original PES Face/Hair Modifier project:

- [MjTs140914/PES_Face_Hair_Modifier](https://github.com/MjTs140914/PES_Face_Hair_Modifier)

The original project states that it is heavily based on:

- [PES-FMDL by the4chancup](https://github.com/the4chancup/PES-FMDL)

Original project authors and contributors include:

- MjTs-140914
- the4chancup
- leus
- Atvaark — GzsTool
- zlac — `pes_diff.bin` research/work
- Blenderanon
- 魔大农

Original pre-release testers:

- Tsunami07
- aliefzv01
- barcerojas
- Fleishman-
- Gabri Facemaker
- ryudek
- Ummah Qiya

Additional credit belongs to the Blender community, Blender.org, Microsoft DirectXTex, and Chuck Walbourn, as identified by the original project.

## License

The original project is distributed under the **MIT License**. Refer to the original repository for its authoritative license text and project history.

## Disclaimer

PES, eFootball, and related names and assets belong to their respective owners. This community tool is not affiliated with or endorsed by Konami.
