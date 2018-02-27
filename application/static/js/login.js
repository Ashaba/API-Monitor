function onSignIn(googleUser) {
    // Useful data for your client-side scripts:
    var profile = googleUser.getBasicProfile();
    // The ID token you need to pass to your backend:
    var id_token = googleUser.getAuthResponse().id_token;
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
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        headers: {
            'Authorization': id_token
        },
        success: function (data) {
            window.location.href = "/dashboard"
        }
    });
}
