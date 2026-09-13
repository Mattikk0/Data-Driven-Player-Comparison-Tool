const button = document.getElementById('search-button');
const input = document.getElementById('name-input');

button.addEventListener('mouseenter', () => {
    if (input.value.trim() == '') {
        button.classList.add('shake-horizontal');
    }
    else{
        button.classList.add('shadow-drop-center');
    }
});

button.addEventListener('mouseleave', () => {
    button.classList.remove('shake-horizontal');
    button.classList.remove('shadow-drop-center');
});

button.addEventListener('click', () => {
    if (input.value.trim() == '') {
        input.classList.add('shake-horizontal');
    }
});

input.addEventListener('animationend', () => {
    input.classList.remove('shake-horizontal');
});
