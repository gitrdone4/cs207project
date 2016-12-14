var json;

// on change, convert and handle the uploaded file to process for insertion to database
$(".form-control-file").change(function(event){
  var uploadedFile = event.target.files[0]; 

  if(uploadedFile.type !== "text/javascript" && uploadedFile.type !== "application/x-javascript") { 
    alert("Wrong file type == " + uploadedFile.type); 
    return false;
  }

  if (uploadedFile) {
    var readFile = new FileReader();
    readFile.onload = function(e) { 
        var contents = e.target.result;
        json = JSON.parse(contents);
        //alert_data(json);
    };
    readFile.readAsText(uploadedFile);
  } else {
      console.log("Failed to load file");
  }
});

  function alert_data(json)
{
     alert('Id : ' + json.id + ', Std : '+ json.std + ', TS : ' + json.ts[0].value)
}

$(document).ready(function() {

  // force show the panels of the accordion
  $('#collapseOne').show();
  $('#collapseTwo').show();
  $('#collapseThree').show();
  $('#collapseFour').show();
  $('#collapseFive').show();

  // disable get time series buttons at page init.
  $('#btn-get-by-file').attr('disabled', 'disabled');
  $('#btn-get-by-id').attr('disabled', 'disabled');

  // toggle disabled button quality when file is ready or not
  $('#input-file').change(function() {
    if($(this).val()) {
      $('#btn-get-by-file').removeAttr('disabled');
    } else {
      $('#btn-get-by-file').attr('disabled', '');
    }
  });

  // id must be provided for button to be enabled
  $('#id-input').change(function() {
    if($(this).val()) {
      $('#btn-get-by-id').removeAttr('disabled');
    } else {
      $('#btn-get-by-id').attr('disabled', '');
    }
  });

  // handles if actions are needed when panels are shown or hidden
  $('.panel-collapse').on('shown.bs.collapse', function () {
  })

  $('.panel-collapse').on('hide.bs.collapse', function () {
  })

  // display charts using the file uploaded
  $("#btn-get-by-file").click(function(e) {

    //alert("FROM BUTTON" + 'Id : ' + json.id + ', Std : '+ json.std + ', TS : ' + json.ts[0].value)

    //getPrimaryChartByFileInput(json);
    e.preventDefault();

    //id = $('#id-input').val()
    // test id
    id = 221;

    $.ajax({
        url: '/timeseries/' + id,
        //data: id,
        type: 'GET',
        success: function(response) {
          getPrimaryChartById(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
        $.ajax({
        url: '/simquery',
        data: {
          "the_id": id
        },
        type: 'GET',
        success: function(response) {
            getSecondaryCharts(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
  });
});

function getData() {
  getCharts();
};

var data1;
function getPrimaryChartById(response) {

  // populate the primary chart metadata fields
  $("#primary-id span").empty().append(response.id);
  $("#primary-std span").empty().append(response.metadata[0].std);
  $("#primary-mean span").empty().append(response.metadata[0].mean);
  $("#primary-blarg span").empty().append(response.metadata[0].blarg);
  $("#primary-level span").empty().append(response.metadata[0].level);

  // get the times and values, convert them to json format for flot
  times = response.time_series.time;
  values = response.time_series.value;

  data1 = [];
  for ( i = 0; i < times.length; i++)
  {
    data1.push([times[i], values[i]]);
  }

  data = {"data":data1};

  // show the main chart content
  $('#main-content').show();

    $(function() {
      var options = {
        series: {
        lines: { show: true, colors: ["#dba255"]},
        points: { show: false }
        },
        colors: ["#3b97d3","#FF7070"]
      };

      var d1 = [];
      for (var i = 0; i < 75; i += 0.5) {
        d1.push([i, Math.sin(i)]);
      }
      // plot the primary data chart 
      $.plot("#placeholder", [ data ], options);
      }); 
}

var d1;
function getPrimaryChartByFileInput(json) {

  $('#main-content').show();

    var options = {
      series: {
          lines: { show: true, colors: ["#dba255"]},
          points: { show: false }
      },
      colors: ["#3b97d3","#FF7070"]
    };

        d1 = [];
        for (var i = 0; i < 75; i += 0.5) {
          d1.push([i, Math.sin(i)]);
        }

  for (var i = 0; i < json.ts.length; i++) {
      var obj = json.ts[i].value
      console.log(obj);
  }
  $.plot("#placeholder", [ d1, data1 ], options);
}

// function to plot the 5 secondary charts
function getSecondaryCharts(response) {

  // ajax calls are used for each of the 5 similar charts

  $.ajax({
      url: '/timeseries/' + response[0].id,
      type: 'GET',
      success: function(response) {

        $("#secondary1-id span").empty().append(response.id);
        $(".btn1").addClass(" " + response.id);
        $("#secondary1-std span").empty().append(response.metadata[0].std);
        $("#secondary1-mean span").empty().append(response.metadata[0].mean);
        $("#secondary1-blarg span").empty().append(response.metadata[0].blarg);
        $("#secondary1-level span").empty().append(response.metadata[0].level);

        var options = {
          series: {
          lines: { show: true, colors: ["#dba255"]},
          points: { show: false }
          },
          colors: ["#FF7070","#3b97d3"]
        };

        times = response.time_series.time;
        values = response.time_series.value;

        var data = [];

        for ( i = 0; i < times.length; i++)
        {
          data.push([times[i], values[i]]);
        }
        data = {"data":data};

        $.plot("#s1_placeholder", [ data, data1 ], options);
      },
      error: function(error) {
          console.log(error);
      }
  });

  $.ajax({
    url: '/timeseries/' + response[1].id,
    type: 'GET',
    success: function(response) {

      $("#secondary2-id span").empty().append(response.id);
      $(".btn2").addClass(" " + response.id);
      $("#secondary2-std span").empty().append(response.metadata[0].std);
      $("#secondary2-mean span").empty().append(response.metadata[0].mean);
      $("#secondary2-blarg span").empty().append(response.metadata[0].blarg);
      $("#secondary2-level span").empty().append(response.metadata[0].level);

      var options = {
        series: {
        lines: { show: true, colors: ["#dba255"]},
        points: { show: false }
        },
        colors: ["#FF7070","#3b97d3"]
      };

      times = response.time_series.time;
      values = response.time_series.value;

      var data = [];

      for ( i = 0; i < times.length; i++)
      {
        data.push([times[i], values[i]]);
      }
      data = {"data":data};

      $.plot("#s2_placeholder", [ data, data1 ], options);
    },
    error: function(error) {
        console.log(error);
    }
  });

  $.ajax({
  url: '/timeseries/' + response[2].id,
  type: 'GET',
  success: function(response) {

    $("#secondary3-id span").empty().append(response.id);
    $(".btn3").addClass(" " + response.id);
    $("#secondary3-std span").empty().append(response.metadata[0].std);
    $("#secondary3-mean span").empty().append(response.metadata[0].mean);
    $("#secondary3-blarg span").empty().append(response.metadata[0].blarg);
    $("#secondary3-level span").empty().append(response.metadata[0].level);

    var options = {
      series: {
      lines: { show: true, colors: ["#dba255"]},
      points: { show: false }
      },
      colors: ["#FF7070","#3b97d3"]
    };

    times = response.time_series.time;
    values = response.time_series.value;

    var data = [];

    for ( i = 0; i < times.length; i++)
    {
      data.push([times[i], values[i]]);
    }
    data = {"data":data};

    $.plot("#s3_placeholder", [ data, data1 ], options);
  },
  error: function(error) {
      console.log(error);
  }
});

  $.ajax({
  url: '/timeseries/' + response[3].id,
  type: 'GET',
  success: function(response) {

    $("#secondary4-id span").empty().append(response.id);
    $(".btn4").addClass(" " + response.id);
    $("#secondary4-std span").empty().append(response.metadata[0].std);
    $("#secondary4-mean span").empty().append(response.metadata[0].mean);
    $("#secondary4-blarg span").empty().append(response.metadata[0].blarg);
    $("#secondary4-level span").empty().append(response.metadata[0].level);

    var options = {
      series: {
      lines: { show: true, colors: ["#dba255"]},
      points: { show: false }
      },
      colors: ["#FF7070","#3b97d3"]
    };

    times = response.time_series.time;
    values = response.time_series.value;

    var data = [];

    for ( i = 0; i < times.length; i++)
    {
      data.push([times[i], values[i]]);
    }
    data = {"data":data};

    $.plot("#s4_placeholder", [ data, data1 ], options);
  },
  error: function(error) {
      console.log(error);
  }
});

  $.ajax({
  url: '/timeseries/' + response[4].id,
  type: 'GET',
  success: function(response) {

    $("#secondary5-id span").empty().append(response.id);
    $(".btn5").addClass(" " + response.id);
    $("#secondary5-std span").empty().append(response.metadata[0].std);
    $("#secondary5-mean span").empty().append(response.metadata[0].mean);
    $("#secondary5-blarg span").empty().append(response.metadata[0].blarg);
    $("#secondary5-level span").empty().append(response.metadata[0].level);

    var options = {
      series: {
      lines: { show: true, colors: ["#dba255"]},
      points: { show: false }
      },
      colors: ["#FF7070","#3b97d3"]
    };

    times = response.time_series.time;
    values = response.time_series.value;

    var data = [];

    for ( i = 0; i < times.length; i++)
    {
      data.push([times[i], values[i]]);
    }
    data = {"data":data};

    $.plot("#s5_placeholder", [ data, data1 ], options);
    },
    error: function(error) {
        console.log(error);
    }
  });
};

// an ID was provided, make the ajax calls to get the primary chart setup and find 
// the five most similar
$('#btn-get-by-id').click(function(e) {

  e.preventDefault();

  id = $('#id-input').val()

  $.ajax({
      url: '/timeseries/' + id,
      //data: id,
      type: 'GET',
      success: function(response) {
        getPrimaryChartById(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
      $.ajax({
      url: '/simquery',
      data: {
        "the_id": id
      },
      type: 'GET',
      success: function(response) {
          getSecondaryCharts(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
});

// a similar chart was selected to become the primary chart
$('.btn-get-similar-ts').click(function(e) {

  e.preventDefault();
  id = $(this).attr('class').split(' ').pop();

  $.ajax({
      url: '/timeseries/' + id,
      type: 'GET',
      success: function(response) {
        getPrimaryChartById(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
      $.ajax({
      url: '/simquery',
      data: { 
        "the_id": id
      },
      type: 'GET',
      success: function(response) {

          getSecondaryCharts(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
});