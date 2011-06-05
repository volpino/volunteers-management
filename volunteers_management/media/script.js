function redirect_home() {
    window.setTimeout(function () {
        location.href = '/';
    }, 2000);
}


function are_you_sure(redirect) {
    if (confirm("Are you sure?")) {
        location.href = redirect;
    }
}

