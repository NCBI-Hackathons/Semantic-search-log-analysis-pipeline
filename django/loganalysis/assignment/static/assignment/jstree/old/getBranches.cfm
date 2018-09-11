
<cfscript>
//START-UP ----------------------------------------------------------------------------------
  //Make URLs work when page is renamed during testing
  variables.selfurl = GetFileFromPath(GetCurrentTemplatePath());
  variables.CurrentPage=GetFileFromPath(GetBaseTemplatePath());

  variables.filter = CreateObject("component", "cfc.filter");
  filter.init();
  WriteDump(var=filter.getVariables().filters, label="Filters", expand="no"); 
  variables.meshTree = CreateObject("component", "cfc.meshTree");

//Info about the data set we're working with

variables.qBranchM = meshTree.getBranchM(filter);
</cfscript>

<cfcontent type="application/json" reset="yes">
  <cfoutput>#SerializeJSON(qBranchM)#</cfoutput>
  <cfabort>

