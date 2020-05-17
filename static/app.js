

function getData(vars){
  for(x of vars){
    document.getElementById("dropList").innerHTML +=
  '<a id="'+x.ID+'" class="dropdown-item" href="#">'+x.fName+' '+x.lName+'</a>';
};
    return vars;
  };


  window.onload=function(){
    document.querySelector('.dropdown').addEventListener('click', function(event){
      console.log(event.target.id);
    });
  };
