// Initialize FullCalendar
document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      locale: 'en', 
      selectable: true,
      dateClick: function (info) {
        // Capture the date clicked by user and display it
        document.querySelector("#selected-date").textContent = `Selected Date: ${info.dateStr}`;
        selectedDate = info.dateStr; // Store the selected date globally
      }
    });
    calendar.render();
  });
  
  // Function to handle saving the appointment
  function saveAppointment() {
    const selectedTime = document.querySelector('.time-btn.active');
  
    if (selectedDate && selectedTime) {
      alert(`Appointment booked for ${selectedDate} at ${selectedTime.innerText}`);
      // tryto include a way to send the data to your backend to save the appointment
    } else {
      alert('Please select both a date and time.');
    }
  }
  
  // Add event listener to time buttons
  const timeButtons = document.querySelectorAll('.time-btn');
  timeButtons.forEach(button => {
    button.addEventListener('click', function () {
      timeButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
    });
  });
  