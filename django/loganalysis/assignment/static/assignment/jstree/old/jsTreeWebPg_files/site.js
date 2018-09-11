/* global jQuery, WR */
(function ($) {
	"use strict";
	$(function () {
		var search = function (str) {
				var tmp = str && str.length ? $.vakata.search(str, true, { threshold : 0.2, fuzzy : true, caseSensitive : false }) : null,
					res = $('#api_inner')
								.find('.item').hide()
								.filter(function () {
									return tmp ? tmp.search($(this).find('>h4>code').text()).isMatch : true;
								}).show().length;
				$('#api_inner').find('#no_res')[ !tmp || res ? 'hide' : 'show' ]();
				$('#api_inner').find('#cl_src')[ tmp && res ? 'show' : 'hide' ]();
				if(!$('#srch').is(':focus')) {
					$('#srch').val(str);
				}
				$(window).resize();
			},
			filter = function (str) {
				$('.item-inner').hide();
				if(str) {
					var i = $('.item[rel="'+str+'"]');
					if(!i.length) { i = $('.item[rel^="'+str+'"]'); }
					if(i && i.length) {
						i = i.eq(0);
						i.children('.item-inner').show().end();
						if(i.offset().top < $(document).scrollTop() || i.offset().top + i.height() > $(document).scrollTop() + $(window).height()) {
							i[0].scrollIntoView();
						}
					}
				}
			};

		var to1 = false;
		$(window).resize(function () {
			if(to1) { clearTimeout(to1); }
			to1 = setTimeout(function () {
				$('.page').css('minHeight','0px').css('minHeight', ($(document).height() - $('#head').outerHeight()) + 'px');
			},50);
		}).resize();

		$('#head form').on('submit', function (e) {
			e.preventDefault();
			document.location = WR + 'api/#/?q=' + $('#srch').val();
		});

		var container = $('#api_inner'), str;
		if(container.length) {
			var to2 = false, api;
			$('#srch').on('keyup', function () {
				if(to2) { clearTimeout(to2); }
				to2 = setTimeout(function () {
					var f = $.address.parameter('f'),
						q = $('#srch').val(),
						d = [];
					if(q && q.length) {
						d.push('q=' + q);
					}
					if(f && f.length && false) {
						d.push('f=' + f);
					}
					$.address.value('/' + (d.length ? '?' + d.join('&') : ''));
				}, 250);
			});
			
			api = $.getJSON(WR + 'jstree.json', function (data) {
				//return;
				$.each(data, function (ii, v) {
					if(v.description.full.indexOf('<p>lobals') === 0) { return true; }
					if(v.ignore) { return true; }
					var str = '', name, plugin, internal, params = [], retrn, priv = false, evnt = false, trig, i, j;
					for(i = 0, j = v.tags.length; i < j; i++) {
						switch(v.tags[i].type) {
							case "name":
								name = v.tags[i].string;
								break;
							case "private":
								priv = true;
								break;
							case "event":
								evnt = true;
								break;
							case "trigger":
								trig = v.tags[i].string;
								break;
							case 'plugin':
								plugin = v.tags[i].string;
								break;
							case 'return':
								retrn = '<ul class="params list-unstyled"><li><code class="param return">Returns</code><p><code class="type">' + v.tags[i].types.join('</code> <code class="type">') + '</code> ' + v.tags[i].description + '</p></li></ul>';

								break;
							case 'param':
								params.push('<code class="param">' + v.tags[i].name + '</code><p><code class="type">' + v.tags[i].types.join('</code> <code class="type">') + '</code> ' + v.tags[i].description + '</p>');
								break;
						}
					}
					str += '<div class="item '+(priv?'private':'')+'" rel="'+(name?name.replace('"',''):'')+'">';
					if(name) {
						if(name.indexOf('(') !== -1 && name.indexOf('$(') === -1) {
							name = name.split('(');
							name = '<strong>' + name[0] + '</strong> (' + name[1];
						}
						str += '<h4><code class="'+(name.indexOf('(') === -1 ? (evnt ? 'evnt' : 'prop') : 'func')+'">'+name+(evnt?' Event <i class="glyphicon glyphicon-flash"></i>' : '')+'</code>';
						if(plugin) { str += '<code class="meta plugin"><i class="glyphicon glyphicon-leaf"></i> '+plugin+' plugin</code> '; }
						if(priv) { str += '<code class="meta">private</code> '; }
						str += '</h4>';
					}
					str += '<div class="' + (name ? "item-inner" : "" ) + '">';
					str += '<div>'+ v.description.full +'</div>';
					if(params.length) {
						str += '<ul class="params list-unstyled">';
						for(var k = 0, l = params.length; k < l; k++) {
							str += '<li>' + params[k] + '</li>';
						}
						str += '</ul>';
					}
					if(retrn) {
						str += retrn;
					}
					if(trig) {
						str += '<ul class="params list-unstyled"><li><code class="param trigger">Triggers</code><p><code class="evnt">'+ trig.split(',').join('</code> <code class="evnt">')+'</code></p></li></ul>';
					}
					str += '</div>';
					str += '</div>';
					container.append(str);
				});

				$('#api h3').prepend('<i class="glyphicon glyphicon-leaf"></i>&nbsp;').closest('.item').css({ 'background' : 'white', 'border' : '0', 'borderRadius' : '0', /*'borderBottom' : '1px solid #8b0000', 'textAlign' : 'center',*/ 'marginTop' : '0', 'paddingTop' : '0' }).prev().css('marginBottom', '3em');

				$('.item > h4').on('click', function () {
					var r = $(this).parent().attr('rel');
					if(r && r.length) {
						var q = $.address.parameter('q');
						if($.address.parameter('f') === r) {
							$.address.value('/' + (q ? '?q=' + q : ''));
						}
						else {
							$.address.value('/?' + (q ? 'q=' + q + '&' : '') + 'f=' +  r);
						}
					}
					//$(this).next().slideToggle();
				});
				//$('.item > h4 > code').on('click', function () { $('#srch').val($(this).text().replace(' Event','')).keyup(); });

				container.find('pre').each(function () {
					var d = $('<div>'),
						p = $(this).closest('.item').find('.item-inner');
					$(this).prev().appendTo(d);
					$(this).appendTo(d);
					p.append(d);
				});

				if($('#srch').val().length) {
					search(decodeURIComponent($.address.parameter('q')));
				}
				filter(decodeURIComponent($.address.parameter('f')));
			});
			$.address
				.change(function(e) {
					api.done(function () {
						search($.address.parameter('q') ? decodeURIComponent($.address.parameter('q')) : '');
						filter($.address.parameter('f') ? decodeURIComponent($.address.parameter('f')) : '');
						$(window).resize();
					});
				});
		}
	});
}(jQuery));