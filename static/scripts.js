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

    showSignInBtn(true);
}

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

    if (profile != null) {
        showSignInBtn(false);
    }
}