console.log('Script loaded');

$(document).ready(function() {
  $('.reserve-btn').click(function() {
    var seat_number = $(this).data('seat');
    var status = $(this).closest('tr').find('.status').attr('class').split(' ')[1];
    if (status == 'red') {
      alert('This seat is already reserved. Please choose another seat.');
      return;
    }
    var name = prompt('Please enter your name:');
    if (!name) {
      alert('You must enter a name to reserve a seat.');
      return;
    }
    $.post('/reserve', {
      seat: seat_number,
      name: name
    }, function(data) {
      var new_status = data.status == 'success' ? 'red' : 'green';
      $('.reserve-btn[data-seat=' + seat_number + ']').closest('tr').find('.status').removeClass('green red').addClass(new_status);
      $('.reserve-btn[data-seat=' + seat_number + ']').closest('tr').find('.name').text(name);
    });
  });
});
