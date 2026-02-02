"""
AutoContour: built-in module for AI-based auto-contouring (Option B).

Add your PyTorch/MONAI/ONNX model in AutoContourLogic.run().
Input: selected volume (CT/MRI).
Output: new segmentation node in the scene.
"""

from typing import Optional

import qt
import slicer
from slicer.ScriptedLoadableModule import (
    ScriptedLoadableModule,
    ScriptedLoadableModuleLogic,
    ScriptedLoadableModuleWidget,
)

# Import to ensure resources are available (generated at build time)
try:
    from Resources import AutoContourResources  # noqa: F401
except ImportError:
    pass


class AutoContour(ScriptedLoadableModule):
    """Module for AI-based auto-contouring (add your model in the logic)."""

    def __init__(self, parent: Optional[qt.QWidget]):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "AutoContour"
        self.parent.categories = ["Segmentation"]
        self.parent.dependencies = []
        self.parent.contributors = ["AutoSegmentSlicer"]
        self.parent.helpText = (
            "Run AI segmentation on the selected volume. "
            "Add your PyTorch/MONAI/ONNX model in AutoContourLogic.run()."
        )
        self.parent.acknowledgementText = ""


class AutoContourWidget(ScriptedLoadableModuleWidget):
    """UI for AutoContour: volume selector + Run button."""

    def __init__(self, parent: Optional[qt.QWidget]):
        ScriptedLoadableModuleWidget.__init__(self, parent)

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        self.uiWidget = slicer.util.loadUI(self.resourcePath("UI/AutoContour.ui"))
        self.layout.addWidget(self.uiWidget)
        self.ui = slicer.util.childWidgetVariables(self.uiWidget)

        self.logic = AutoContourLogic()

        self.ui.RunButton.clicked.connect(self._onRunClicked)

    def _onRunClicked(self):
        volumeNode = self.ui.InputVolumeSelector.currentNode()
        if not volumeNode:
            slicer.util.warningDisplay("Select a volume first.")
            return
        try:
            segmentationNode = self.logic.run(volumeNode)
            if segmentationNode:
                slicer.util.infoDisplay(f"Created segmentation: {segmentationNode.GetName()}")
        except Exception as e:
            slicer.util.errorDisplay(f"Auto-contour failed: {e}")


class AutoContourLogic(ScriptedLoadableModuleLogic):
    """
    Logic for auto-contouring.

    Replace the placeholder below with your PyTorch/MONAI/ONNX inference:
    - Load your model (e.g. torch.load, MONAI, onnxruntime).
    - Run inference on the volume's image data.
    - Convert the output to a vtkMRMLSegmentationNode (or label map volume) and add to the scene.
    """

    def run(self, volumeNode) -> Optional["vtkMRMLSegmentationNode"]:
        """
        Run AI segmentation on the given volume.

        Args:
            volumeNode: vtkMRMLScalarVolumeNode (CT/MRI).

        Returns:
            New vtkMRMLSegmentationNode in the scene, or None.
        """
        if not volumeNode or not volumeNode.GetImageData():
            return None

        # Placeholder: create an empty segmentation so the pipeline is ready.
        # Replace this block with your model inference, e.g.:
        #   import torch
        #   output = model(tensor_from_volume(volumeNode))
        #   segmentation = label_map_to_segmentation(output)
        segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
        segmentationNode.SetName(volumeNode.GetName() + " - AutoContour")
        segmentationNode.CreateDefaultDisplayNodes()

        # When you add real inference (PyTorch/MONAI/ONNX), replace the above with:
        # - Get volume as numpy/tensor, run model, convert output to segmentation segments.
        # - Use segmentationNode.GetSegmentation().AddSegment(segment) for each label.

        return segmentationNode
