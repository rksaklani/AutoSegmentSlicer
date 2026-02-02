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

// AutoSegmentSlicer includes
#include "qAutoSegmentSlicerAppMainWindow.h"
#include "qAutoSegmentSlicerAppMainWindow_p.h"

// Qt includes
#include <QDesktopWidget>
#include <QLabel>
#include <QSettings>
#include <QShowEvent>
#include <QTimer>

// Slicer includes
#include "qSlicerApplication.h"
#include "qSlicerAboutDialog.h"
#include "qSlicerMainWindow_p.h"
#include "qSlicerLayoutManager.h"
#include "qSlicerModuleSelectorToolBar.h"
#include "qMRMLWidget.h"

// MRML includes
#include <vtkMRMLLayoutNode.h>

//-----------------------------------------------------------------------------
// qAutoSegmentSlicerAppMainWindowPrivate methods

qAutoSegmentSlicerAppMainWindowPrivate::qAutoSegmentSlicerAppMainWindowPrivate(qAutoSegmentSlicerAppMainWindow& object)
  : Superclass(object)
{
}

//-----------------------------------------------------------------------------
qAutoSegmentSlicerAppMainWindowPrivate::~qAutoSegmentSlicerAppMainWindowPrivate()
{
}

//-----------------------------------------------------------------------------
void qAutoSegmentSlicerAppMainWindowPrivate::init()
{
#if (QT_VERSION >= QT_VERSION_CHECK(5, 7, 0))
  QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
#endif
  Q_Q(qAutoSegmentSlicerAppMainWindow);
  this->Superclass::init();
}

//-----------------------------------------------------------------------------
void qAutoSegmentSlicerAppMainWindowPrivate::setupUi(QMainWindow * mainWindow)
{
  qSlicerApplication * app = qSlicerApplication::application();

  //----------------------------------------------------------------------------
  // Add actions
  //----------------------------------------------------------------------------
  QAction* helpAboutSlicerAppAction = new QAction(mainWindow);
  helpAboutSlicerAppAction->setObjectName("HelpAboutAutoSegmentSlicerAppAction");
  helpAboutSlicerAppAction->setText(qAutoSegmentSlicerAppMainWindow::tr("About %1").arg(qSlicerApplication::application()->mainApplicationDisplayName()));

  //----------------------------------------------------------------------------
  // Calling "setupUi()" after adding the actions above allows the call
  // to "QMetaObject::connectSlotsByName()" done in "setupUi()" to
  // successfully connect each slot with its corresponding action.
  this->Superclass::setupUi(mainWindow);

  // Add Help Menu Action
  this->HelpMenu->addAction(helpAboutSlicerAppAction);

  //----------------------------------------------------------------------------
  // Configure
  //----------------------------------------------------------------------------
  mainWindow->setWindowIcon(QIcon(":/Icons/Medium/DesktopIcon.png"));

  QLabel* logoLabel = new QLabel();
  logoLabel->setObjectName("LogoLabel");
  logoLabel->setPixmap(qMRMLWidget::pixmapFromIcon(QIcon(":/LogoFull.png")));
  this->PanelDockWidget->setTitleBarWidget(logoLabel);

  // Hide the menus
  //this->menubar->setVisible(false);
  //this->FileMenu->setVisible(false);
  //this->EditMenu->setVisible(false);
  //this->ViewMenu->setVisible(false);
  //this->LayoutMenu->setVisible(false);
  //this->HelpMenu->setVisible(false);
}

//-----------------------------------------------------------------------------
// qAutoSegmentSlicerAppMainWindow methods

//-----------------------------------------------------------------------------
qAutoSegmentSlicerAppMainWindow::qAutoSegmentSlicerAppMainWindow(QWidget* windowParent)
  : Superclass(new qAutoSegmentSlicerAppMainWindowPrivate(*this), windowParent)
{
  Q_D(qAutoSegmentSlicerAppMainWindow);
  d->init();
}

//-----------------------------------------------------------------------------
qAutoSegmentSlicerAppMainWindow::qAutoSegmentSlicerAppMainWindow(
  qAutoSegmentSlicerAppMainWindowPrivate* pimpl, QWidget* windowParent)
  : Superclass(pimpl, windowParent)
{
  // init() is called by derived class.
}

//-----------------------------------------------------------------------------
qAutoSegmentSlicerAppMainWindow::~qAutoSegmentSlicerAppMainWindow()
{
}

//-----------------------------------------------------------------------------
void qAutoSegmentSlicerAppMainWindow::showEvent(QShowEvent* event)
{
  this->Superclass::showEvent(event);
  // On first run (no saved layout), apply standard Slicer UI: conventional layout + Welcome module
  QTimer::singleShot(0, this, [this]()
  {
    qSlicerLayoutManager* layoutManager = qSlicerApplication::application()->layoutManager();
    if (!layoutManager)
    {
      return;
    }
    if (layoutManager->layout() == vtkMRMLLayoutNode::SlicerLayoutInitialView)
    {
      layoutManager->setLayout(vtkMRMLLayoutNode::SlicerLayoutConventionalView);
      QSettings settings;
      if (settings.value("Modules/HomeModule").toString().isEmpty())
      {
        settings.setValue("Modules/HomeModule", QString("Welcome"));
        this->setHomeModuleCurrent();
      }
    }
  });
}

//-----------------------------------------------------------------------------
void qAutoSegmentSlicerAppMainWindow::on_HelpAboutAutoSegmentSlicerAppAction_triggered()
{
  qSlicerAboutDialog about(this);
  about.setLogo(QPixmap(":/Logo.png"));
  about.exec();
}
