/*==============================================================================

  Copyright (c) Kitware, Inc.

  See http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware, Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

#ifndef __qAutoSegmentSlicerAppMainWindow_h
#define __qAutoSegmentSlicerAppMainWindow_h

// AutoSegmentSlicer includes
#include "qAutoSegmentSlicerAppExport.h"
class qAutoSegmentSlicerAppMainWindowPrivate;

// Slicer includes
#include "qSlicerMainWindow.h"

class Q_AUTOSEGMENTSLICER_APP_EXPORT qAutoSegmentSlicerAppMainWindow : public qSlicerMainWindow
{
  Q_OBJECT
public:
  typedef qSlicerMainWindow Superclass;

  qAutoSegmentSlicerAppMainWindow(QWidget *parent=0);
  virtual ~qAutoSegmentSlicerAppMainWindow();

public slots:
  void on_HelpAboutAutoSegmentSlicerAppAction_triggered();

protected:
  void showEvent(QShowEvent* event) override;
  qAutoSegmentSlicerAppMainWindow(qAutoSegmentSlicerAppMainWindowPrivate* pimpl, QWidget* parent);

private:
  Q_DECLARE_PRIVATE(qAutoSegmentSlicerAppMainWindow);
  Q_DISABLE_COPY(qAutoSegmentSlicerAppMainWindow);
};

#endif
