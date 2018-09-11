<!--- 
http://stackoverflow.com/questions/9220172/using-jquery-ajax-json-format-how-do-you-output-a-query-from-a-cfm-page-to-the

JSON = "JavaScript Object Notation"
--->

<!---
CFC is learncf_jquery.cfc
test.cfm output looks like: {"COLUMNS":["TEAM"],"DATA":[["Dallas Cowboys"],["NY Giants"],["Philadelphia Eagles"],["Washington Redskins"]]}
--->

<!---
A somewhat similar tutorial on reading in the contents of an XML file, 
http://www.lynda.com/CSS-tutorials/Retrieving-displaying-XML-data/133326/145990-4.html, 
Retrieving and Displaying XML Data, Joseph Lowery, Working with Data on the Web
--->


<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>jQuery-json-cfm</title>

<!---AJAX via jQuery--->
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    <script type="text/javascript"> 
    $(document).ready(function(){ 

    $("#runQuery").click(function () {

        $.ajax({
            type: "GET",
            url: "test.cfm",
            dataType: "json",
            success: function (resp, textStatus, jqXHR) {
                buildResultsTable(resp);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert(errorThrown); 
            }
        });
    });


    function buildResultsTable(resp)
    {
        var output = $("<tr />");
        var j = 0;

            $("#results").html(""); 

            for (var i = 0; i < resp["COLUMNS"].length; i++)
            {
                var tmp_th = $("<th />");   
                tmp_th.text(resp["COLUMNS"][i]);
                output.append(tmp_th);
            }
            $("#results").append(output);

            for (j = 0; j < resp["DATA"].length; j++)
            {
                output = $("<tr />");

                for (var i = 0; i < resp["DATA"][j].length; i++)
                {
                    var tmp_td = $("<td />");   
                    tmp_td.text(resp["DATA"][j][i]);
                    output.append(tmp_td);
                }
                $("#results").append(output);
            }

    }

    })
    </script>

</head>

<body>

<h1>jQuery-json-cfm</h1>

<p>Source: <a href="http://stackoverflow.com/questions/9220172/using-jquery-ajax-json-format-how-do-you-output-a-query-from-a-cfm-page-to-the">http://stackoverflow.com/questions/9220172/using-jquery-ajax-json-format-how-do-you-output-a-query-from-a-cfm-page-to-the</a></p>


    <input type="button" id="runQuery" value="Show Teams" />
    <input type="text" name="name">


<p>&nbsp;</p>

<table id="results" cellspacing="0" cellpadding="0" border="1">

</table>


</body>
</html>