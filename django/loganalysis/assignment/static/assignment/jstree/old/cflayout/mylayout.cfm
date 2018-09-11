<!--- I am building a query here but normally this would be a query against a categories table --->
<cfset getcategories = querynew("category_id,Name,ParentID")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","1")>
<cfset querysetcell(getcategories,"Name","Category1")>
<cfset querysetcell(getcategories,"ParentID","0")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","2")>
<cfset querysetcell(getcategories,"Name","Category2")>
<cfset querysetcell(getcategories,"ParentID","1")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","3")>
<cfset querysetcell(getcategories,"Name","Category3")>
<cfset querysetcell(getcategories,"ParentID","1")>
<cfset queryaddrow(getcategories)>
<cfset querysetcell(getcategories,"category_id","4")>
<cfset querysetcell(getcategories,"Name","Category4")>
<cfset querysetcell(getcategories,"ParentID","0")>



<!--- Here is where all the magic happens the trick was figuring out that the
   "value" attribute in the cftreeitem tag corresponds to the "id" property in the
   YAHOO.widget.TreeView.getNodeByProperty() function. That took some digging
   but I found it.   
--->
<script language="JavaScript">
function catTreeNodeSelection(catID){
   tree = ColdFusion.Tree.getTreeObject("categorytree");
   me = tree.getNodeByProperty('id',catID);
   me.parent.expand();
   me.tree.fireEvent("labelClick", me);
}
</script>



<!doctype html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Example</title>
</head>

<body>

<!--- cfajaximport is needed so the cftree will work withing the layoutarea --->
<cfajaximport tags="cftree">

<cflayout type="Border" name="toplevellayout" style="margin:0px;height:400px;">
<cflayoutarea
       position="left"
      name="treepanel"
      title="Document Categories"
      size="250"
      style="padding-top:3px;"
      overflow="auto"
      collapsible="false"
      splitter="true"
      minsize="200">
      
      <cfform>
         <cftree name = "categorytree" font = "Arial Narrow" italic="yes" completepath="no" format="html">
         <cftreeitem value="0" display="Show All Documents" parent="categorytree" imgopen="folder">
            <cfloop query="getcategories">
               <cftreeitem
                  value="#getcategories.category_id#"
                  display="#getcategories.name#"
                  parent="#getcategories.ParentID#"
                  img="folder"
                  imgopen="folder"
                  expand="no">
            </cfloop>
         </cftree>
      </cfform>
      
</cflayoutarea>
   
<cflayoutarea position="center" name="documentwindow" overflow="hidden">
          <!--- I'm using a URL binding on this cfdiv and passing the selected category
               tree node so that when a new node is selected the div content --->
<cfdiv bind="url:display.cfm?category_id={categorytree.node}"/>
</cflayoutarea>

</cflayout>

</body>
</html>
