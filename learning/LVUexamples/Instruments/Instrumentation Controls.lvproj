<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Autosetup.vi" Type="VI" URL="../Autosetup.vi"/>
		<Item Name="Dual output square wave 180 out of phase.vi" Type="VI" URL="../Dual output square wave 180 out of phase.vi"/>
		<Item Name="Instrumentation Controls.vi" Type="VI" URL="../Instrumentation Controls.vi"/>
		<Item Name="Multiple test points on oscilliscope.vi" Type="VI" URL="../Multiple test points on oscilliscope.vi"/>
		<Item Name="Read (Single _mod).vi" Type="VI" URL="../Read (Single _mod).vi"/>
		<Item Name="RIGOL DS1000 Series Acquire Continuous Waveform.vi" Type="VI" URL="../RIGOL DS1000 Series Acquire Continuous Waveform.vi"/>
		<Item Name="Rigol_Scope_Configure.vi" Type="VI" URL="../Rigol_Scope_Configure.vi"/>
		<Item Name="ScopeTest.vi" Type="VI" URL="../ScopeTest.vi"/>
		<Item Name="Single test point on oscilliscope.vi" Type="VI" URL="../Single test point on oscilliscope.vi"/>
		<Item Name="Voltage measurment on multimeter.vi" Type="VI" URL="../Voltage measurment on multimeter.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="instr.lib" Type="Folder">
				<Item Name="Close.vi" Type="VI" URL="/&lt;instrlib&gt;/RIGOL DM3058/Public/Close.vi"/>
				<Item Name="Configure Measurement.vi" Type="VI" URL="/&lt;instrlib&gt;/RIGOL DM3058/Public/Configure/Configure Measurement.vi"/>
				<Item Name="Initialize.vi" Type="VI" URL="/&lt;instrlib&gt;/RIGOL DM3058/Public/Initialize.vi"/>
				<Item Name="Read Single Point.vi" Type="VI" URL="/&lt;instrlib&gt;/RIGOL DM3058/Public/Data/Read Single Point.vi"/>
				<Item Name="RIGOL DG4000 Series.lvlib" Type="Library" URL="/&lt;instrlib&gt;/RIGOL DG4000 Series/RIGOL DG4000 Series.lvlib"/>
				<Item Name="RIGOL DS1000 Series.lvlib" Type="Library" URL="/&lt;instrlib&gt;/RIGOL DS1000 Series/RIGOL DS1000 Series.lvlib"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Binary to Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDT.llb/Binary to Digital.vi"/>
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="Check for Equality.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/Check for Equality.vi"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Close File+.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Close File+.vi"/>
				<Item Name="compatCalcOffset.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatCalcOffset.vi"/>
				<Item Name="compatFileDialog.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatFileDialog.vi"/>
				<Item Name="compatOpenFileOperation.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatOpenFileOperation.vi"/>
				<Item Name="compatWriteText.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatWriteText.vi"/>
				<Item Name="Compress Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDT.llb/Compress Digital.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="DTbl Binary U8 to Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DTblOps.llb/DTbl Binary U8 to Digital.vi"/>
				<Item Name="DTbl Binary U16 to Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DTblOps.llb/DTbl Binary U16 to Digital.vi"/>
				<Item Name="DTbl Binary U32 to Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DTblOps.llb/DTbl Binary U32 to Digital.vi"/>
				<Item Name="DTbl Compress Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DTblOps.llb/DTbl Compress Digital.vi"/>
				<Item Name="DTbl Digital Size.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DTblOps.llb/DTbl Digital Size.vi"/>
				<Item Name="DU64_U32SubtractWithBorrow.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/TSOps.llb/DU64_U32SubtractWithBorrow.vi"/>
				<Item Name="DWDT Binary U8 to Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDTOps.llb/DWDT Binary U8 to Digital.vi"/>
				<Item Name="DWDT Binary U16 to Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDTOps.llb/DWDT Binary U16 to Digital.vi"/>
				<Item Name="DWDT Binary U32 to Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDTOps.llb/DWDT Binary U32 to Digital.vi"/>
				<Item Name="DWDT Compress Digital.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDTOps.llb/DWDT Compress Digital.vi"/>
				<Item Name="DWDT Digital Size.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDTOps.llb/DWDT Digital Size.vi"/>
				<Item Name="DWDT Get Waveform Time Array.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDTOps.llb/DWDT Get Waveform Time Array.vi"/>
				<Item Name="Dynamic To Waveform Array.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/transition.llb/Dynamic To Waveform Array.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="ex_CorrectErrorChain.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_CorrectErrorChain.vi"/>
				<Item Name="ex_Modify Signal Name.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_Modify Signal Name.vi"/>
				<Item Name="ex_Modify Signals Names.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_Modify Signals Names.vi"/>
				<Item Name="Export Waveform To Spreadsheet File.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTFileIO.llb/Export Waveform To Spreadsheet File.vi"/>
				<Item Name="Export Waveforms To Spreadsheet File (1D).vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTFileIO.llb/Export Waveforms To Spreadsheet File (1D).vi"/>
				<Item Name="Export Waveforms To Spreadsheet File (2D).vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTFileIO.llb/Export Waveforms To Spreadsheet File (2D).vi"/>
				<Item Name="Export Waveforms To Spreadsheet File (Digital).vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTFileIO.llb/Export Waveforms To Spreadsheet File (Digital).vi"/>
				<Item Name="Export Waveforms to Spreadsheet File.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTFileIO.llb/Export Waveforms to Spreadsheet File.vi"/>
				<Item Name="Express Cycle RMS.vi" Type="VI" URL="/&lt;vilib&gt;/express/express analysis/AmpandLevelConfig.llb/Express Cycle RMS.vi"/>
				<Item Name="Express DC-RMS.vi" Type="VI" URL="/&lt;vilib&gt;/express/express analysis/AmpandLevelBlock.llb/Express DC-RMS.vi"/>
				<Item Name="Express Voltage Measurements.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/Express Voltage Measurements.vi"/>
				<Item Name="Find First Error.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find First Error.vi"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="General Error Handler Core CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler Core CORE.vi"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="Get Waveform Time Array.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/Get Waveform Time Array.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="I128 Timestamp.ctl" Type="VI" URL="/&lt;vilib&gt;/Waveform/TSOps.llb/I128 Timestamp.ctl"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="LVRectTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVRectTypeDef.ctl"/>
				<Item Name="Move t0 to the end.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/transition.llb/Move t0 to the end.vi"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="NI_AALPro.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALPro.lvlib"/>
				<Item Name="NI_MABase.lvlib" Type="Library" URL="/&lt;vilib&gt;/measure/NI_MABase.lvlib"/>
				<Item Name="NI_MAPro.lvlib" Type="Library" URL="/&lt;vilib&gt;/measure/NI_MAPro.lvlib"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="Number of Waveform Samples.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/Number of Waveform Samples.vi"/>
				<Item Name="Open_Create_Replace File.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/Open_Create_Replace File.vi"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
				<Item Name="subAmplitudeMeasure.vi" Type="VI" URL="/&lt;vilib&gt;/express/express analysis/AmpandLevelBlock.llb/subAmplitudeMeasure.vi"/>
				<Item Name="subPulseMeasurements.vi" Type="VI" URL="/&lt;vilib&gt;/express/express analysis/Timing-TransBlock.llb/subPulseMeasurements.vi"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="Timestamp Subtract.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/TSOps.llb/Timestamp Subtract.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="Waveform Array To Dynamic.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/transition.llb/Waveform Array To Dynamic.vi"/>
				<Item Name="Waveform Min Max.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/Waveform Min Max.vi"/>
				<Item Name="Waveform Time to Date Time String.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTFileIO.llb/Waveform Time to Date Time String.vi"/>
				<Item Name="WDT Get Waveform Time Array DBL.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Get Waveform Time Array DBL.vi"/>
				<Item Name="WDT Number of Waveform Samples CDB.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Number of Waveform Samples CDB.vi"/>
				<Item Name="WDT Number of Waveform Samples DBL.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Number of Waveform Samples DBL.vi"/>
				<Item Name="WDT Number of Waveform Samples EXT.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Number of Waveform Samples EXT.vi"/>
				<Item Name="WDT Number of Waveform Samples I8.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Number of Waveform Samples I8.vi"/>
				<Item Name="WDT Number of Waveform Samples I16.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Number of Waveform Samples I16.vi"/>
				<Item Name="WDT Number of Waveform Samples I32.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Number of Waveform Samples I32.vi"/>
				<Item Name="WDT Number of Waveform Samples SGL.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/WDT Number of Waveform Samples SGL.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="Write File+ (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write File+ (string).vi"/>
			</Item>
			<Item Name="Dual output square wave 180 out of phase.vi" Type="VI" URL="../../../LabViewProjects/Powerboard_Controller Test/Includes/Dual output square wave 180 out of phase.vi"/>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="Scope signal frame trim.vi" Type="VI" URL="../../../LabViewProjects/Powerboard_Controller Test/Includes/Scope signal frame trim.vi"/>
			<Item Name="ScopeConfigure.vi" Type="VI" URL="../../../LabViewProjects/Powerboard_Controller Test/Includes/ScopeConfigure.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Read(Single_mod)" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{D47FEA1B-0099-48A1-948E-BA805CD6CD45}</Property>
				<Property Name="App_INI_GUID" Type="Str">{2BC0CB26-F3EE-441C-A32E-212C32B9C605}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{40B3878D-6F90-4698-A57C-00B5320D1375}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Read(Single_mod)</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/NI_AB_PROJECTNAME/Read(Single_mod)</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{11E634F8-A6E0-4C91-9319-D7C58C797A92}</Property>
				<Property Name="Bld_version.build" Type="Int">1</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">Read(Single_mod).exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/Read(Single_mod)/Read(Single_mod).exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/Read(Single_mod)/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{5A2F0FEF-93B8-4B14-9C4B-2E2292E46F2C}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/Read (Single _mod).vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">ICON Health &amp; Fitness</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Read(Single_mod)</Property>
				<Property Name="TgtF_internalName" Type="Str">Read(Single_mod)</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2020 ICON Health &amp; Fitness</Property>
				<Property Name="TgtF_productName" Type="Str">Read(Single_mod)</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{80A0327E-B5A0-4074-970A-61BB7BA72242}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">Read(Single_mod).exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
			<Item Name="Rigol_Scope_Configure" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{EF828C8E-DFB5-44DB-98D6-633E272C8D5A}</Property>
				<Property Name="App_INI_GUID" Type="Str">{0F5D9600-27CE-4EB2-8194-DB3F317B6242}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{999EF86C-922A-4BAF-A96C-AC73712DB02B}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Rigol_Scope_Configure</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/NI_AB_PROJECTNAME/Rigol_Scope_Configure</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{C549BEB8-8C87-4942-976E-228630ECACB5}</Property>
				<Property Name="Bld_version.build" Type="Int">1</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">Rigol_Scope_Configure.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/Rigol_Scope_Configure/Rigol_Scope_Configure.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/Rigol_Scope_Configure/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{5A2F0FEF-93B8-4B14-9C4B-2E2292E46F2C}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/Rigol_Scope_Configure.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">ICON Health &amp; Fitness</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Rigol_Scope_Configure</Property>
				<Property Name="TgtF_internalName" Type="Str">Rigol_Scope_Configure</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2020 ICON Health &amp; Fitness</Property>
				<Property Name="TgtF_productName" Type="Str">Rigol_Scope_Configure</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{617BDBC7-28B7-499D-AF80-D5C6B09351A2}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">Rigol_Scope_Configure.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
		</Item>
	</Item>
</Project>
