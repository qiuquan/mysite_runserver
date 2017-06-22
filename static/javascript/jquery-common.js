// $(document).ready(function(){
//     //注册函数
//     var id_username = $("#id_username");
//     var id_password = $("#id_password");
//     var id_password_yz = $("#id_password_yz");
//     var id_email = $("#id_email");
//     var submit = $(".submit");

//     //检查用户名
//     id_username.blur(function ()
//      {
//         $('.name_tip').remove();
//         if (id_username.val().length < 3)
//             {
//                 id_username.after('<p class="name_tip tip">用户名长度小于3位</p>');
//                 // submit.attr("disabled",true);
//             }
//         else {
//             var input_name = id_username.val();
//             $.ajax({
//                 url:'/ajax_check_username/',
//                 type: 'POST',
//                 data: {username: input_name},
//                 success: function(arg){
//                     if (arg === input_name){
//                         id_username.after('<p class="name_tip tip">用户名已存在</p>')
//                      }
//                 }
//                 })
//             }

//     });

//     //检查密码
//     id_password.blur(function ()
//     {
//         $('.password_tip').remove();
//         if (id_password.val().length < 4)
//             {
//                 id_password.after('<p class="password_tip tip">密码长度小于4位</p>');
//             }

//     });
//     //第二次核对密码
//     id_password_yz.blur(function ()
//     {
//         $('.password_yz_tip').remove();
//         if (id_password_yz.val() !== id_password.val())
//             {
//                 id_password_yz.after('<p class="password_yz_tip tip">两次密码不一致</p>');
//             }

//     });
// //last
// });

$(document).ready(function() {
	var go_top = $(".go-top");
	var feedback = $(".feedback");
	var feedback_box = $('.feedback-box');
	var feedback_button = $("#feedback-button")

	go_top.mousemove(function() {
		go_top.html('回到<br>顶部');
		go_top.css({
			'background-image': '',
			'background-color': '#188eee',
			'color': '#fff',
		});
	});
	go_top.mouseout(function() {
		go_top.text('');
		go_top.css({
			'background-color': '',
			'background-image': 'url(../../static/images/icon/top.png)',
		});
	});

	$(window).scroll(function() { //bom 操作，当浏览器窗口滑动的时候。
		var feedback_top = feedback.offset().top
		if (feedback_top < 600) {
			go_top.hide();
		} else {
			go_top.show();
		}
	});

	go_top.click(function() {
		$('body,html').animate({
			scrollTop: '0'
		}, 'fast');
	});

	feedback_box_handel();

	function feedback_box_handel() {
		feedback.bind({
			mouseover: function() {
				feedback.html('我要<br>反馈');
				feedback.css({
					'background-image': '',
					'background-color': '#188eee',
					'color': '#fff'
				});
			},
			mouseout: function() {
				feedback.text('');
				feedback.css({
					'background-color': '',
					'background-image': 'url(../../static/images/icon/feedback.png)'
				});
			}
		});

		feedback.click(function() {
			if (feedback_box.css('display') === 'none') {
				// alert(feedback_box.css('display'));
				feedback.unbind("mouseover mouseout");
				feedback.html('点击<br>关闭')
			} else {
				// alert(feedback_box.css('display'))
				feedback.bind({
					mouseover: function() {
						feedback.html('我要<br>反馈');
						feedback.css({
							'background-image': '',
							'background-color': '#188eee',
							'color': '#fff'
						});
					},
					mouseout: function() {
						feedback.text('');
						feedback.css({
							'background-color': '',
							'background-image': 'url(../../static/images/icon/feedback.png)'
						});
					}
				});
			};
			feedback_box.toggle("normal")
		});
	};

	feedback_button.click(function() {
		var feedback_content = $('#problem');
		var feedback_contact = $('#contact');
		$.ajax({
			url: '/ajax_feedback/',
			type: 'POST',
			data: {
				feedback_content: feedback_content.val(),
				feedback_contact: feedback_contact.val()
			},
			success: function(msg) {
				if (msg === 'True') {
					alert('您的反馈提交成功，谢谢！');
					feedback_content.val('');
					feedback_contact.val('');
					// feedback_box.hide('normal');
				} else {
					alert('请输入要反馈的内容或者关闭反馈框');
				}
			}
		});

	});
	//last
});