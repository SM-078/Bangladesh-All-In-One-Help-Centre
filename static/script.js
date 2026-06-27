function alertHotline(number) {
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

  if (isMobile) {
    // Redirect to phone dialer
    window.location.href = `tel:${number}`;
  } else {
    // Show a message if not on mobile
    if (number === '999') {
      alert("Dial 999 from your phone now for immediate emergency help.");
    } else if (number === '333') {
      alert("Dial 333 from your phone now for government help regarding shelter and precaution.");
    } else {
      alert("Unknown hotline number.");
    }
  }
}

// Attach event listeners after DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  const hotline999 = document.getElementById("hotline-999");
  const hotline333 = document.getElementById("hotline-333");

  if (hotline999) {
    hotline999.addEventListener("click", function() {
      alertHotline('999');
    });
  }

  if (hotline333) {
    hotline333.addEventListener("click", function() {
      alertHotline('333');
    });
  }
});

             

