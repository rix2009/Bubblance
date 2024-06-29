function change_visibility(self){
    if (self.style.visibility == "")
    {document.getElementById(self).style.visibility = "hidden";}
    else{document.getElementById(self).style.visibility = "";}
    }