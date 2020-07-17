// Show distance input when Run, Ride, Swim, or Hike is selected
showDistanceForm = () => {
  let sport = $('#workout-type option:selected');
  if (sport.val() == 'Weight Training' || sport.val() == 'Other') {
    $('#workout-distance-container').hide();
    console.log(sport.val());
  } else {
    $('#workout-distance-container').show();
    console.log(sport.val());
  }
};
