$(document).ready(function() {

	function dateCompare (start,end=new Date()) {
	// body...
	var date1=new Date(start);
	var date2=new Date(end);
	if (date1<date2) {
		return true;
	} else {
		return false;
	}
}

// 还原输入框
function clearInput (id,form_id) {
	// body...
	$('#'+id).val('');
	$(this).popover('destroy');
	$('#'+form_id).attr("class","form_group")
};

// 重置注册的输入框
$("#regReset").click(function(){
	clearInput("regUsername");
	clearInput("password");
	clearInput("confirm");
})

//重置修改密码的输入框
$("#resetChangePsw").click(function(){
	clearInput("oldpsw");
	clearInput("newpsw");
	clearInput("confirm");
})

//检查是否为空
function isEmpty (id,form_id,message) {
	// body...
	var length=$("#"+id).val().length;
	if(length==0){
		$('#'+form_id).attr("class","form-group has-error");
		$('#'+id).attr("data-content",message);
		$('#'+id).popover({placement:'bottom'});
		$('#'+id).popover({trigger:'manual'});
		$('#'+id).popover('show');
		return true;
	} else {
		$('#'+id).popover('hide');
		$('#'+form_id).attr("class","form-group");
		return false;
	}
};


$("#mobilePhone").on('focus',function(){
	var l=$("#mobilePhone").val().length
	if (l!=11) {
		$('#mobilePhone').parent().attr("class","form-group has-error");
		$('#mobilePhone').attr("data-content",'请输入正确的手机号！');
		$('#mobilePhone').popover({placement:'bottom'});
		$('#mobilePhone').popover({trigger:'manual'});
		$('#mobilePhone').popover('show');
	};
})


$("#t_1").on('click',function(e){
	if(e.target.id=="deleteQualification"){
	// 删除证书
	var qno=$('[value='+e.target.value+']').parent().prev().prev().text();
	var row=$('[value='+e.target.value+']').parents('tr');
	$.get("../users/regtable/delQualification/?qualificationID="+qno,function(data,status){
		alert("删除证书成功！");
		row.remove();
		$("#qualiHead").attr('rowspan',parseInt($("#qualiHead").attr('rowspan'))-1);
		return;
	})
}
})

// 添加资格证书
$("#addQuali").click(function(){
	if (!isEmpty("qualiNo","qualiNoForm","请输入证书编号") & 
		!isEmpty("qualiName","qualiNameForm","请输入证书名称")) {
		// submit
	var qno=$("#qualiNo").val();
	var qname=$("#qualiName").val();
	$.get('../users/regtable/addQualification/?qualificationID='+qno+'&qualificationName='+qname,
		function  (data) {
				// body...
				if(data=='exist'){
					alert("证书已存在！");
					return;
				} else {
					alert("添加成功！");
					$("#qualiHead").attr('rowspan',parseInt($("#qualiHead").attr('rowspan'))+1);
					$("#qualiHeadRow").after(
						"<tr><td>"+qno+"</td><td>"+
						qname+"</td><td><button type='button' id='deleteQualification' value="+qno+
						" class='deleteQualification btn btn-default'>删除</button></td></tr>")
				}
				clearInput("qualiNo","qualiNoForm");
				clearInput("qualiName","qualiNameForm");
				$("#qualificationModal").modal('toggle');
				$("#qualificationModal").modal('hide');
				return;
			})
};
});

// 选择评审领域
$("#addAppraise").click(function  (argument) {
	// body...
	var length=$("#appraisefieldModal").find(".modal-body").find(":checked").length;
	if (length>2) {
		alert("最多选择两项！")
		return;
	};
	if (length<1) {
		alert("请选择至少一项！")
		return;
	};
	var one=$("#appraisefieldModal").find(".modal-body").find(":checked").first().attr("value");
	var two=$("#appraisefieldModal").find(".modal-body").find(":checked").last().attr("value");
	if (one == two) {
		two = '';
	};
	$.get("../users/regtable/addAppraiseField/?appraisefield1="+one+"&appraisefield2="+two,function  (data,status) {
		// body...
		if(data == "ok"){
			$("#field1").text(one);
			$("#field2").text(two);
			$("#appraisefieldModal").modal('toggle');
			$("#appraisefieldModal").modal('hide');			
		}
	})
})

// 增加评估/评审经历
$("#addAppraiseExp").click(function(){
	if (!isEmpty("appraiseTime","appraiseTimeForm","请输入评审时间") & 
		!isEmpty("appraiseName","appraiseNameForm","请输入评审任务名称") &
		!isEmpty("appraiseDesc","appraiseDescForm","请输入评审任务描述") &
		!isEmpty("appraiseType","appraiseTypeForm","请输入评审任务类型")) {

		var appTime=$("#appraiseTime").val();
	var appName=$("#appraiseName").val();
	var appDesc=$("#appraiseDesc").val();
	var appType=$("#appraiseType").val();

	if (!dateCompare(appTime)) {
		$('#appraiseTimeForm').attr("class","form-group has-error");
		$('#appraiseTime').attr("data-content","不能大于当前时间!");
		$('#appraiseTime').popover({placement:'bottom'});
		$('#appraiseTime').popover({trigger:'manual'});
		$('#appraiseTime').popover('show');
		return;		
	};

		// submit	
		$.get('../users/regtable/addAppraiseExperience/?time='+appTime+'&appraiseName='+appName+
			"&appraiseDesc="+appDesc+'&appraiseType='+appType,
			function  (data) {
				// body...
				if(data=='exist'){
					alert("该评审/评估经历已存在！");
					return;
				} else {
					alert("添加成功！");
					$("#appraiseExperienceFormHead").after(
						"<tr><td>"+appTime+"</td><td>"+appName+"</td><td>"+appDesc+"</td><td>"+appType+
						"</td><td><button type='button' id='deleteAppraiseExperience' class='btn btn-default'>删除</button></td></tr>")
				}
				clearInput("appraiseTime","appraiseTimeForm");
				clearInput("appraiseName","appraiseNameForm");
				clearInput("appraiseDesc","appraiseDescForm");
				clearInput("appraiseType","appraiseTypeForm");
				$("#AppraiseExperienceModal").modal('toggle');
				$("#AppraiseExperienceModal").modal('hide');
				return;
			})
	};
});

// 删除评审/评估经历
$("#t_2").on('click',function(e){
	if(e.target.id=="deleteAppraiseExperience"){
		var time=$(e.target).parents().prev().prev().prev().prev().text();
		var name=$(e.target).parent().prev().prev().prev().text();
		var row=$(e.target).parent().parent();
		$.get("../users/regtable/delAppraiseExperience/?time="+time+"&appraiseName="+name,function(data,status){
			if (data == "ok") {
				alert("删除评审/评估经历成功！");
				row.remove();				
			};
		})
	}
})

// 增加工作经历
$("#addWorkingExp").click(function(){
	if (!isEmpty("startTime","startTimeForm","请输入开始时间") &
		!isEmpty("endTime","endTimeForm","请输入终止时间") & 
		!isEmpty("workingUnit","workingUnitForm","请输入工作单位") &
		!isEmpty("job","jobForm","请输入职务描述") &
		!isEmpty("referee","refereeForm","请输入证明人")) {
		// submit

	var stime=$("#startTime").val();
	var etime=$("#endTime").val();
	var unit=$("#workingUnit").val();
	var job=$("#job").val();
	var referee=$("#referee").val();

	// 比较起始时间和终止时间
	if (!dateCompare(stime,etime)) {
		$('#endTimeForm').attr("class","form-group has-error");
		$('#endTime').attr("data-content","终止时间不能小于起始时间!");
		$('#endTime').popover({placement:'bottom'});
		$('#endTime').popover({trigger:'manual'});
		$('#endTime').popover('show');
		return;		
	};

	// 比较起始时间和当前时间
	if (!dateCompare(stime)) {
		$('#startTimeForm').attr("class","form-group has-error");
		$('#startTime').attr("data-content","起始时间不能大于当前时间!");
		$('#startTime').popover({placement:'bottom'});
		$('#startTime').popover({trigger:'manual'});
		$('#startTime').popover('show');
		return;		
	};

	// 比较终止时间和当前时间
	if (!dateCompare(etime)) {
		$('#endTimeForm').attr("class","form-group has-error");
		$('#endTime').attr("data-content","终止时间不能大于当前时间!");
		$('#endTime').popover({placement:'bottom'});
		$('#endTime').popover({trigger:'manual'});
		$('#endTime').popover('show');
		return;		
	};

	$.get('../users/regtable/addWorkingExperience/?startTime='+stime+'&endTime='+etime+
		"&workingUnit="+unit+'&job='+job+'&referee='+referee,
		function  (data) {
				// body...
				if(data=='exist'){
					alert("该工作经历已存在！");
					return;
				} else {
					alert("添加成功！");
					$("#workingExperienceFormHead").after(
						"<tr><td>"+stime+"</td><td>"+etime+"</td><td>"+unit+"</td><td>"+job+
						"</td><td>"+referee+"</td><td><button type='button' id='deleteWorkingExperience' class='btn btn-default'>删除</button></td></tr>")
				}
				clearInput("startTime","startTimeForm");
				clearInput("endTime","endTimeForm");
				clearInput("workingUnit","workingUnitForm");
				clearInput("job","jobForm");
				clearInput("referee","refereeForm");
				$("#WorkingExperienceModal").modal('toggle');
				$("#WorkingExperienceModal").modal('hide');
				return;
			})
};
});

// 删除工作经历
$("#t_3").on('click',function(e){
	if(e.target.id=="deleteWorkingExperience"){
		var stime=$(e.target).parents().prev().prev().prev().prev().prev().text();
		var etime=$(e.target).parent().prev().prev().prev().prev().text();
		var unit=$(e.target).parent().prev().prev().prev().text();
		var row=$(e.target).parent().parent();
		$.get("../users/regtable/delWorkingExperience/?startTime="+stime+"&endTime="+etime+
			"&workingUnit="+unit,function(data,status){
				if (data == "ok") {
					alert("删除工作经历成功！");
					row.remove();				
				};
			})
	}
})

// 增加回避单位
$("#addWorkingUnit").click(function(){
	if (!isEmpty("avoidUnitName","avoidUnitNameForm","请输入回避单位名") & 
		!isEmpty("IsWorkingUnit","IsWorkingUnitForm","请选择是否为工作单位")) {
		// submit
	var avoidName=$("#avoidUnitName").val();
	var isWork=$("#IsWorkingUnit").val();
	$.get('../users/regtable/addAvoidingUnit/?unitName='+avoidName+'&isWorkingUnit='+isWork,
		function  (data) {
				// body...
				if(data == 'exist'){
					alert("该回避单位已存在！");
					return;
				} else {
					alert("添加成功！");
					$("#avodingUnitFormHead").after(
						"<tr><td>"+avoidName+"</td><td>"+isWork+
						"</td><td><button type='button' id='deleteAvoidingUnit' class='btn btn-default'>删除</button></td></tr>")
				}
				clearInput("avoidUnitName","avoidUnitNameForm");
				clearInput("IsWorkingUnit","IsWorkingUnitForm");
				$("#AvodingUnitModal").modal('toggle');
				$("#AvodingUnitModal").modal('hide');
				return;
			})
};
});

// 删除回避单位
$("#t_4").on('click',function(e){
	if(e.target.id=="deleteAvoidingUnit"){
		var name=$(e.target).parent().prev().prev().text();
		var row=$(e.target).parent().parent();
		$.get("../users/regtable/delAvoidingUnit/?unitName="+name,function(data,status){
			if (data == "ok") {
				alert("删除回避单位成功！");
				row.remove();				
			};
		})
	}
})


$.get('../users/expGetInfo',function (data,status){
	var d=$.parseJSON(data)
	var key;

		// 将保存的信息填入
		for (key in d){
			$("#"+key).val(d[key]);
		}

		// 判断是否已提交
		if (d['verifyState']=="审核中") {
			$('[base="true"]').attr("disabled",true)
		};
	})


// 保存
$("#saveInfo").click(function (argument) {
		// body...
		$.post('../users/regtable/saveInfo',{
			'expName':$("#expName").val(),
			'expSex':$("#expSex").val(),
			'birthday':$("#birthday").val(),
			'politicalStatus':$("#politicalStatus").val(),
			'IDType':$("#IDType").val(),
			'authority':$("#authority").val(),
			'IDNumber':$("#IDNumber").val(),
			'highestSchooling':$("#highestSchooling").val(),
			'highestDegree':$("#highestDegree").val(),
			'title':$("#title").val(),
			'titleID':$("#titleID").val(),
			'expjob':$("#expjob").val(),
			'workingLength':$("#workingLength").val(),
			'isRetired':$("#isRetired").val(),
			'isPart_time':$("#isPart_time").val(),
			'expworkingUnit':$("#expWorkingUnit").val(),
			'address':$("#address").val(),
			'zipcode':$("#zipcode").val(),
			'email':$("#email").val(),
			'mobilePhone':$("#mobilePhone").val(),
			'homePhone':$("#homePhone").val(),
			'graduateSchool':$("#graduateSchool").val(),
			'skill':$("#skill").val(),
			'achievements':$("#achievements").val(),
			'otherDesc':$("#otherDesc").val()
		},function (data,status) {
			// body...
			if (data=='ok') {
				alert("保存成功")	
				$("#verifyState").text("填写中")
			};
		})
	})


	// 提交
	$("#submitInfo").click(function (argument) {

		// validating
		var finished=true;
		$("[base='true']").each(function  (argument) {
			// body...
			if($(this).val()==''){
				$(this).attr("data-content","请填写");
				$(this).popover({placement:'bottom'});
				$(this).popover({trigger:'manual'});
				$(this).popover('show');
				finished=false;
			}
		})
		if(!finished){
			return;
		}

		// 先保存后提交
		$.post('/users/regtable/saveInfo',{
			'expName':$("#expName").val(),
			'expSex':$("#expSex").val(),
			'birthday':$("#birthday").val(),
			'politicalStatus':$("#politicalStatus").val(),
			'IDType':$("#IDType").val(),
			'authority':$("#authority").val(),
			'IDNumber':$("#IDNumber").val(),
			'highestSchooling':$("#highestSchooling").val(),
			'highestDegree':$("#highestDegree").val(),
			'title':$("#title").val(),
			'titleID':$("#titleID").val(),
			'expjob':$("#expjob").val(),
			'workingLength':$("#workingLength").val(),
			'isRetired':$("#isRetired").val(),
			'isPart_time':$("#isPart_time").val(),
			'expworkingUnit':$("#expworkingUnit").val(),
			'address':$("#address").val(),
			'zipcode':$("#zipcode").val(),
			'email':$("#email").val(),
			'mobilePhone':$("#mobilePhone").val(),
			'homePhone':$("#homePhone").val(),
			'graduateSchool':$("#graduateSchool").val(),
			'skill':$("#skill").val(),
			'achievements':$("#achievements").val(),
			'otherDesc':$("#otherDesc").val()
		},function (data,status) {
			// submit
			$.post('/users/regtable/submitInfo',function  (data,status) {
				// do nothing
				if (data=="ok") {
					alert("提交成功！")
				};
			})
		})

		// 重新显示表格
		$.get('/users/expGetInfo',function (data,status){
			var d=$.parseJSON(data)
			var key;

			// 将保存的信息填入
			for (key in d){
				$("#"+key).val(d[key]);
			}

			// 判断是否已提交
			if (d['verifyState']=="审核中") {
				$('[base="true"]').attr("disabled",true)
				$('[base="true"]').attr("disabled",true)
			};
		})
	})


// admin part

// 查询专家
$("#query").click(function  (e) {
	// body...
	e.preventDefault()
	$.post('/users/searchexp',{
		"field":$("#fieldQuery").val(),
		"status":$("#stateQuery").val()
	},function (data,status) {
		// body...
		$("#searchResult").nextAll().remove()
		var d=$.parseJSON(data)
		var one;
		for (var i = 0; i < d.length; i++) {
			one=d[i]
			$("#searchResult").after('<tr><td>'+one["expCertificateID"]+'</td><td>'+
				one["expName"]+'</td><td>'+one["expworkingUnit"]+'</td><td>'+
				one["mobilePhone"]+'</td><td>'+one["type"]+'</td><td>'+one['verifyState']+
				'</td><td><a href="/users/admin/expinfo/'+one['username']+'">显示评审项目</a></td></tr>')
		};
	})
})

// 同意申请
$("#passExp").click(function  (argument) {
	// body...
	var username=$("#username").text();
	$.post('/users/expinfo/agreeExpert',{
		'username':username
	},function  (data,status) {
		// body...
		var d=$.parseJSON(data)
		alert("已同意申请！")
		$("#expCertificateID").text(d['certificate'])
		$("#certificateValidTime").text(d['validTime'])
		$("#verifyState").text("可用")
		$("#denyExp").attr("disabled",true)
	})
})

// 驳回申请
$("#denyExp").click(function (argument) {
	// body...
	var l=$("#denyReason").val().length
	$("#denyInput").text(l)
	$("#denyLeft").text(500-l)
	if (l>=500|l<=0) {
		$("#denySubmit").attr("disabled",true)
	} else {
		$("#denySubmit").attr("disabled",false)
	}
})
$("#denyReason").on('keyup',function (argument) {
	// body...
	var l=$("#denyReason").val().length
	$("#denyInput").text(l)
	$("#denyLeft").text(500-l)
	if (l>=500|l<=0) {
		$("#denySubmit").attr("disabled",true)
	} else {
		$("#denySubmit").attr("disabled",false)
	}
})
$("#denySubmit").on('click',function (argument) {
	// body...
	var username=$("#username").text();
	$.post('/users/expinfo/denyExpert',{
		'username':username,
		'verifyStateReason':$("#denyReason").val(),
	},function (argument) {
		// body...
		alert("申请已驳回！")
		$("#verifyState").text("驳回")
		$("#denyModal").modal('toggle')
		$("#denyModal").modal('hide');
	})
})

// 终止资格
$("#stopExp").click(function (argument) {
	// body...
	var l=$("#stopReason").val().length
	$("#stopInput").text(l)
	$("#stopLeft").text(500-l)
	if (l>=500|l<=0) {
		$("#stopSubmit").attr("disabled",true)
	} else {
		$("#stopSubmit").attr("disabled",false)
	}
})
$("#stopReason").on('keyup',function (argument) {
	// body...
	var l=$("#stopReason").val().length
	$("#stopInput").text(l)
	$("#stopLeft").text(500-l)
	if (l>=500|l<=0) {
		$("#stopSubmit").attr("disabled",true)
	} else {
		$("#stopSubmit").attr("disabled",false)
	}
})
$("#stopSubmit").on('click',function (argument) {
	// body...
	var username=$("#username").text();
	$.post('/users/expinfo/stopExpert',{
		'username':username,
		'verifyStateReason':$("#stopReason").val(),
	},function (argument) {
		// body...
		alert("资格已终止！")
		$("#verifyState").text("终止")
		$("#stopModal").modal('toggle')
		$("#stopModal").modal('hide');
	})
})
})
