import os
from typing import Optional

import qt
import slicer
import SlicerCustomAppUtilities
from slicer.ScriptedLoadableModule import (
    ScriptedLoadableModule,
    ScriptedLoadableModuleLogic,
    ScriptedLoadableModuleWidget,
)
from slicer.util import VTKObservationMixin

# Import to ensure the files are available through the Qt resource system
from Resources import HomeResources  # noqa: F401


class Home(ScriptedLoadableModule):
    """The home module allows to orchestrate and style the overall application workflow.

    It is a "special" module in the sense that its role is to customize the application and
    coordinate a workflow between other "regular" modules.

    Associated widget and logic are not intended to be initialized multiple times.
    """

    def __init__(self, parent: Optional[qt.QWidget]):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Home"
        self.parent.categories = [""]
        self.parent.dependencies = []
        self.parent.contributors = ["Sam Horvath (Kitware Inc.)", "Jean-Christophe Fillion-Robin (Kitware Inc.)"]
        self.parent.helpText = """This module orchestrates and styles the overall application workflow."""
        self.parent.helpText += self.getDefaultModuleDocumentationLink()
        self.parent.acknowledgementText = """..."""  # replace with organization, grant and thanks.


class HomeWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    @property
    def toolbarNames(self) -> list[str]:
        return [str(k) for k in self._toolbars]

    _toolbars: dict[str, qt.QToolBar] = {}

    def __init__(self, parent: Optional[qt.QWidget]):
        """Called when the application opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)
        self._volumesAlreadySetAsBackground = set()
        self._volumesAlreadySetAsForeground = set()

    def setup(self):
        """Called when the application opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer)
        self.uiWidget = slicer.util.loadUI(self.resourcePath("UI/Home.ui"))
        self.layout.addWidget(self.uiWidget)
        self.ui = slicer.util.childWidgetVariables(self.uiWidget)

        # Get references to relevant underlying modules
        # NA

        # Create logic class
        self.logic = HomeLogic()

        # Dark palette does not propagate on its own
        # See https://github.com/KitwareMedical/SlicerCustomAppTemplate/issues/72
        self.uiWidget.setPalette(slicer.util.mainWindow().style().standardPalette())

        # Wire Welcome quick action buttons to Slicer actions
        self._connectWelcomeButtons()

        # Wire Load volume by path (workaround for Add Data path bug)
        self.ui.LoadVolumePathButton.clicked.connect(self._onLoadVolumeByPathClicked)
        self.ui.LoadVolumePathBrowseButton.clicked.connect(self._onLoadVolumePathBrowseClicked)
        self.ui.OpenDICOMPatcherButton.clicked.connect(self.openDICOMPatcher)

        # Wire Auto-contouring buttons (Option A: extension, Option B: built-in module)
        self.ui.AutoContourViaExtensionButton.clicked.connect(self._onAutoContourViaExtensionClicked)
        self.ui.AutoContourModuleButton.clicked.connect(self._onAutoContourModuleClicked)

        # Set icons for quick action buttons (standard Qt icons)
        self._setWelcomeButtonIcons()

        # Wire Data Probe checkbox and sync with current state
        self.ui.ShowZoomedSliceCheckBox.toggled.connect(self._onShowZoomedSliceToggled)
        try:
            self.ui.ShowZoomedSliceCheckBox.blockSignals(True)
            self.ui.ShowZoomedSliceCheckBox.setChecked(slicer.util.getDataProbeVisible())
            self.ui.ShowZoomedSliceCheckBox.blockSignals(False)
        except Exception:
            pass

        # Remove unneeded UI elements or show full Slicer UI
        self.modifyWindowUI()
        # Default: show full Slicer UI (menu bar, toolbar, 4-panel layout); user can hide via Settings
        self.setCustomUIVisible(False)

        # Ensure four views (sagittal, axial, coronal, 3D) show on the home screen by default
        self._setConventionalFourViewLayout()

        # Enable slice planes in 3D view so the 3D window shows the slices (not empty)
        self._ensureSlicesVisibleIn3D()

        # Apply style
        self.applyApplicationStyle()

        # When user loads MRI/CT data, show it in all slice views (sagittal, axial, coronal)
        self.addObserver(slicer.mrmlScene, slicer.vtkMRMLScene.NodeAddedEvent, self._onMRMLNodeAdded)

        # Preload DICOM and segmentation modules so they are available (avoids "module is not loaded" when switching)
        self._preloadRequiredModules()

    def _preloadRequiredModules(self):
        """Preload DICOM and segmentation modules so they are available when the user switches to them."""
        required_modules = ["DICOM", "DICOMPatcher", "SegmentEditor", "SegmentStatistics"]
        for name in required_modules:
            self._loadModuleByName(name)

    def _loadModuleByName(self, name: str) -> bool:
        """Try to load a module by name (without switching UI); returns True if loaded or already loaded."""
        try:
            if hasattr(slicer.util, "getModule"):
                slicer.util.getModule(name)
                return True
        except Exception:
            pass
        for key in [name, name.lower(), name[0].lower() + name[1:]]:
            try:
                if hasattr(slicer.modules, key):
                    getattr(slicer.modules, key)
                    return True
            except Exception:
                pass
        return False

    def openDICOMPatcher(self):
        """Switch to DICOMPatcher module (loads it if not yet loaded). Use from UI or Python."""
        try:
            slicer.util.selectModule("DICOMPatcher")
        except Exception as e:
            slicer.util.errorDisplay(f"DICOMPatcher failed to load: {e}")

    def _onAutoContourViaExtensionClicked(self):
        """Option A: Open Extensions Manager so user can install an AI segmentation extension."""
        try:
            mainWindow = slicer.util.mainWindow()
            action = slicer.util.findChild(mainWindow, "OpenExtensionsManagerAction")
            if action and action.trigger:
                action.trigger()
            else:
                slicer.util.infoDisplay(
                    "Go to View → Extension Manager (or Help → Extension Manager) to install an AI segmentation extension (e.g. TotalSegmentator, MONAI Label)."
                )
        except Exception as e:
            slicer.util.errorDisplay(f"Could not open Extensions Manager: {e}")

    def _onAutoContourModuleClicked(self):
        """Option B: Switch to the built-in AutoContour module (add PyTorch/MONAI model there)."""
        try:
            slicer.util.selectModule("AutoContour")
        except Exception as e:
            slicer.util.errorDisplay(f"AutoContour module failed to load: {e}")

    def cleanup(self):
        """Called when the application closes and the module widget is destroyed."""
        try:
            self.removeObserver(slicer.mrmlScene, slicer.vtkMRMLScene.NodeAddedEvent, self._onMRMLNodeAdded)
        except Exception:
            pass

    def _setWelcomeButtonIcons(self):
        """Set standard icons for Welcome quick action buttons."""
        style = slicer.app.style()
        if style:
            self.ui.AddDataButton.setIcon(style.standardIcon(qt.QStyle.SP_DirIcon))
            self.ui.AddDICOMDataButton.setIcon(style.standardIcon(qt.QStyle.SP_FileIcon))
            self.ui.InstallExtensionsButton.setIcon(style.standardIcon(qt.QStyle.SP_ComputerIcon))
            self.ui.DownloadSampleDataButton.setIcon(style.standardIcon(qt.QStyle.SP_BrowserReload))
            self.ui.CustomizeSlicerButton.setIcon(qt.QIcon(self.resourcePath("Icons/Gears.png")))
            self.ui.ExploreAddedDataButton.setIcon(style.standardIcon(qt.QStyle.SP_FileDialogContentsView))

    def _setConventionalFourViewLayout(self):
        """Set layout to Four Up (4-panel: 3 slice views + 1 3D view) on home screen by default."""
        try:
            layoutManager = slicer.app.layoutManager()
            if layoutManager is None:
                return
            layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
        except Exception:
            pass

    def _connectWelcomeButtons(self):
        """Connect Welcome quick action buttons to Slicer actions."""
        self.ui.AddDataButton.clicked.connect(self._onAddDataClicked)
        self.ui.AddDICOMDataButton.clicked.connect(self._onAddDICOMDataClicked)
        self.ui.InstallExtensionsButton.clicked.connect(self._onInstallExtensionsClicked)
        self.ui.DownloadSampleDataButton.clicked.connect(self._onDownloadSampleDataClicked)
        self.ui.CustomizeSlicerButton.clicked.connect(self._onCustomizeSlicerClicked)
        self.ui.ExploreAddedDataButton.clicked.connect(self._onExploreAddedDataClicked)

    def _onAddDataClicked(self):
        """Open Add Data dialog."""
        try:
            slicer.app.ioManager().openAddDataDialog()
        except Exception:
            pass

    def _normalizeVolumePath(self, path: str) -> str:
        """Fix duplicated path like .../file.nii/file.nii -> .../file.nii."""
        path = (path or "").strip().replace("\\", "/")
        if not path:
            return path
        # If path ends with /filename/filename (same segment twice), use parent
        parts = path.rstrip("/").split("/")
        if len(parts) >= 2 and parts[-1] == parts[-2]:
            return "/".join(parts[:-1])
        return path

    def _onLoadVolumeByPathClicked(self):
        """Load a volume from the path in the line edit (workaround for Add Data path bug)."""
        le = self.ui.LoadVolumePathLineEdit
        raw = le.text() if callable(getattr(le, "text", None)) else getattr(le, "text", "")
        path = self._normalizeVolumePath(raw)
        if not path:
            slicer.util.warningDisplay("Enter a file path (e.g. M:/RKDrive/IA_Sub_001.nii).")
            return
        # Use OS-native path for file check and loading (handles M:/ and M:\)
        path_native = os.path.normpath(path.replace("/", os.sep))
        if not os.path.isfile(path_native):
            slicer.util.errorDisplay(
                f"File not found: {path_native}\n"
                "Check that the path is correct and the file exists (e.g. M: drive connected)."
            )
            return
        try:
            node = slicer.util.loadVolume(path_native, {"singleFile": True})
            if node:
                slicer.util.infoDisplay(f"Loaded: {node.GetName()}")
            else:
                slicer.util.warningDisplay(f"Load returned no node for: {path_native}")
        except Exception as e:
            err = str(e)
            slicer.util.errorDisplay(
                f"Load failed: {path_native}\n{err}\n\n"
                "If the file exists, try: Add Data from the menu and enable 'Show Options' for reader settings."
            )

    def _onLoadVolumePathBrowseClicked(self):
        """Open file dialog and set chosen path in the line edit."""
        result = qt.QFileDialog.getOpenFileName(
            self.uiWidget,
            "Select volume file (NIfTI, NRRD, etc.)",
            "",
            "Volumes (*.nii *.nii.gz *.nrrd *.nhdr *.mha *.mhd);;All files (*)",
        )
        # Qt5 returns (path, filter); Qt6 returns path only; some bindings return more
        path = result[0] if isinstance(result, (tuple, list)) else result
        if path:
            self.ui.LoadVolumePathLineEdit.setText(path.replace("\\", "/"))

    def _onAddDICOMDataClicked(self):
        """Open DICOM browser or switch to DICOM module."""
        try:
            slicer.util.selectModule("DICOM")
        except Exception:
            pass

    def _onInstallExtensionsClicked(self):
        """Open Extensions Manager."""
        try:
            mainWindow = slicer.util.mainWindow()
            action = slicer.util.findChild(mainWindow, "OpenExtensionsManagerAction")
            if action:
                action.trigger()
        except Exception:
            pass

    def _onDownloadSampleDataClicked(self):
        """Switch to Sample Data module."""
        try:
            slicer.util.selectModule("SampleData")
        except Exception:
            pass

    def _onCustomizeSlicerClicked(self):
        """Switch to Application Settings or show layout options."""
        try:
            slicer.util.selectModule("ApplicationSettings")
        except Exception:
            pass

    def _onExploreAddedDataClicked(self):
        """Switch to Data module to explore loaded data."""
        try:
            slicer.util.selectModule("Data")
        except Exception:
            pass

    def _onShowZoomedSliceToggled(self, checked: bool):
        """Toggle data probe visibility (zoomed slice is part of data probe)."""
        try:
            slicer.util.setDataProbeVisible(checked)
        except Exception:
            pass

    def _onMRMLNodeAdded(self, caller, event, callData=None):
        """When a volume, segmentation, or markup is added, show it by default in slice and 3D views."""
        if caller != slicer.mrmlScene or event != slicer.vtkMRMLScene.NodeAddedEvent:
            return
        node = callData
        if node is None:
            return
        # Volumes: first as background; second (e.g. label map / annotation) as foreground overlay so annotations show
        if node.IsA("vtkMRMLScalarVolumeNode") or node.IsA("vtkMRMLVolumeNode"):
            if node.GetID() not in self._volumesAlreadySetAsBackground and node.GetID() not in self._volumesAlreadySetAsForeground:
                if len(self._volumesAlreadySetAsBackground) == 0:
                    # First volume: set as background
                    self._setVolumeAsBackgroundInAllSliceViews(node)
                    self._volumesAlreadySetAsBackground.add(node.GetID())
                else:
                    # Second (or later) volume: set as foreground overlay so annotations show by default
                    self._setVolumeAsForegroundInAllSliceViews(node)
                    self._volumesAlreadySetAsForeground.add(node.GetID())
        # Segmentations (e.g. from .seg.nrrd): show in 2D and 3D by default
        if node.IsA("vtkMRMLSegmentationNode"):
            self._setSegmentationVisibleByDefault(node)
        # Markups (fiducials, curves, etc.): show by default
        if node.IsA("vtkMRMLMarkupsNode"):
            self._setMarkupVisibleByDefault(node)

    def _setSliceNodeVisibleIn3D(self, sliceNode):
        """Enable a slice node to be visible in the 3D view (slice planes in 3D window)."""
        if sliceNode is None:
            return
        try:
            if hasattr(sliceNode, "SetSliceVisibleIn3D"):
                sliceNode.SetSliceVisibleIn3D(1)
            elif hasattr(sliceNode, "SetInteractionFlags") and hasattr(sliceNode, "GetInteractionFlags"):
                # SliceVisibleIn3D is often flag 128 (0x80)
                flags = sliceNode.GetInteractionFlags()
                sliceNode.SetInteractionFlags(flags | 0x80)
        except Exception:
            pass

    def _ensureSlicesVisibleIn3D(self):
        """Enable all slice planes to show in the 3D view so the 3D window is not empty."""
        try:
            layoutManager = slicer.app.layoutManager()
            if layoutManager is None:
                return
            for viewName in layoutManager.sliceViewNames():
                try:
                    sliceWidget = layoutManager.sliceWidget(viewName)
                    if sliceWidget and sliceWidget.sliceLogic():
                        sliceNode = sliceWidget.sliceLogic().GetSliceNode()
                        self._setSliceNodeVisibleIn3D(sliceNode)
                except Exception:
                    pass
            # Also set all slice nodes from the scene (in case layout uses different nodes)
            try:
                for i in range(slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLSliceNode")):
                    sliceNode = slicer.mrmlScene.GetNthNodeByClass(i, "vtkMRMLSliceNode")
                    self._setSliceNodeVisibleIn3D(sliceNode)
            except Exception:
                pass
            # Set first volume as background in slices and reset 3D camera if we have a volume
            try:
                volNodes = slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")
                if not volNodes:
                    volNodes = slicer.util.getNodesByClass("vtkMRMLVolumeNode")
                if volNodes and layoutManager:
                    firstVol = next(iter(volNodes.values()), None)
                    if firstVol:
                        self._setVolumeAsBackgroundInAllSliceViews(firstVol)
            except Exception:
                pass
        except Exception:
            pass

    def _setVolumeAsBackgroundInAllSliceViews(self, volumeNode):
        """Set the given volume as background in Red, Yellow, Green slice views and show slices in 3D view."""
        try:
            layoutManager = slicer.app.layoutManager()
            if layoutManager is None:
                return
            volumeId = volumeNode.GetID()
            for viewName in layoutManager.sliceViewNames():
                try:
                    sliceWidget = layoutManager.sliceWidget(viewName)
                    if sliceWidget and sliceWidget.sliceLogic():
                        compositeNode = sliceWidget.sliceLogic().GetSliceCompositeNode()
                        if compositeNode:
                            compositeNode.SetBackgroundVolumeID(volumeId)
                        sliceNode = sliceWidget.sliceLogic().GetSliceNode()
                        self._setSliceNodeVisibleIn3D(sliceNode)
                except Exception:
                    pass
            # Reset 3D camera so the volume/slices are framed in the 3D view
            try:
                threeDWidget = layoutManager.threeDWidget(0)
                if threeDWidget and threeDWidget.threeDView():
                    threeDWidget.threeDView().resetCamera()
            except Exception:
                pass
        except Exception:
            pass

    def _setVolumeAsForegroundInAllSliceViews(self, volumeNode):
        """Set the given volume as foreground overlay in slice views (for label maps / annotations)."""
        try:
            layoutManager = slicer.app.layoutManager()
            if layoutManager is None:
                return
            volumeId = volumeNode.GetID()
            for viewName in layoutManager.sliceViewNames():
                try:
                    sliceWidget = layoutManager.sliceWidget(viewName)
                    if sliceWidget and sliceWidget.sliceLogic():
                        compositeNode = sliceWidget.sliceLogic().GetSliceCompositeNode()
                        if compositeNode:
                            compositeNode.SetForegroundVolumeID(volumeId)
                            if hasattr(compositeNode, "SetForegroundOpacity"):
                                compositeNode.SetForegroundOpacity(0.5)
                except Exception:
                    pass
        except Exception:
            pass

    def _setSegmentationVisibleByDefault(self, segmentationNode):
        """Turn on 2D and 3D visibility for a segmentation so annotations show by default."""
        if segmentationNode is None:
            return
        try:
            disp = segmentationNode.GetDisplayNode()
            if disp is None:
                return
            disp.SetVisibility(1)
            if hasattr(disp, "Visibility2DFillOn"):
                disp.Visibility2DFillOn()
            if hasattr(disp, "Visibility2DOutlineOn"):
                disp.Visibility2DOutlineOn()
            if hasattr(disp, "Visibility3DOn"):
                disp.Visibility3DOn()
            if hasattr(disp, "SetVisibility2D"):
                disp.SetVisibility2D(1)
            if hasattr(disp, "SetVisibility3D"):
                disp.SetVisibility3D(1)
        except Exception:
            pass

    def _setMarkupVisibleByDefault(self, markupNode):
        """Turn on visibility for markups (fiducials, curves, etc.) so annotations show by default."""
        if markupNode is None:
            return
        try:
            disp = markupNode.GetDisplayNode()
            if disp is not None and hasattr(disp, "SetVisibility"):
                disp.SetVisibility(1)
        except Exception:
            pass

    def setSlicerUIVisible(self, visible: bool):
        exemptToolbars = [
            "MainToolBar",
            "ViewToolBar",
            *self.toolbarNames,
        ]
        slicer.util.setDataProbeVisible(visible)
        slicer.util.setMenuBarsVisible(visible, ignore=exemptToolbars)
        slicer.util.setModuleHelpSectionVisible(visible)
        slicer.util.setModulePanelTitleVisible(visible)
        slicer.util.setPythonConsoleVisible(visible)
        slicer.util.setApplicationLogoVisible(visible)
        keepToolbars = [slicer.util.findChild(slicer.util.mainWindow(), toolbarName) for toolbarName in exemptToolbars]
        slicer.util.setToolbarsVisible(visible, keepToolbars)

    def modifyWindowUI(self):
        """Customize the entire user interface to resemble the custom application"""
        # Custom toolbars
        self.initializeSettingsToolBar()

    def insertToolBar(self, beforeToolBarName: str, name: str, title: Optional[str] = None) -> qt.QToolBar:
        """Helper method to insert a new toolbar between existing ones"""
        beforeToolBar = slicer.util.findChild(slicer.util.mainWindow(), beforeToolBarName)

        if title is None:
            title = name

        toolBar = qt.QToolBar(title)
        toolBar.name = name
        slicer.util.mainWindow().insertToolBar(beforeToolBar, toolBar)

        self._toolbars[name] = toolBar

        return toolBar

    def initializeSettingsToolBar(self):
        """Create toolbar and dialog for app settings"""
        settingsToolBar = self.insertToolBar("MainToolBar", "SettingsToolBar", title="Settings")

        gearIcon = qt.QIcon(self.resourcePath("Icons/Gears.png"))
        self.settingsAction = settingsToolBar.addAction(gearIcon, "")

        # Settings dialog
        self.settingsDialog = slicer.util.loadUI(self.resourcePath("UI/Settings.ui"))
        self.settingsUI = slicer.util.childWidgetVariables(self.settingsDialog)
        self.settingsUI.CustomUICheckBox.toggled.connect(self.setCustomUIVisible)
        self.settingsUI.CustomStyleCheckBox.toggled.connect(self.toggleStyle)
        self.settingsAction.triggered.connect(self.raiseSettings)

    def toggleStyle(self, visible: bool):
        if visible:
            self.applyApplicationStyle()
        else:
            slicer.app.styleSheet = ""

    def raiseSettings(self, _):
        self.settingsDialog.exec()

    def setCustomUIVisible(self, visible: bool):
        self.setSlicerUIVisible(not visible)

    def applyApplicationStyle(self):
        SlicerCustomAppUtilities.applyStyle([slicer.app], self.resourcePath("Home.qss"))
        self.styleThreeDWidget()
        self.styleSliceWidgets()

    def styleThreeDWidget(self):
        viewNode = slicer.app.layoutManager().threeDWidget(0).mrmlViewNode()  # noqa: F841
        # viewNode.SetBackgroundColor(0.0, 0.0, 0.0)
        # viewNode.SetBackgroundColor2(0.0, 0.0, 0.0)
        # viewNode.SetBoxVisible(False)
        # viewNode.SetAxisLabelsVisible(False)
        # viewNode.SetOrientationMarkerType(slicer.vtkMRMLViewNode.OrientationMarkerTypeAxes)

    def styleSliceWidgets(self):
        for name in slicer.app.layoutManager().sliceViewNames():
            sliceWidget = slicer.app.layoutManager().sliceWidget(name)
            self.styleSliceWidget(sliceWidget)

    def styleSliceWidget(self, sliceWidget: slicer.qMRMLSliceWidget):
        controller = sliceWidget.sliceController()  # noqa: F841
        # controller.sliceViewLabel = ""
        # slicer.util.findChild(sliceWidget, "PinButton").visible = False
        # slicer.util.findChild(sliceWidget, "ViewLabel").visible = False
        # slicer.util.findChild(sliceWidget, "FitToWindowToolButton").visible = False
        # slicer.util.findChild(sliceWidget, "SliceOffsetSlider").spinBoxVisible = False


class HomeLogic(ScriptedLoadableModuleLogic):
    """
    Implements underlying logic for the Home module.
    """

    pass
