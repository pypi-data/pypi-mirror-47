# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/noplay/code/gns3/gns3-gui/gns3/ui/new_appliance_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewApplianceDialog(object):

    def setupUi(self, NewApplianceDialog):
        NewApplianceDialog.setObjectName("NewApplianceDialog")
        NewApplianceDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        NewApplianceDialog.resize(458, 317)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewApplianceDialog.sizePolicy().hasHeightForWidth())
        NewApplianceDialog.setSizePolicy(sizePolicy)
        NewApplianceDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewApplianceDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiImportApplianceTemplatePushButton = QtWidgets.QPushButton(NewApplianceDialog)
        self.uiImportApplianceTemplatePushButton.setObjectName("uiImportApplianceTemplatePushButton")
        self.verticalLayout.addWidget(self.uiImportApplianceTemplatePushButton)
        self.label = QtWidgets.QLabel(NewApplianceDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.uiAddIOSRouterRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddIOSRouterRadioButton.setObjectName("uiAddIOSRouterRadioButton")
        self.verticalLayout.addWidget(self.uiAddIOSRouterRadioButton)
        self.uiAddIOUDeviceRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddIOUDeviceRadioButton.setObjectName("uiAddIOUDeviceRadioButton")
        self.verticalLayout.addWidget(self.uiAddIOUDeviceRadioButton)
        self.uiAddQemuVMRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddQemuVMRadioButton.setObjectName("uiAddQemuVMRadioButton")
        self.verticalLayout.addWidget(self.uiAddQemuVMRadioButton)
        self.uiAddVirtualBoxVMRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddVirtualBoxVMRadioButton.setObjectName("uiAddVirtualBoxVMRadioButton")
        self.verticalLayout.addWidget(self.uiAddVirtualBoxVMRadioButton)
        self.uiAddVMwareVMRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddVMwareVMRadioButton.setObjectName("uiAddVMwareVMRadioButton")
        self.verticalLayout.addWidget(self.uiAddVMwareVMRadioButton)
        self.uiAddDockerVMRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddDockerVMRadioButton.setObjectName("uiAddDockerVMRadioButton")
        self.verticalLayout.addWidget(self.uiAddDockerVMRadioButton)
        self.uiAddVPCSRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddVPCSRadioButton.setObjectName("uiAddVPCSRadioButton")
        self.verticalLayout.addWidget(self.uiAddVPCSRadioButton)
        self.uiAddCloudRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddCloudRadioButton.setObjectName("uiAddCloudRadioButton")
        self.verticalLayout.addWidget(self.uiAddCloudRadioButton)
        self.uiAddEthernetHubRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddEthernetHubRadioButton.setObjectName("uiAddEthernetHubRadioButton")
        self.verticalLayout.addWidget(self.uiAddEthernetHubRadioButton)
        self.uiAddEthernetSwitchRadioButton = QtWidgets.QRadioButton(NewApplianceDialog)
        self.uiAddEthernetSwitchRadioButton.setObjectName("uiAddEthernetSwitchRadioButton")
        self.verticalLayout.addWidget(self.uiAddEthernetSwitchRadioButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.uiButtonBox = QtWidgets.QDialogButtonBox(NewApplianceDialog)
        self.uiButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.uiButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Help | QtWidgets.QDialogButtonBox.Ok)
        self.uiButtonBox.setObjectName("uiButtonBox")
        self.horizontalLayout.addWidget(self.uiButtonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewApplianceDialog)
        QtCore.QMetaObject.connectSlotsByName(NewApplianceDialog)

    def retranslateUi(self, NewApplianceDialog):
        _translate = QtCore.QCoreApplication.translate
        NewApplianceDialog.setWindowTitle(_translate("NewApplianceDialog", "New appliance template"))
        self.uiImportApplianceTemplatePushButton.setText(_translate("NewApplianceDialog", "Import an appliance template file"))
        self.label.setText(_translate("NewApplianceDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:x-large; font-weight:600;\">OR</span></p></body></html>"))
        self.uiAddIOSRouterRadioButton.setText(_translate("NewApplianceDialog", "&Add an IOS router using a real IOS image (supported by Dynamips)"))
        self.uiAddIOUDeviceRadioButton.setText(_translate("NewApplianceDialog", "&Add an IOU (IOS on UNIX) device using a L3 or L2 IOU image"))
        self.uiAddQemuVMRadioButton.setText(_translate("NewApplianceDialog", "&Add a Qemu virtual machine"))
        self.uiAddVirtualBoxVMRadioButton.setText(_translate("NewApplianceDialog", "&Add a VirtualBox virtual machine"))
        self.uiAddVMwareVMRadioButton.setText(_translate("NewApplianceDialog", "&Add a VMware virtual machine"))
        self.uiAddDockerVMRadioButton.setText(_translate("NewApplianceDialog", "&Add a Docker container"))
        self.uiAddVPCSRadioButton.setText(_translate("NewApplianceDialog", "Add a VPCS"))
        self.uiAddCloudRadioButton.setText(_translate("NewApplianceDialog", "Add a cloud"))
        self.uiAddEthernetHubRadioButton.setText(_translate("NewApplianceDialog", "Add a generic ethernet hub"))
        self.uiAddEthernetSwitchRadioButton.setText(_translate("NewApplianceDialog", "Add a generic ethernet switch"))

from . import resources_rc
