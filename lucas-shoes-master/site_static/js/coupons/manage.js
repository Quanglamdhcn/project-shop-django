$(function(){

			$('#create_coupon').click(function(){

				$.ajax({
					url: $(this).attr('data-href'),
					type: 'get',
					dataType: 'json',
					success: function(data){
						$('.js_include_form').html(data.form);
					}
				});

			});
			$('#js-cancel').click(function(){
				$('form#js_add_item_form').hide();
				$('#create_coupon').show();
			});

			var check_empty = function(){
				$('small.empty').hide();
				var els = ['id_valid_form','id_valid_to','id_code','id_city','id_discount'];
				
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
			var show_error = function(data){
				if (!$('#id_code').val()) {
						$('.id_code').html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
					} else{
						$('.id_code').html('<small class="form-text text-muted empty" style="color:#ff0505;">'+data.er_code+'</small>');
					};
					if (!$('#id_valid_form').val()) {
						$('.id_valid_form').html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
					} else{
						$('.id_valid_form').html('<small class="form-text text-muted empty" style="color:#ff0505;">'+data.er_valid_form+'</small>');
					};
					if (!$('#id_valid_to').val()) {
						$('.id_valid_to').html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
					} else{
						$('.id_valid_to').html('<small class="form-text text-muted empty" style="color:#ff0505;">'+data.er_valid_to+'</small>');
					};
					if (!$('#id_discount').val()) {
						$('.id_discount').html('<small class="form-text text-muted empty" style="color:#ff0505;">Trường này là bắt buộc</small>')
					} else{
						$('.id_discount').html('<small class="form-text text-muted empty" style="color:#ff0505;">'+data.er_discount+'</small>');
					}
			};

			// add item
			$('.js_include_form').on('submit','#js_add_item_form', function(){

				check_empty();

				var $el = $(this);
				$.ajax({
					url: $(this).attr("action"),
					dataType: "json",
					type: 'post',
					data: $(this).serialize(),
					success : function(data){
						if (data.error){
							show_error(data);
						} else {
							$('#coupons').html(data.tbody);
							$el.hide();
							$('#create_coupon').show();
							
						}
					}
				});

				return false;
			});

			// Delete 1 item
			$('#coupons').on('click','.js-delete', function(){
				$.ajax({
					url: $(this).attr('data-href'),
					dataType:'json',
					type:'get',
					success: function(data){
						$('#coupons').html(data.tbody);
					}
				})
				return false;
			});	

			// edit item
			$('#coupons').on('click','.js-edit', function(){

				$.ajax({
					url: $(this).attr("data-href"),
					dataType:'json',
					type:'get',
					success: function(data){
						$('.js_include_form').html(data.coupon_update_form);

					}
				});

				return false;
			});

			$('.js_include_form').on('submit','#js_update_item_form', function(){
				check_empty();

				$.ajax({
					url: $(this).attr("data-href"),
					type:'post',
					dataType: 'json',
					data: $(this).serialize(),
					success: function(data){
						if (data.error){
							show_error(data);
						} else {
							$('#coupons').html(data.tbody);
							$('#js_update_item_form').hide();
						}

					}
				});

				return false;
			});

			$('.js_include_form').on('click', '#js-cancel', function(data){
				$(this).closest('form').hide();
			});

			// delete all item
			$('.js_delte_all_item').click(function(){
				$.ajax({
					url: $(this).attr('data-href'),
					type: 'get',
					dataType: 'json',
					success: function(data){
						$('#coupons').html(data.tbody);
					}
				});
			});

		});