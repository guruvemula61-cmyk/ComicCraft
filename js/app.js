const panels = document.querySelectorAll(".fade-panel");

function revealPanels(){

panels.forEach(panel => {

const top = panel.getBoundingClientRect().top;

const trigger = window.innerHeight * 0.85;

if(top < trigger){
panel.classList.add("visible");
}

});

}

window.addEventListener("scroll", revealPanels);

revealPanels();