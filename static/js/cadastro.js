nome = document.querySelector("typeName").text
erroNome = document.querySelector("erroNome").text

if ( nome == ""){
    erroNome.value = "Nome incalido"
}