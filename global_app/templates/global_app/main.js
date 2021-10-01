
const overlay = document.querySelector(".overlay");
const modal = document.querySelector(".modal");
const description = document.querySelector("#description");


const handleClick = e => {
  const t = e.target;


  if (t.matches('.view') || t.matches('.view *')) {
    let data = t.dataset.info;
    console.log(data)
    
    let pTag = document.createElement('p');
    pTag.style = 'text-align:center;';
    pTag.innerHTML = data;
    
    description.innerHTML = pTag.outerHTML;
    
    overlay.classList.add("active");
    modal.classList.add("active");
  } else if (t.matches('.close') || t.matches('.close *') || t.matches('.overlay')) {
    overlay.classList.remove("active");
    modal.classList.remove("active");
  }
}

document.addEventListener("click", handleClick);