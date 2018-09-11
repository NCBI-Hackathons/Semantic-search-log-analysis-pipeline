<cfsilent>

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
	        <cftreeitem bind="cfc:treefeeder.getSections({cftreeitemvalue},{cftreeitempath})" />
		</cftree>

	</cfform>
</body>
</html>