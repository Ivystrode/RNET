var logo        = document.getElementById("main-title")
var sidenav     = document.getElementById('sidenav')
var dropownMenu = document.getElementById('dropdownbuttonmain')
var dropcontent = document.querySelector('.dropdown-content')
var sidebutton  = document.querySelectorAll('.sidebutton')
var dropbutton  = document.querySelectorAll('.unused_dropbutton')
var msgbox      = document.getElementById('msgbox')
var hidebutton  = document.getElementById('hideButton')

msgbox.style.display = 'none'


logo.addEventListener("click", function() {
    window.location.href = '/'
})

window.addEventListener("scroll", function(){
    let scrollAmount = window.scrollY
    if (scrollAmount < 15){
        sidenav.style.paddingTop = '60px'
    }
    if (scrollAmount > 15 && scrollAmount < 25){
        sidenav.style.paddingTop = '40px'
    }
    if (scrollAmount > 25 && scrollAmount < 35){
        sidenav.style.paddingTop = '30px'
    }
    if (scrollAmount > 35 && scrollAmount < 45){
        sidenav.style.paddingTop = '20px'
    }
    if (scrollAmount > 45){
        sidenav.style.paddingTop = '10px'
    }
})

dropownMenu.addEventListener("click", function(){
    if (dropcontent.style.display !== 'block'){
        console.log("dropdown")
        console.log(dropcontent.style.display)
        dropcontent.style.display = 'block'
    }
    else if (dropcontent.style.display === 'block'){
        console.log("hiding dropdown")
        dropcontent.style.display = 'none'
    }
})

for (let i = 0; i < sidebutton.length; i++){
    sidebutton[i].addEventListener("mousedown", function(){
        sidebutton[i].style.color = 'white'
        sidebutton[i].style.backgroundColor = 'rgb(54, 46, 46)'
    })
    sidebutton[i].addEventListener("mouseup", function(){
        sidebutton[i].style.color = 'midnightblue'
        sidebutton[i].style.backgroundColor = 'lightslategray'
    })
}

for (let i = 0; i < dropbutton.length; i++){
    dropbutton[i].addEventListener("click", function(){
        console.log("show msgbox")
        msgbox.style.display = 'block'
    })}

hidebutton.addEventListener("click", function(){
    console.log("hiding msgbox")
    msgbox.style.display = "none"
})


function toLogin(){
    window.location.assign("/login")
}

function toProfile(username){
    console.log("user link")
    window.location.assign("/profile/" + username)
}

