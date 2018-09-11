<cfcomponent name="Tree Feeder" output="false">

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
		QuerySetCell(myQuery, "Section", "Contacts");
		QuerySetCell(myQuery, "Section_id", 8);
		QuerySetCell(myQuery, "Image", "");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Human Resources");
		QuerySetCell(myQuery, "Dept_ID", 3);
		QuerySetCell(myQuery, "Section", "Personnel List");
		QuerySetCell(myQuery, "Section_id", 9);
		QuerySetCell(myQuery, "Image", "");

		QueryAddRow(myQuery);
		QuerySetCell(myQuery, "Department", "Human Resources");
		QuerySetCell(myQuery, "Dept_ID", 3);
		QuerySetCell(myQuery, "Section", "Forms");
		QuerySetCell(myQuery, "Section_id", 10);
		QuerySetCell(myQuery, "Image", "");

	</cfscript>

	<cffunction name="getSections" output="false" returntype="array" access="remote">
		<cfargument name="cftreeitemvalue" type="string" required="true" hint="" />
		<cfargument name="cftreeitempath" type="string" required="true" hint="" />

		<!--- If no values are passed, return just the departments --->
		<cfif Arguments.cftreeitemvalue EQ "">

			<cfquery name="LOCAL.Sections" dbtype="query">
			SELECT DISTINCT Department, Dept_ID
			FROM myQuery
			ORDER BY Dept_ID
			</cfquery>

			<cfset LOCAL.ReturnValue = [] />
			<cfloop query="LOCAL.Sections">
				<cfset ArrayAppend(LOCAL.ReturnValue, {
					DISPLAY = Department
					, VALUE = Dept_ID
					, IMG = "folder"
					, IMGOPEN = "folder"
				}) />
			</cfloop>


		<cfelse>
			<!--- They're after a department, give them the sections --->
			<cfquery name="LOCAL.Sections" dbtype="query">
			SELECT DISTINCT [Section], Section_ID, Image
			FROM myQuery
			WHERE Dept_ID = <cfqueryparam cfsqltype="cf_sql_integer" value="#Arguments.cftreeitemvalue#" />
			ORDER BY Dept_ID, Section_ID
			</cfquery>

			<cfset LOCAL.ReturnValue = [] />
			<cfloop query="LOCAL.Sections">
				<cfset ArrayAppend(LOCAL.ReturnValue, {
					DISPLAY = Section
					, VALUE = Section_ID
					, LEAFNODE = True
					, IMG = Image
					, HREF = "cfctree.cfm"

				}) />
			</cfloop>

		</cfif>

		<cfreturn LOCAL.ReturnValue />

	</cffunction>
</cfcomponent>