<cfsilent>
	<cfscript>
		myQuery = QueryNew("Department,Dept_ID,Section,Section_ID,Image");
		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Accounting");
		QuerySetCell(myQuery, "Dept_ID", 1);
		QuerySetCell(myQuery, "Section", "The Budget");
		QuerySetCell(myQuery, "Section_id", 2);
		QuerySetCell(myQuery, "Image", "");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Accounting");
		QuerySetCell(myQuery, "Dept_ID", 1);
		QuerySetCell(myQuery, "Section", "Calculator");
		QuerySetCell(myQuery, "Section_id", 3);
		QuerySetCell(myQuery, "Image", "");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Accounting");
		QuerySetCell(myQuery, "Dept_ID", 1);
		QuerySetCell(myQuery, "Section", "Checkbook");
		QuerySetCell(myQuery, "Section_id", 4);
		QuerySetCell(myQuery, "Image", "");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "IT");
		QuerySetCell(myQuery, "Dept_ID", 2);
		QuerySetCell(myQuery, "Section", "CDs");
		QuerySetCell(myQuery, "Section_id", 5);
		QuerySetCell(myQuery, "Image", "cd");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "IT");
		QuerySetCell(myQuery, "Dept_ID", 2);
		QuerySetCell(myQuery, "Section", "Floppies (yea right)");
		QuerySetCell(myQuery, "Section_id", 6);
		QuerySetCell(myQuery, "Image", "floppy");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "IT");
		QuerySetCell(myQuery, "Dept_ID", 2);
		QuerySetCell(myQuery, "Section", "Serial Numbers");
		QuerySetCell(myQuery, "Section_id", 7);
		QuerySetCell(myQuery, "Image", "document");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Human Resources");
		QuerySetCell(myQuery, "Dept_ID", 3);
		QuerySetCell(myQuery, "Section", "Personnel List");
		QuerySetCell(myQuery, "Section_id", 9);
		QuerySetCell(myQuery, "Image", "");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Human Resources");
		QuerySetCell(myQuery, "Dept_ID", 3);
		QuerySetCell(myQuery, "Section", "Contacts");
		QuerySetCell(myQuery, "Section_id", 8);
		QuerySetCell(myQuery, "Image", "");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Human Resources");
		QuerySetCell(myQuery, "Dept_ID", 3);
		QuerySetCell(myQuery, "Section", "Forms");
		QuerySetCell(myQuery, "Section_id", 10);
		QuerySetCell(myQuery, "Image", "");

	</cfscript>
</cfsilent>
<html>
<head>
	<title>Dynamic CFTREE</title>
	<style type="text/css">
	body {font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;}
	</style>
</head>
<body>
	<cfform>
		<cftree format="html" name="dynamicTree">
	        <cftreeitem
	            query="myQuery"
	            value="Dept_ID,Section_ID"
	            display="Department,Section"
				queryasroot="NO"
				img="folder,document"
				href="dynamic.cfm?parent=1,dynamic.cfm"
			/>
		</cftree>

	</cfform>
</body>
</html>