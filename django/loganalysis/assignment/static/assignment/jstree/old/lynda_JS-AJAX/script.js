$.getJSON('data.json', function(data) {
	var output = '<ul>';
	$.each(data, function(key, val) {
		output += '<li>' + val.name + '</li>';
	});
	output +='</ul>';
	$('#update').append(output);
});


<!-- Troubleshooting tip:
// $.getJSON('data.json', function(data) {
//	 console.log(data);
// Then go to Chrome and Inspect Element > Console to see if the object made it to the browser
// });
 -->