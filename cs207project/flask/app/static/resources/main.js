var json;

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
            alert_data(json);
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




	// force hide the first panel of the accordion 
	$('#collapseOne').collapse("hide");

	// disable get time series buttons at page init.
	$('#btn-get-by-file').attr('disabled', 'disabled');
	$('#btn-get-by-id').attr('disabled', 'disabled');







	   $('#input-file').change(function() {
      if($(this).val()) {

        $('#btn-get-by-file').removeAttr('disabled');
      } else {
      	$('#btn-get-by-file').attr('disabled', '');
      }
    });

	   	   $('#id-input').change(function() {
      if($(this).val()) {


        $('#btn-get-by-id').removeAttr('disabled');
      } else {
      	$('#btn-get-by-id').attr('disabled', '');
      }
    });









// $('.panel-collapse').on('show.bs.collapse', function () {
// 	id = ($(this).attr('id'));
//   // do something…
//   //e.preventDefault();
//   if (id = collapseOne) {
//   	alert("YES!");

//   }
//   //$("#s1_placeholder").empty();
  

  
// })


	$('.panel-collapse').on('shown.bs.collapse', function () {





      $.ajax({
      url: '/timeseries/' + 100,
      //data: id,
      type: 'GET',
      success: function(response) {


          $("#secondary" + 1 + "-id span").empty().append(response.id);
          $("#secondary" + 1 + "-std span").empty().append(response.metadata[0].std);
          $("#secondary" + 1 + "-mean span").empty().append(response.metadata[0].mean);
          $("#secondary" + 1 + "-blarg span").empty().append(response.metadata[0].blarg);
          $("#secondary" + 1 + "-level span").empty().append(response.metadata[0].level);

        



                        var options = {
    series: {
        lines: { show: true, colors: ["#dba255"]},
        points: { show: false }
       
    },
    colors: ["#FF7070","#3b97d3"]
};

        // var d1 = [];
        // for (var i = 0; i < 14; i += 0.5) {
        //   d1.push([i, Math.sin(i)]);
        // }

        // var d2 = [[0, 3], [4, 8], [8, 5], [9, 13],[10, 12], [5, 22], [8, 44], [9, 55]];

        // var d2 = [];
        // for (var i = 0; i < 14; i += 2.5) {
        //   d2.push([i, Math.sin(i)]);
        // }




  times = response.time_series.time;
  values = response.time_series.value;

  var data = [];

  for ( i = 0; i < times.length; i++)
  {
    data.push([times[i], values[i]]);

  }

  // var myJsonString = JSON.stringify(data);

  data = {"data":data};




        // A null signifies separate line segments

        // var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];

        $.plot("#s1_placeholder", [ data ], options);

        // Add the Flot version string to the footer






          // console.log(response.metadata[0].blarg);
          // console.log(response.id)
          // console.log(response.time_series.time)
      },
      error: function(error) {
          console.log(error);
      }
  });







	  // do something…
	  //e.preventDefault();
	   // getData();
      //getSecondaryCharts();

	  
	})

	$('.panel-collapse').on('hide.bs.collapse', function () {
	  // do something…
	  //e.preventDefault();
	  //$("#s1_placeholder").empty();
	})





    // $("#btn-get-by-id").click(function(e) {

    // 	id = $("#id-input").val();

    //     e.preventDefault();
    //     getPrimaryChart();
    //     getData();

    // });

    $("#btn-get-by-file").click(function(e) {

    //alert("FROM BUTTON" + 'Id : ' + json.id + ', Std : '+ json.std + ', TS : ' + json.ts[0].value)

    getPrimaryChartByFileInput(json);





  // var reader = new FileReader();

  // // alert("YES");

  // reader.onload = function(event) {
  //   var jsonObj = JSON.parse(event.target.result);
  //   alert(jsonObj.name);
  // }

  // reader.readAsText(event.target.files[0]);






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
            var json = JSON.parse(contents);
            alert_data(json);
        };
        readFile.readAsText(uploadedFile);
    } else { 
        console.log("Failed to load file");
    }
});

function alert_data(json)
{
     alert('id : ' + json.id + ', Std : '+ json.std)
}






//     	var file = document.getElementById('input-file').files[0]; //Files[0] = 1st file
// var reader = new FileReader();
// reader.readAsText(file, 'UTF-8');

// alert(reader);

