(function() {
  document.addEventListener('keydown', function(event) {
    if (event.keyCode === 9) {
      document.body.classList.add('keyboard-navigation');
    }
  });

  document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
  });

  if ((document.cookie = 'cookies_enabled=1') && (document.cookie.indexOf('cookies_enabled=') !== -1) && (document.cookie = 'cookies_enabled=1; expires=Thu, 01-Jan-1970 00:00:01 GMT')) {
    document.body.classList.add('cookies-enabled');
  }

  var localDay = Math.round((new Date().setHours(0, 0, 0, 0) - new Date(2021, 5, 19, 0, 0, 0, 0)) / 86400000);

  // Header

  var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  document.querySelector('.subtitle__day').innerHTML = '#' + localDay + ' &middot; ' + months[new Date().getMonth()] + ' ' + new Date().getDate() + ', ' + new Date().getFullYear() + ' &middot; ';

  // Results

  var resultsRequest = new XMLHttpRequest();
  resultsRequest.onload = function() {
    if (resultsRequest.status === 200) {
      document.querySelector('.results').innerHTML = resultsRequest.responseText;
    }
  };
  var id = new URLSearchParams(document.location.search).get('id');
  resultsRequest.open('GET', 'results?day=' + localDay + (id ? '&id=' + id : ''));
  resultsRequest.send();

  // Form

  document.querySelector('.day-input').value = localDay;

  // Link action

  var linkInput = document.querySelector('.link-input');
  var linkAction = document.querySelector('.link-action');
  if (linkInput && linkAction) {
    if (navigator.share) {
      linkAction.innerHTML = 'Share Link';
    }
    linkAction.addEventListener('click', function() {
      if (navigator.share) {
        navigator.share({ url: linkInput.value });
      } else {
        navigator.clipboard.writeText(linkInput.value).then(function() {
          linkAction.innerHTML = 'Copied!';
        });
      }
    });
  }
})();