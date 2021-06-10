function indexPage(){

    var products = document.getElementsByClassName("productButton");
    var searchBar = document.getElementById("searchBar")

    searchBar.addEventListener('keyup', function(){
        empty = true;
        for(let x = 0; x < products.length; x++){
            if(products[x].value.startsWith(searchBar.value) || products[x].textContent.split(' , ')[1].toLowerCase().startsWith(" "+searchBar.value.toLowerCase())){
                products[x].style.display = "inline-block";
                empty = false;
            }else{
                products[x].style.display = "none";
            }
        };
        if(empty){
            document.getElementById("extractForm").style.display = "block";
            document.getElementById("extractButton").setAttribute('href',"extract/"+searchBar.value);
            document.getElementById("extractButton").innerHTML = "Extract "+searchBar.value;
        }else{
            document.getElementById("extractForm").style.display = "none";
        }
    });
}