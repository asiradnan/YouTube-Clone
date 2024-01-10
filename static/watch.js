function uploadVid() {
    window.location.href = 'upload';
}
function lout(){
    window.location.href = 'account_logout';
}
function acc(){
    let x = document.getElementById('useracc');
    if (x.style.display=='block') {
        x.style.display='none';
        
    }
    else {
        x.style.display='block';
       
    }
}
window.onclick = clickyy;
function clickyy(event) {
    if (!event.target.matches('.user')) {
      let x = document.getElementById("useracc"); 
        x.style.display = "none";
    }
    if (event.target.id != 'noti'){
        let x = document.getElementById('notification');
        x.style.display='none';
    }
    if (event.target.id != 'togg') document.getElementById('fullsidebar').style.display = 'none';
}
function shownoti(){
    let x = document.getElementById('notification');
    if (x.style.display=='none') x.style.display='block';
    else x.style.display='none'; 
    console.log("hereeeeeeeeeee");
}
function sidetog(){
    let x= document.getElementById('fullsidebar');
    if (x.style.display=='none') {
        x.style.display='block';
    }
    else{
        x.style.display='none';
    }
}