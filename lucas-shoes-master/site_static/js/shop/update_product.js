$(function(){
	$('#id_name').on("change", function(){
	      var name = $("#id_name");
	      $.ajax({
	        url: name.attr("data-href"),
	        dataType: "json",
	        data: {
	          'name': name.val(),
	        },
	        type:'get',
	        success: function(data){
	          if (data.is_error) {
	            $('#ms_id_name').html('Sản phẩm đã được tạo xem'+data.msg).show();
	          } else {
	            $('#ms_id_name').html('');
	          }
	        }
	      })

	  });

	$("form").on('submit', function(){
		var form = $("#upload_product_form");
		if (!$("#id_name").val()) {
			$('#ms_id_name').show();
		} else{
			$('#ms_id_name').hide();
		}
		if (!$("#id_price").val()) {
			$("#ms_id_price").show();
		} else {
			$("#ms_id_price").hide();
		}

		$.ajax({
			url: form.attr("data-href"),
			type:form.attr("method"),
			dataType: "json",
			data: form.serialize(),
			success: function(data){
				if (data.is_error){
					 $("#ms_id_price").html(data.pricve_msg_error).show();
					 $('#show-msg-success').hide();
					 $('#show-msg-error').show().fadeOut(5000);
				} else {
					$('#show-msg-error').hide();
					$('#show-msg-success').show().fadeOut(5000);
					
				}
			}
		});

		return false;
	});

	$('.delete_image').click(function(){
		$.ajax({
			url: $(this).attr("data-href"),
			dataType: "json",
			type: "get",
			success: function(data){
				$("#show_image").html(data.photo_html);
			}
		})
	});
});