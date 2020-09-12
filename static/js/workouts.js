// Show distance input when Run, Ride, Swim, or Hike is selected
showDistanceForm = () => {
  let sport = $('#workout-type option:selected');
  if (sport.val() == 'Weight Training' || sport.val() == 'Other') {
    $('#workout-distance-container').hide();
  } else {
    $('#workout-distance-container').show();
  }
};

// $(document).ready(function () {
//   $('.submit-form-btn').click(function (e) {
//     if ($('input:invalid')) {
//       e.preventDefault();
//       $('input:invalid').addClass('error');
//       console.log('');
//     } else {
//       $('input:valid').removeClass('error');
//       console.log('no errors');
//       $('.add-workout-form').submit();
//     }
//   });
// });
