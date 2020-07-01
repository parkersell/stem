function setChart(){
    var ctx = document.getElementById("myChart");
    var ctx2 = document.getElementById("myChart2");
    var tf =  'YYYY-MMM-D h:mm a';
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: stud1time,
        datasets: [{
            label: labels1,
            yAxisID: labels1,
            data: stud1hr,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'minute',
                    
                },
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 20
                }
            }],
            yAxes: [{
                id: labels1,
                type: 'linear',
                ticks: {
                    suggestedMin: 50
                }
            }]
        }
    }

});
    /* var myChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: stud2time,
        datasets: [{
            label: labels2,
            yAxisID: labels2,
            data: stud2hr,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'minute'
                }
            }],
            yAxes: [{
                id: labels2,
                type: 'linear',
            }]
        }
    }
}); */
}