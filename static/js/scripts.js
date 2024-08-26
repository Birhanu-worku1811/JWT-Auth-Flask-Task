const apiBaseUrl = window.location.origin;

let accessToken = null;
let refreshToken = null;

$(document).ready(function () {
    // Register User
    $('#register-form').on('submit', function (e) {
        e.preventDefault();

        const username = $('#register-username').val();
        const email = $('#register-email').val();
        const password = $('#register-password').val();

        $.ajax({
            url: `${apiBaseUrl}/register`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, email, password }),
            success: function (response) {
                $('#register-result').text(response.message).addClass('text-success');
                $('#register-form')[0].reset();
            },
            error: function (xhr) {
                $('#register-result').text(`Error: ${xhr.responseJSON.message}`).addClass('text-danger');
            }
        });
    });

    // Login User
    $('#login-form').on('submit', function (e) {
        e.preventDefault();

        const username = $('#login-username').val();
        const password = $('#login-password').val();

        $.ajax({
            url: `${apiBaseUrl}/login`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, password }),
            success: function (response) {
                $('#login-result').text(response.message).addClass('text-success');
                accessToken = response.tokens.access_token;
                refreshToken = response.tokens.refresh_token;

                // Fetch the user profile info
                fetchUserProfile();

                // Switch to the dashboard
                $('#auth-section').hide();
                $('#dashboard-section').show();
            },
            error: function (xhr) {
                $('#login-result').text(`Error: ${xhr.responseJSON.error}`).addClass('text-danger');
            }
        });
    });

    // Fetch User Profile
    function fetchUserProfile() {
        $.ajax({
            url: `${apiBaseUrl}/profile`,
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
            success: function (response) {
                $('#user-name').text(response.user_details.username);
                $('#profile-username').text(response.user_details.username);
                $('#profile-email').text(response.user_details.email);
            },
            error: function (xhr) {
                $('#response-output').text(`Error: ${xhr.responseJSON.error}`).addClass('text-danger');
            }
        });
    }

    // Who Am I
    $('#profile-btn').on('click', function () {
        $.ajax({
            url: `${apiBaseUrl}/profile`,
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
            success: function (response) {
                $('#response-output').text(JSON.stringify(response, null, 2));
            },
            error: function (xhr) {
                $('#response-output').text(`Error: ${xhr.responseJSON.error}`).addClass('text-danger');
            }
        });
    });

    // Refresh Token
    $('#refresh-btn').on('click', function () {
        $.ajax({
            url: `${apiBaseUrl}/refresh`,
            method: 'GET',
            headers: {
                Authorization: `Bearer ${refreshToken}`
            },
            success: function (response) {
                $('#response-output').text('Access token refreshed.');
                accessToken = response.access_token;
            },
            error: function (xhr) {
                $('#response-output').text(`Error: ${xhr.responseJSON.error}`).addClass('text-danger');
            }
        });
    });

    // Verify Token
    $('#verify-btn').on('click', function () {
        $.ajax({
            url: `${apiBaseUrl}/verify`,
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
            success: function (response) {
                $('#response-output').text(JSON.stringify(response, null, 2));
            },
            error: function (xhr) {
                $('#response-output').text(`Error: ${xhr.responseJSON.error}`).addClass('text-danger');
            }
        });
    });
});
