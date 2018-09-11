   <cfinvoke 
   component="learncf_jquery" 
   method="getDataSetInfo" 
   returnVariable="getItems">
   </cfinvoke>

  <cfoutput>#SerializeJSON(getItems)#</cfoutput>
