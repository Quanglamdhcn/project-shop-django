$(function(){
	var check_empty = function(){
		$('small.empty').hide();
		var els = ['id_name','id_email','id_title','id_content'];
		
		for (var el in els){
			var em = '#'+els[el]
			var error = '.'+els[el]
			if (!$(em).val()){
				$(error).html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
			} else {
				$(error).html('');
			}
		};
	};

	$('form#js_contact').on('submit', function(){
		var $form = $(this);
		check_empty();

		$.ajax({
			url: $form.attr("data-href"),
			type:'post',
			dataType: 'json',
			data: $form.serialize(),
			success: function(data){
				if (data.error) {
					if (!$('#id_email').val()) {
						$('.id_email').html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
					} else{
						$('.id_email').html('<small class="form-text text-muted empty" style="color:#ff0505;">'+data.error_email+'</small>');
					};
				} else{
					$('#js_ms').show().fadeOut(10000);
					$form.each(function(){ 
					    this.reset();
					});
				}
			}
		});

		return false;
	});
});