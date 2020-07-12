$(function(){
	$("form#js-checkout").on('submit', function(){
		$('small.empty').hide();
		var els = ['id_last_name','id_first_name','id_email','id_city','id_phone','id_address'];
		
		for (var el in els){
			var em = '#'+els[el]
			var error = '.'+els[el]
			if (!$(em).val()){
				$(error).html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
			} else {
				$(error).html('');
			}
		};

		$.ajax({
			url: $('form#js-checkout').attr("data-href"),
			dataType:'json',
			type: 'post',
			data: $('form#js-checkout').serialize(),
			success: function(data){
				if (data.error){
					if (!$('#id_phone').val()) {
						$('.id_phone').html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
					} else{
						$('.id_phone').html('<small class="form-text text-muted empty" style="color:#ff0505;">'+data.error_phone+'</small>');
					}
					if (!$('#id_email').val()) {
						$('.id_email').html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
					} else{
						$('.id_email').html('<small class="form-text text-muted empty" style="color:#ff0505;">'+data.error_email+'</small>');
					}
			
				} else {
					$('main').html(data.msg_success);
				}
			}
		});

		return false;
	});

	

});