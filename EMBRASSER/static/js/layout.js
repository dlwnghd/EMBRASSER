$(document).ready(function(){
    $(".main_navbar_menu").click(function(){
        sideMenu();
    });
});

function sideMenu() {
    let menu = document.querySelector(".main_navbar_menu");
    let side_menu = document.querySelector(".main_navbar");
    menu.classList.toggle("active");
    side_menu.classList.toggle("active");
}