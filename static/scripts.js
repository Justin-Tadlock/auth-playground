window.onload = function() {

    checkAuthenticated();
}


function checkAuthenticated() {
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
    xhr.send();
}


function logout() {
    console.log("Attempting logout...");
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/logout');
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log("Logging out the user");
        $('.result').html("Successfully logged out! Redirecting in 2 seconds...");
        setTimeout(function() {
            window.location.href = '/';
        }, 2000);
    }
    xhr.send('logout=true');
}


function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}

// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().

    console.log('status: ', response.status);

    if (response.status === 'connected') {
        // Logged into your app and Facebook.
        var access_token = FB.getAuthResponse()['accessToken'];
        console.log('Successfully connected!');

        var state = $('#state').data().state;

        FB.api('/me', function(response) {
            console.log('Successful login for: ' + response.name);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/fbconnect');
            xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
            xhr.onload = function() {
                console.log(xhr.responseText);

                // Facebook verification response from server
                var server_response = JSON.parse(xhr.responseText);

                // If data is true, it means that the user is authenticated and needs to refresh page
                if (server_response.data) {
                    $('.result').html("Successfully logged in as " + response.name + ". Redirecting in 4 seconds...");
                    setTimeout(function() {
                        window.location.href = "/";
                    }, 4000);
                }
            };
            xhr.send('accessToken=' + access_token + '&user_id=' + response.id + '&state=' + state);
        });
    }
}


window.fbAsyncInit = function() {
    FB.init({
        appId      : '434043257321789',
        cookie     : true,  // enable cookies to allow the server to access 
                            // the session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v3.1' // The Graph API version to use for the call
    });
};

// Load the SDK asynchronously
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
} (document, 'script', 'facebook-jssdk'));


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

    if (FB.getAccessToken() != null) {
        FB.logout(function(response) {
            // user is now logged out from facebook
        });
    }

    logout();
}

function onSignIn(googleUser) {
    console.log("Enter onSignIn()"); 

    var id_token = googleUser.getAuthResponse().id_token;

    var state = $('#state').data().state;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/gconnect');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        var profile = googleUser.getBasicProfile();

        console.log('Signed in as: ' + profile.getName());

        var server_response = JSON.parse(xhr.responseText);

        // If data is true, it means that the user is authenticated and needs to refresh page
        if (server_response.data) {
            $('.result').html("Successfully logged in as " + profile.getName() + ". Redirecting in 4 seconds...");
            setTimeout(function() {
                window.location.href = "/";
            }, 4000);
        }
    };
    xhr.send('idtoken=' + id_token + '&state=' + state);
}