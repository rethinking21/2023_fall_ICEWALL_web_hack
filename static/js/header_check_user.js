
axios.get('/getsessiondata/username')
  .then(function (response) {
    // 세션 데이터를 받아와서 처리합니다.
    var button = document.createElement('button');
    button.classList.add('btn');
    button.id = "login-logout-btn";

    if (response.data != null){
        document.getElementById("header-user").innerHTML = `Hello <b>${response.data}</b>!`;
        button.onclick = function() {
          location.href = '/logout';
        };
        button.innerText = "logout";
    }
    else{
        document.getElementById("header-user").innerHTML = 'please login';
        button.onclick = function() {
          location.href = '/login/';
        };
        button.innerText = "login";
    }
    document.getElementById("header-right-btn").appendChild(button);
  })
  .catch(function (error) {
    document.getElementById("header-user").innerHTML = 'please login';
    button.onclick = function() {
      location.href = '/login/';
    };
    button.innerText = "login";
    document.getElementById("header-right-btn").appendChild(button);
  });

  