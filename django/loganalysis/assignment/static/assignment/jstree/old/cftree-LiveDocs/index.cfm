<!---
http://localhost:8500/_pubmed2015/mesh/cftree-LiveDocs/index.cfm

Adobe: Building tree controls with the cftree tag: 
http://help.adobe.com/en_US/ColdFusion/9.0/Developing/WSc3ff6d0ea77859461172e0811cbec22c24-7a86.html

See also:

Home / Developing ColdFusion 9 Applications / Requesting and Presenting Information / Building Dynamic Forms with cfform Tags
Building tree controls with the cftree tag
http://help.adobe.com/en_US/ColdFusion/9.0/Developing/WSc3ff6d0ea77859461172e0811cbec22c24-7a86.html



Home / ColdFusion 9 CFML Reference / ColdFusion Tags / Tags t
cftree
http://help.adobe.com/en_US/ColdFusion/9.0/CFMLRef/WSc3ff6d0ea77859461172e0811cbec22c24-7d84.html

 --->



<cfquery name="mesher" datasource="pubmed"> 
    select parentNumber, DescriptorName
    from mesh_tree
    where TreeNumber like 'A%'
    and not trLevel like '1'
    order by parentNumber
</cfquery> 
<!---
concat(DescriptorName, ' ', TreeNumber) as listItem
concat(parentName, ' ', parentNumber) as parent--->

<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MeSH tree for query analysis</title>
<link href="../../_styles/boilerplate.css" rel="stylesheet" type="text/css">
<link href="../../_styles/main.css" rel="stylesheet" type="text/css">
<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<script src="../_scripts/respond.min.js"></script>
<style type="text/css">
table, td, th, tr {
	border:none;
}

</style>

</head>

<body>

<div class="skipnavigation"><a class="skipnavigation" href="#skip" title="Skip the navigation on this page">Skip Navigation</a></div>

<div class="gridContainer clearfix">

  <div id="header">

    <div id="hgroup">
    <h1>PubMed Record Set Analyzer - home</h1>
  </div>
  
    <div id="siteNav">
  
      <h2>Site navigation</h2>
        
        <ul class="topMenu"><cfoutput>
            <li><a href="#request.cfg.applicationUrlPath()#index.cfm" title="Home">Home</a></li>
        </cfoutput></ul>  

  </div><!-- end #siteNav --> 
  
  </div><!--end header-->
  

  <div id="mainContent">
    <a id="skipnav" name="skip"></a>
  
  
      <h1>Browse the MeSH Tree</h1>  
  
<cfform name="form1" action="submit.cfm"> 

<cftree name="meshTree"
	format="html"
    required="Yes"
    appendkey="yes"
    width="400"> 
    
    <cftreeitem 
        query="mesher" 
        value="parentNumber,DescriptorName" 
        queryasroot="No"
        expand="no"
        img="folder,document"        
        > 
</cftree> 
<!---    border="no"
    hscroll="No"--->

</cfform>



<!---<cfdump var="#mesher#">--->


  </div><!-- end #mainContent --> 
  
  
  
  <div id="footer">

    <p>Updated January 11, 2014</p>
    <p>2008-2014 Daniel Wendling and authors</p>
  </div><!-- end #footer --> 
  
</div>

</body>
</html>


