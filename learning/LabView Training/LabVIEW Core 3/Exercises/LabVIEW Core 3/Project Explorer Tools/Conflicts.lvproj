<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="14008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Sine Wave" Type="Folder">
			<Item Name="Generate Signal.vi" Type="VI" URL="../Working Directory/Sine Wave/Generate Signal.vi"/>
		</Item>
		<Item Name="Square Wave" Type="Folder">
			<Item Name="Generate Signal.vi" Type="VI" URL="../Working Directory/Square Wave/Generate Signal.vi"/>
		</Item>
		<Item Name="File IO" Type="Folder">
			<Item Name="Log to File.vi" Type="VI" URL="../Working Directory/File IO/Log to File.vi"/>
		</Item>
		<Item Name="Create and Save Signal.vi" Type="VI" URL="../Working Directory/Create and Save Signal.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="NI_MABase.lvlib" Type="Library" URL="/&lt;vilib&gt;/measure/NI_MABase.lvlib"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
			</Item>
			<Item Name="Log to File.vi" Type="VI" URL="../Backup Directory/File IO/Log to File.vi"/>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
