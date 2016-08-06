$(document).on('ready',function (argument) {
	// body...
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
			'workingUnit':$("#expWorkingUnit").val(),
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
			'workingUnit':$("#workingUnit").val(),
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
			};
		})
	})
})