//     	   var fileName = document.getElementById('input-file').files[0].name; //Should be 'picture.jpg'
// alert(fileName);











//     	var myFile = $('#input-file').prop('files');
//     	alert(myFile);

//     	var form = new FormData(); 
// form.append("video", $("#input-file")[0].files[0]);

// 		alert(form);


// ( function ( $ ) {
// 	// Add click event handler to button
// 	$( '#input-file' ).click( function () {
		// if ( ! window.FileReader ) {
		// 	return alert( 'FileReader API is not supported by your browser.' );
		// }
		// var $i = $( '#input-file' ), // Put file input ID here
		// 	input = $i[0]; // Getting the element from jQuery
		// if ( input.files && input.files[0] ) {
		// 	file = input.files[0]; // The file
		// 	fr = new FileReader(); // FileReader instance
		// 	fr.onload = function () {
		// 		// Do stuff on onload, use fr.result for contents of file
		// 		$( '#file-content' ).append( $( '<div/>' ).html( fr.result ) )
		// 	};
		// 	//fr.readAsText( file );
		// 	fr.readAsDataURL( file );
		// } else {
		// 	// Handle errors here
		// 	alert( "File not selected or browser incompatible." )
		// }
	// } );
// } )( jQuery );








        e.preventDefault();
        getPrimaryChart();
        getData();

    });

});



    function getData() {
    	
    	getCharts();

     //    $.ajax({
	    //     type: "POST",
	    //     url: '@Url.Action("SelectPackage", "Home")',
	    //     dataType: "JSon",
	    //     data: { "PackageId": PackageId },
	    //     success: function (data) {
	    //         console.log(data);
	    //         //$("#SecondInfo").focus({ scrollTop: "0px" });
	    //         $('html, body').animate({ scrollTop: $('#contact-us').offset().top }, 'slow');
	    //     },
	    //     error: console.log("it did not work"),
    	// });
};







function getPrimaryChartById(response) {

  // var toString = Object.prototype.toString;




  $("#primary-id span").empty().append(response.id);
  $("#primary-std span").empty().append(response.metadata[0].std);
  $("#primary-mean span").empty().append(response.metadata[0].mean);
  $("#primary-blarg span").empty().append(response.metadata[0].blarg);
  $("#primary-level span").empty().append(response.metadata[0].level);


  times = response.time_series.time;
  values = response.time_series.value;

  var data = [];

  for ( i = 0; i < times.length; i++)
  {
    data.push([times[i], values[i]]);

  }

  // var myJsonString = JSON.stringify(data);

  data = {"data":data};

// OBJ.prototype.toJSON = function (key) {
//        var returnObj = new Object();
//        returnObj.data = data
//        return returnObj;
//    }

// console.log("JSON" + myJsonString);

// console.log("TIMES" + times);
// console.log("VALUES" + values);
//var data = new Array(times, values);
// console.log("THE VALUES - " + data);

//   console.log("YES" + response.time_series.value);

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

        //console.log("D1" + d1);

        //d1 = data;

        // var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];
        // console.log("D2" + d2);

        // // A null signifies separate line segments

        // var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];

        $.plot("#placeholder", [ data ], options);

        // Add the Flot version string to the footer

      });	
}






function getPrimaryChartByFileInput(json) {

	//console.log(json.id);

	$('#main-content').show();

      // $(function() {

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


	for (var i = 0; i < json.ts.length; i++) {
	    var obj = json.ts[i].value
	    console.log(obj);
	}



        // var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];

        // // A null signifies separate line segments

        // var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];

        $.plot("#placeholder", [ d1 ], options);

        // Add the Flot version string to the footer

      // });	
}





