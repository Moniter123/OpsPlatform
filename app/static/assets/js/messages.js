$(function(){
	$("#myAlert").bind('closed.bs.alert', function () {
		alert("提示消息框被关闭。");
	});
});
