window.onload = function() {
    $('.g-signin2 div div span span:last').text("Sign in with Google");
    $('.g-signin2 div div span span:first').text("Sign in with Google");

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/authenticated');
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        var response = JSON.parse(xhr.responseText);

        console.log(response);
        if (response.data) {
            console.log("Logged in");
            showSignInBtn(false);
        }
        else {
            console.log("Not logged in");
            showSignInBtn(true);
        }
    }
    xhr.send()
}
function showSignInBtn(setVisible) {
    if(setVisible) {
        $('.sign-in').css('display', 'block');
        $('.sign-out').css('display', 'none');
    }
    else {
        $('.sign-in').css('display', 'none');
        $('.sign-out').css('display', 'block');
    }
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
    console.log('User signed out.');
    });

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/oauthcallback');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log('Logging out the user.');

        window.location.href = '/';
    }
    xhr.send('logout=true');
    
}

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    
    if (profile != null) {
        var id_token = googleUser.getAuthResponse().id_token;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/oauthcallback');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            var response = JSON.parse(xhr.responseText);

            if (response['data'] == "Logged In") {
                $.ajax({
                    type:'GET',
                    url:'/',
                    success: function() {
                        result_text = response['message'] + " Reloading in 4 seconds...";
                        $('.result').html(result_text);
                        setTimeout(function() {
                            window.location.href="/";
                        }, 4000);
                    }
                })
            }
        };
        xhr.send('idtoken=' + id_token);
    }
}