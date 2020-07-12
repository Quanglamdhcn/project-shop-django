$(function(){
	function numberWithCommas(x) {
    	return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}

	$('.js_remove_cart').click(function(){
		var $el = $(this);

		$.ajax({
			url: $(this).attr("data-href"),
			datType: 'json',
			type: 'get',
			success : function(data){
				$el.closest('div.product-mini').remove();
				$(".cart_count").text(data.total_item);
				$('#total_price').text(numberWithCommas(data.total_price)+" VNĐ");
			}
		});
	});
});