var packages = document.getElementsByClassName("package_names"); //Some global variables
var length_of_packages = packages.length;
console.log(packages)



function give_id() {
    for (var i = 3; i < length_of_packages; i++){               //This function gives an unique id to each package, so we can easily navigate to them later
        var id_name = "package_name_id" + i;
        packages[i].id = id_name;
        }
}

function change_display(){                                      //We add a clickable element, that calls a function to extend information on given package.

    for (var i = 0; i < length_of_packages; i++){
        packages[i].onclick = function(e){

            if (this.childNodes[0].className == "sub_info_block")   //If package info is hidden --> show it and vice versa.

            {
                for (y = 0; y < this.childNodes.length; y++){
                    this.childNodes[y].className = "sub_info_none";
                    }
            } else {

                for (y = 0; y < this.childNodes.length; y++){
                    this.childNodes[y].className = "sub_info_block";
                   }
            }


                }
            }
        }

function close_preface(){                                                       //This function is called when you press the x-symbol on the preface.
    document.getElementsByClassName("modal")[0].style.display = "none";
}
