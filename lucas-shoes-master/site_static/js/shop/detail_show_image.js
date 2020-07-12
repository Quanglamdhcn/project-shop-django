$(function(){
	$('#show_image').on('click','.click_image', function(){
		var new_image = $(this).attr("data-src");
		$('.js_re').each(function(){
			$(this).css('border','');
		});
		$(this).closest('.br-product__thumb').css('border','3px solid #2bb5d6')
		$('.photo_large').attr("src",new_image);
	});
});