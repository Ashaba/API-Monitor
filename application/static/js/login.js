function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    userDetails = {
        "ID": profile.getId(),
        "fullName": profile.getName(),
        "nickName": profile.getGivenName(),
        "familyName": profile.getFamilyName(),
        "imageUrl": profile.getImageUrl(),
        "email": profile.getEmail(),
        "token": googleUser.getAuthResponse().id_token
    };
    $.ajax({
        type: 'POST',
        url: '/auth',
        data: JSON.stringify(userDetails),
        contentType: "application/json; charset=utf-8",
        success: function () {
            window.location.href = "/dashboard"
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        window.location.href = "/"
    });
}

$(function() {
    gapi.load('auth2', function () {
        gapi.auth2.init();
    });
});
