$(function(){

	function numberWithCommas(x) {
    	return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}

	$("#id_quantity").on("change",function(){
		var price = parseInt($('#total_price_detail').attr("price"))
		var total = price*$(this).val();
		$('#total_price_detail').text(numberWithCommas(total));

	});
});