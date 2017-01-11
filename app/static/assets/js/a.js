        // 路径配置
        require.config({
            paths: {
                'echarts': 'http://echarts.baidu.com/build/dist'
            }
        });

        // 使用
        require(
            [
                'echarts',
                'echarts/chart/pie'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表

                myChart = ec.init(document.getElementById('main'));
                var option = {
                    title : {
                        text: 'System Cpu Load',
                        subtext: '系统负载',
                        x:'center'
                    },
                    tooltip : {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    legend: {
                        orient : 'vertical',
                        x : 'left',
                        data:[]
                    },
                    toolbox: {
                        show : true,  //是否开启工具栏
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {
                                show: true,
                                type: ['pie', 'funnel'],
                                option: {
                                    funnel: {
                                        x: '25%',
                                        width: '50%',
                                        funnelAlign: 'left',
                                        max: 1548
                                    }
                                }
                            },
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    series : []
                };
                    // 载入动画---------------------
                    myChart.showLoading({
                        text: '正在努力的读取数据中...'   //loading话术
                    });

                   // 定时器
                   window.onload=function(){
                   //每隔2秒检查一下数据
                   window.setInterval(checkStatus,5000);
                   };

                function checkStatus() {
                    // ajax 加载数据
                    $.ajax({
                        url: '/dataapi/query5api',  //
                        type: 'post',
                        contentType: "application/json;charset=UTF-8",
                        dataType: "json",
                        async: True,
                        data: {},
                        success: function (data) {


                            var legendData = [];
                            var seriesData = [];


                            if (data != null && data["series"].length > 0) {
                                legendData = data["legen"];
                                seriesData.push({
                                    "name": "CPU Load",
                                    "type": "pie",
                                    "radius": '65%',   //饼图半径大小
                                    "center": ['50%', '60%'],//饼图圆心位置x,y
                                    "data": function () {
                                        var t_data = [];
                                        for (var i = 0, len = data["series"].length; i < len; i++) {
                                            t_data.push({
                                                "name": legendData[i],
                                                "value": data["series"][i]
                                            });
                                        }
                                        return t_data;
                                    }()
                                });
                            }

                            option.legend.data = legendData;
                            myChart.setOption(option);
                            myChart.setSeries(seriesData);
                        },

                        error: function () {
                            var legendData = [''];
                            var seriesData = [
                                {
                                    "name": "饼图标例1",
                                    "type": "pie",
                                    "radius": '55%',   //饼图半径大小
                                    "center": ['50%', '60%'],//饼图圆心位置x,y
                                    data: [0]
                                }
                            ];
                            option.legend.data = legendData;
                            myChart.setOption(option);
                            myChart.setSeries(seriesData);

                        },
                        complete: function () {
                            //停止动画载入提示
                            myChart.hideLoading();
                        }
                    });
                }
            }

        );