function getSecondaryCharts(response) {

  
//console.log("THE RESPONSE" + response[0].id);

        for (i = 0; i < 2; i++) {
  $.ajax({
      url: '/timeseries/' + response[i].id,
      //data: id,
      type: 'GET',
      success: function(response) {


          $("#secondary" + i + "-id span").empty().append(response.id);
          $("#secondary" + i + "-std span").empty().append(response.metadata[0].std);
          $("#secondary" + i + "-mean span").empty().append(response.metadata[0].mean);
          $("#secondary" + i + "-blarg span").empty().append(response.metadata[0].blarg);
          $("#secondary" + i + "-level span").empty().append(response.metadata[0].level);

        



                        var options = {
    series: {
        lines: { show: true, colors: ["#dba255"]},
        points: { show: false }
       
    },
    colors: ["#FF7070","#3b97d3"]
};

        // var d1 = [];
        // for (var i = 0; i < 14; i += 0.5) {
        //   d1.push([i, Math.sin(i)]);
        // }

        // var d2 = [[0, 3], [4, 8], [8, 5], [9, 13],[10, 12], [5, 22], [8, 44], [9, 55]];

        // var d2 = [];
        // for (var i = 0; i < 14; i += 2.5) {
        //   d2.push([i, Math.sin(i)]);
        // }




  times = response.time_series.time;
  values = response.time_series.value;

  var data = [];

  for ( i = 0; i < times.length; i++)
  {
    data.push([times[i], values[i]]);

  }

  // var myJsonString = JSON.stringify(data);

  data = {"data":data};




        // A null signifies separate line segments

        // var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];

        $.plot("#s1_placeholder", [ data ], options);

        // Add the Flot version string to the footer






          // console.log(response.metadata[0].blarg);
          // console.log(response.id)
          // console.log(response.time_series.time)
      },
      error: function(error) {
          console.log(error);
      }
  });

}








 


      $(function() {

//       	      	var options = {
//     series: {
//         lines: { show: true, colors: ["#dba255"]},
//         points: { show: true }
       
//     },
//     colors: ["#FF7070","#3b97d3"]
// };

//         // var d1 = [];
//         // for (var i = 0; i < 14; i += 0.5) {
//         //   d1.push([i, Math.sin(i)]);
//         // }

//         // var d2 = [[0, 3], [4, 8], [8, 5], [9, 13],[10, 12], [5, 22], [8, 44], [9, 55]];

//         var d2 = [];
//         for (var i = 0; i < 14; i += 2.5) {
//           d2.push([i, Math.sin(i)]);
//         }

//         // A null signifies separate line segments

//         // var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];

//         $.plot("#s1_placeholder", [ d2 ], options);

//         // Add the Flot version string to the footer

      });

            $(function() {

        // var d1 = [];
        // for (var i = 0; i < 14; i += 0.5) {
        //   d1.push([i, Math.sin(i)]);
        // }

        var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];

        // A null signifies separate line segments

        // var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];

        $.plot("#s2_placeholder", [ d2 ]);

        // Add the Flot version string to the footer

      });







	
};


// AJAX CALLS

// $('#btn-get-by-id').click(function() {
//     // var user = $('#txtUsername').val();
//     // var pass = $('#txtPassword').val();
//     $.ajax({
//         url: '/timeseries',
//         //data: $('form').serialize(),
//         type: 'GET',
//         success: function(response) {
//             console.log(response[0].blarg);
//         },
//         error: function(error) {
//             console.log(error);
//         }
//     });
// });


$('#btn-get-by-id').click(function(e) {


  e.preventDefault();

  id = $('#id-input').val()

  $.ajax({
      url: '/timeseries/' + id,
      //data: id,
      type: 'GET',
      success: function(response) {
        getPrimaryChartById(response);






          // console.log(response.metadata[0].blarg);
          // console.log(response.id)
          // console.log(response.time_series.time)
      },
      error: function(error) {
          console.log(error);
      }
  });

    //console.log(ts);

      //  id = $("#id-input").val();


         //getPrimaryChart();
    //     getData();







      $.ajax({
      url: '/simquery/',
      //data:id,
      data: { 
        "the_id": id
    },
      type: 'GET',
      success: function(response) {

          getSecondaryCharts(response);
          // console.log(response.metadata[0].blarg);
          // console.log(response.id);
          // console.log(response.time_series.time);
          //console.log(response[0].id);
      },
      error: function(error) {
          console.log(error);
      }
  });





});

// $('#btn-get-by-id').click(function() {
//   // var user = $('#txtUsername').val();
//   // var pass = $('#txtPassword').val();

//   id = $('#id-input').val()

//   $.ajax({
//       url: '/timeseries/simquery/',
//       data: {the_id:id},
//       type: 'GET',
//       success: function(response) {
//           // console.log(response.metadata[0].blarg);
//           // console.log(response.id);
//           // console.log(response.time_series.time);
//           console.log(response);
//       },
//       error: function(error) {
//           console.log(error);
//       }
//   });
// });


  //http://127.0.0.1:5000/timeseries/1