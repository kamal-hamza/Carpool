function submit() {
    document.getElementById('formSub').submit()
}

navLinks = document.getElementsByClassName('navlink')

function currentPage() {
    for (var i = 0; i < navLinks.length; i++) {
        if (window.location.href == navLinks[i].href) {
            navLinks[i].class = "active";
        }
    }
}

