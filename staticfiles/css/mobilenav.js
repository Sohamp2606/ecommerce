const hamburger = document.querySelector(".hamburger");
const mobilenav = document.querySelector(".mobilenav");

hamburger.addEventListener("click",()=>{
   console.log('soham');
    mobilenav.classList.toggle("opendrawer");
})
