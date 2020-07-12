$(function(){
	$('#product_table_list').on('click','.delete_product',function(){
		$.ajax({
			url: $(this).attr('data-href'),
			dataTpe: "json",
			type: "get",
			success : function(data){
				$('#product_table_list').html(data.product_table_list);
			}
		});
	});

	$('#product_table_list').on('click','.js-thumbnai', function(){
		$("div.br-product-nav__item").removeClass("slick-current");
		$(this).closest("div.br-product-nav__item").addClass("slick-current");
		var elRep = '.js-replace'+$(this).attr("data-rep");
		$(elRep).attr("src",$(this).attr("src"));
	});

	$('#product_table_list').on('click','.js_add_cart', function(){
		$(this).closest('form').submit();
	});
});