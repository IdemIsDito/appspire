$('document').ready(function(){
	var cloudSettings = {
		"size" : {
			"grid" : 16
		},
		"options" : {
			"color" : "random-dark",
			"printMultiplier" : 3
		},
		"font" : "Futura, Helvetica, sans-serif",
		"shape" : "square"
	};
	$('form').on('submit', function(e) {
		e.preventDefault();

		var $this = $(this),
			$button = $this.find('button'),
			$wordcloud = $this.next('.wordcloud');
			url = $this.attr('action'),
			args = $this.serialize();

		$button.button('loading');
		$wordcloud.empty();

		$.getJSON(url, args, function(data) {
			$button.button('reset');
			$.each(data, function(k, v) {
				$wordcloud.append(
					$('<span/>', {
						'data-weight': v,
						'text': k
					})
				);
			});
			$wordcloud.awesomeCloud(cloudSettings);
		});
	});
});