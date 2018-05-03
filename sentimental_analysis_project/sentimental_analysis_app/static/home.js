 function renderPieChart(chartData){
        var chart = c3.generate({
        data: {
        // iris data from R
        columns: chartData,
        type : 'pie',
        onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
        }
        });

        chart.load({
        columns: chartData
        });
    }

function renderBarChart(chartData) {
    var chart = c3.generate({
    data: {
        columns: chartData,
        type: 'bar'
    },
    bar: {
        width: {
            ratio: 0.4 // this makes bar width 50% of length between ticks
        }
        // or
        //width: 100 // this makes bar width 100px
    }
    });
}

function renderStackChart(chartData) {
    var chart = c3.generate({
    data: {
        columns: chartData,
        types: {
            data1: 'area-spline',
            data2: 'area-spline'
            // 'line', 'spline', 'step', 'area', 'area-step' are also available to stack
        },
        groups: [['data1', 'data2']]
    }
    });
}



// Show chart for Q1
    $('#display-charts-q1').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q1/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    console.log(data);
                    chartData = data.chartData;
                    chartTitle = data.chartTitle;
                    
                    $('<div class=divText>' + chartTitle + '</div>').appendTo('#chartTitle');
                    renderPieChart(chartData);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});

// Q2.most popular tweets.
$('#display-charts-q2').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q2/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    var chartData = data.chartData;
                    var chartTitle = data.chartTitle;
                    
                    var trHTML = '';
                    var tblHTML =  "<br><table id='famous-tweets' class='table table-bordered table-hover'><tr><th>ID </th><th>ScreenName </th><th>Text </th><th>Famous Count </th></tr></table>";
                   
                   $('#charts-display').append(tblHTML);

                    $.each(chartData, function (i, item) {
                    trHTML += '<tr><td>' + chartData[i].id + '</td><td>' + chartData[i].screenName + '</td><td>' + chartData[i].text + '</td><td>' + chartData[i].famousCount + '</td></tr>';
                    });
                   
                   $('#famous-tweets').append(trHTML);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});


// Q2.b.most popular re-tweeted tweets.
$('#display-charts-test').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q2b/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    var chartData = data.chartData;
                    var chartTitle = data.chartTitle;
                    
                    var trHTML = '';
                    var tblHTML =  "<br><table id='retweeted-tweets' class='table table-bordered table-hover'><tr><th>ID </th><th>ScreenName </th><th>Text </th><th>ReTweeted Count </th></tr></table>";
                   
                   $('#charts-display').append(tblHTML);

                    $.each(chartData, function (i, item) {
                    trHTML += '<tr><td>' + chartData[i].id + '</td><td>' + chartData[i].screenName + '</td><td>' + chartData[i].text + '</td><td>' + chartData[i].retweetCount + '</td></tr>';
                    });
                   
                   $('#retweeted-tweets').append(trHTML);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});


// Show chart for Q3
    $('#display-charts-q3').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q3/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    console.log(data);
                    chartData = data.chartData;
                    chartTitle = data.chartTitle;
                    $('<div class=divText>' + chartTitle + '</div>').appendTo('#chartTitle');
                    renderStackChart(chartData);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});

// Show chart for Q4
    $('#display-charts-q4').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q4/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    console.log(data);
                    chartData = data.chartData;
                    chartTitle = data.chartTitle;
                    $('<div class=divText>' + chartTitle + '</div>').appendTo('#chartTitle');
                    renderBarChart(chartData);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});


// Show chart for Q5
    $('#display-charts-q5').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q5/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    console.log(data);
                    chartData = data.chartData;
                    chartTitle = data.chartTitle;
                    $('<div class=divText>' + chartTitle + '</div>').appendTo('#chartTitle');
                    renderBarChart(chartData);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});


// Q6.most popular Users.
$('#display-charts-q6').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q6/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    var chartData = data.chartData;
                    var chartTitle = data.chartTitle;
                    
                    var trHTML = '';
                    var tblHTML =  "<br><center><table id='famous-tweets' class='table table-bordered table-hover'><tr><th>ID </th><th> ScreenName </th><th> ReTweet </th><th> Tweet </th></tr></table><center>";
                   
                   $('#charts-display').append(tblHTML);

                    $.each(chartData, function (i, item) {
                    trHTML += '<tr><td>' + chartData[i].id + '</td><td>' + chartData[i].screenName + '</td><td>' + chartData[i].retweetCount + '</td><td>' + chartData[i].tweetCount + '</td></tr>';
                    });
                   
                   $('#famous-tweets').append(trHTML);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});


// Q7Users whose tweets generated most replies.
$('#display-charts-q7').on('click', function(){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/q7/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    jQuery('#chartTitle').empty();
                    jQuery('#charts-display').empty();;
                    jQuery('#chart').empty();
                    var chartData = data.chartData;
                    var chartTitle = data.chartTitle;
                    
                    var trHTML = '';
                    var tblHTML =  "<br><center><table id='famous-tweets' class='table table-bordered table-hover'><tr><th>ID </th><th> User </th><th> RepliesReceived </th></tr></table><center>";
                   
                   $('#charts-display').append(tblHTML);

                    $.each(chartData, function (i, item) {
                    trHTML += '<tr><td>' + chartData[i].id + '</td><td>' + chartData[i].user + '</td><td>' + chartData[i].repliesReceived + '</td></tr>';
                    });
                   
                   $('#famous-tweets').append(trHTML);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
});

// Dump csv to DB
$('#processdata_id').on('click', function(){
    if (confirm("This is a one time process to insert processed data into database, it will override data! are you sure?")){
    $.ajax({
            dataType: "json",
            type: "GET",
            url: '/processdata/',
            success: function(data){
            console.log('test');
                if(data.error) {
                    alert(data.error);
                } else {
                    console.log(data);
                    alert(data.message);
                }
            },
            error: function(jqXHR, textStatus, errorThrown)
          {
              alert(errorThrown);
           }
        });
    }
    return false;
});

