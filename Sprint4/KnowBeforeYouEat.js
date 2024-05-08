$(document).ready(function () {
  // Init
  $(".image-section").hide();
  $(".loader").hide();
  $("#result").hide();

  // Upload Preview
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#imagePreview").css(
          "background-image",
          "url(" + e.target.result + ")"
        );
        $("#imagePreview").hide();
        $("#imagePreview").fadeIn(650);
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
  $("#imageUpload").change(function () {
    $(".image-section").show();
    $("#btn-predict").show();
    $("#result").text("");
    $("#result").hide();
    readURL(this);
  });

  $("#btn-predict").click(function () {
    var form_data = new FormData($("#upload-file")[0]);

    // Show loading animation
    $(this).hide();
    $(".loader").show();

    // Make prediction by calling api /predict
    $.ajax({
      type: "POST",
      url: "/predict",
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Get and display the result
        $(".loader").hide();
        $("#result").fadeIn(600);
        $("#result").html(
          "<h4><center>Predicted Dish</center></h4> " + data.pred_label
        );

        // Check if nutritional data is available
        if (data.calories !== undefined) {
          $("#calories").text("Calories: " + data.calories);
        } else {
          $("#calories").text("Calories: Data not available");
        }

        if (data.fat !== undefined) {
          $("#fat").text("Fat: " + data.fat + "g");
        } else {
          $("#fat").text("Fat: Data not available");
        }

        if (data.protein !== undefined) {
          $("#protein").text("Protein: " + data.protein + "g");
        } else {
          $("#protein").text("Protein: Data not available");
        }

        if (data.carbs !== undefined) {
          $("#carbs").text("Carbs: " + data.carbs + "g");
        } else {
          $("#carbs").text("Carbs: Data not available");
        }

        // Fetch YouTube video data from Spoonacular API
        var spoonacular_api_url =
          "https://api.spoonacular.com/food/videos/search?apiKey=227a4d1c643048d785e6c5401e3f3d81&query=" +
          data.pred_label +
          "&number=4";
        $.ajax({
          type: "GET",
          url: spoonacular_api_url,
          success: function (response) {
            // Clear previous video iframes
            $("#video-section").empty();

            // Loop through each video in the response and append an iframe
            response.videos.forEach(function (video) {
              var iframe_html =
                '<iframe width="560" height="315" margin="10px" src="https://www.youtube.com/embed/' +
                video.youTubeId +
                '" frameborder="0" allowfullscreen></iframe>';

              $("#video-section").append(iframe_html);
            });
          },
          error: function (xhr, status, error) {
            console.log("Error fetching YouTube video data:", error);
          },
        });

        console.log("Success!");
      },
      error: function (xhr, status, error) {
        // Handle error
        console.log("Error:", error);
        $(".loader").hide();
        $("#result").fadeIn(600);
        $("#result").html(
          "Error: Failed to fetch data from Spoonacular API. Status Code: " +
            xhr.status
        );
      },
    });
  });
});

// Predict
//   $("#btn-predict").click(function () {
//     var form_data = new FormData($("#upload-file")[0]);

//     // Show loading animation
//     $(this).hide();
//     $(".loader").show();

//     // Make prediction by calling api /predict
//     $.ajax({
//       type: "POST",
//       url: "/predict",
//       data: form_data,
//       contentType: false,
//       cache: false,
//       processData: false,
//       async: true,
//       success: function (data) {
//         // Get and display the result
//         $(".loader").hide();
//         $("#result").fadeIn(600);
//         $("#result").html(
//           "<h3><center>Predicted Dish</center></h3> " + data.pred_label
//         );

//         // Check if nutritional data is available
//         if (data.calories !== undefined) {
//           $("#calories").text("Calories: " + data.calories);
//         } else {
//           $("#calories").text("Calories: Data not available");
//         }

//         if (data.fat !== undefined) {
//           $("#fat").text("Fat: " + data.fat + "g");
//         } else {
//           $("#fat").text("Fat: Data not available");
//         }

//         if (data.protein !== undefined) {
//           $("#protein").text("Protein: " + data.protein + "g");
//         } else {
//           $("#protein").text("Protein: Data not available");
//         }

//         if (data.carbs !== undefined) {
//           $("#carbs").text("Carbs: " + data.carbs + "g");
//         } else {
//           $("#carbs").text("Carbs: Data not available");
//         }

//         console.log("Success!");
//       },
//       error: function (xhr, status, error) {
//         // Handle error
//         console.log("Error:", error);
//         $(".loader").hide();
//         $("#result").fadeIn(600);
//         $("#result").html(
//           "Error: Failed to fetch data from Spoonacular API. Status Code: " +
//             xhr.status
//         );
//       },
//     });
//   });
// });
