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
		<Item Name="#include" Type="Folder" URL="../#include">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="main.vi" Type="VI" URL="../main.vi"/>
		<Item Name="test.vi" Type="VI" URL="../test.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Add File to Zip.vi" Type="VI" URL="/&lt;vilib&gt;/zip/Add File to Zip.vi"/>
				<Item Name="Adress_string_in_SS.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Adress_string_in_SS.vi"/>
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="Cell_style.ctl" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Gen_styles/Cell_style.ctl"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="CLAUDIE_xlsx.lvlib" Type="Library" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/CLAUDIE_xlsx.lvlib"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Close Zip File.vi" Type="VI" URL="/&lt;vilib&gt;/zip/Close Zip File.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Create Directory Recursive.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Create Directory Recursive.vi"/>
				<Item Name="Create_app_xml.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_app_xml.vi"/>
				<Item Name="Create_content_types.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_content_types.vi"/>
				<Item Name="Create_core_xml.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_core_xml.vi"/>
				<Item Name="Create_excel.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel.vi"/>
				<Item Name="Create_fills.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Formats/Create_fills.vi"/>
				<Item Name="Create_folder.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Process_folders_VIs/Create_folder.vi"/>
				<Item Name="Create_fonts.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Formats/Create_fonts.vi"/>
				<Item Name="Create_formate_strings.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Formats/Create_formate_strings.vi"/>
				<Item Name="Create_lists_loop.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_lists_loop.vi"/>
				<Item Name="Create_rels.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/_rels/Create_rels.vi"/>
				<Item Name="Create_shared_strings_xml.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_shared_strings_xml.vi"/>
				<Item Name="Create_sheet_xml.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_sheet_xml.vi"/>
				<Item Name="Create_string_list.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Create_string_list.vi"/>
				<Item Name="Create_styles.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Formats/Create_styles.vi"/>
				<Item Name="Create_styles_xml.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_styles_xml.vi"/>
				<Item Name="Create_workbook_xml.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Create_workbook_xml.vi"/>
				<Item Name="CreateZip.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Process_folders_VIs/CreateZip.vi"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="Doc_props.ctl" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Formats/Typedeffs/Doc_props.ctl"/>
				<Item Name="Err1_handler.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Errors/Err1_handler.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="ex_CorrectErrorChain.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_CorrectErrorChain.vi"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Font.ctl" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Gen_styles/Font.ctl"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="Gen_styles_main.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Gen_styles/Gen_styles_main.vi"/>
				<Item Name="General Error Handler Core CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler Core CORE.vi"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Generate_alph_adress.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/Generate_alph_adress.vi"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="Get_sheet_names.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/Get_sheet_names.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="i3-json.lvlib" Type="Library" URL="/&lt;vilib&gt;/LVH/i3 JSON/i3-json.lvlib"/>
				<Item Name="Is Path and Not Empty.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Is Path and Not Empty.vi"/>
				<Item Name="Is_num.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/Is_num.vi"/>
				<Item Name="Is_time_stamp.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/Is_time_stamp.vi"/>
				<Item Name="List Directory and LLBs.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/List Directory and LLBs.vi"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="LVRectTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVRectTypeDef.ctl"/>
				<Item Name="New Zip File.vi" Type="VI" URL="/&lt;vilib&gt;/zip/New Zip File.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="NI_Unzip.lvlib" Type="Library" URL="/&lt;vilib&gt;/zip/NI_Unzip.lvlib"/>
				<Item Name="NI_XML.lvlib" Type="Library" URL="/&lt;vilib&gt;/xml/NI_XML.lvlib"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="Parse_doc_properties.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Parse_doc_properties.vi"/>
				<Item Name="Parse_sheets.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Parse_sheets.vi"/>
				<Item Name="Parse_SS.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Parse_SS.vi"/>
				<Item Name="Parse_styles.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Parse_styles.vi"/>
				<Item Name="Parse_workbook.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Parse_workbook.vi"/>
				<Item Name="Path To Command Line String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Path To Command Line String.vi"/>
				<Item Name="PathToUNIXPathString.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/CFURL.llb/PathToUNIXPathString.vi"/>
				<Item Name="Process_path.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Process_folders_VIs/Process_path.vi"/>
				<Item Name="Process_shared_strings_sizes.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/Process_shared_strings_sizes.vi"/>
				<Item Name="ProcessFolder.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Process_folders_VIs/ProcessFolder.vi"/>
				<Item Name="Read_excel.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel.vi"/>
				<Item Name="Recursive File List.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Recursive File List.vi"/>
				<Item Name="Reform_num_to_form_string.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Formats/Reform_num_to_form_string.vi"/>
				<Item Name="Relative Path To Platform Independent String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Relative Path To Platform Independent String.vi"/>
				<Item Name="Rename_file.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Process_folders_VIs/Rename_file.vi"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="SharedStrings_string.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/SharedStrings_string.vi"/>
				<Item Name="Sheets_data.ctl" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Create_xmls/Sheets_data.ctl"/>
				<Item Name="Sheets_err.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Errors/Sheets_err.vi"/>
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
				<Item Name="SpreadSheet_string.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/SpreadSheet_string.vi"/>
				<Item Name="SS_err.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/Errors/SS_err.vi"/>
				<Item Name="String_modification.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Preprocess_Datas/String_modification.vi"/>
				<Item Name="Style.ctl" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Gen_styles/Style.ctl"/>
				<Item Name="Style_tables.ctl" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Create_excel/Gen_styles/Style_tables.ctl"/>
				<Item Name="subDisplayMessage.vi" Type="VI" URL="/&lt;vilib&gt;/express/express output/DisplayMessageBlock.llb/subDisplayMessage.vi"/>
				<Item Name="subFile Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/express/express input/FileDialogBlock.llb/subFile Dialog.vi"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="To_time_stamp.vi" Type="VI" URL="/&lt;vilib&gt;/ATEsystem/CLAUDIE_xlsx/aplikace/Read_excel/To_time_stamp.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
			</Item>
			<Item Name="DOMUserDefRef.dll" Type="Document" URL="DOMUserDefRef.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="focusKey_input.vi" Type="VI" URL="../../Motor_Controller/#include/focusKey_input.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
