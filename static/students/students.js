function view(id) {
  var elementToDisplay = document.getElementById(id)
  if (elementToDisplay.classList.contains("collapsableinitial")) {
    elementToDisplay.classList.remove("collapsableinitial");
    elementToDisplay.classList.add("collapsablefinal");
  } else {
    elementToDisplay.classList.remove("collapsablefinal");
    elementToDisplay.classList.add("collapsableinitial");  }
  var correspondingTable = document.getElementById(id.toString().concat("table"));
  var rowCount = correspondingTable.getElementsByTagName('tr').length;
  console.log(rowCount);

  if(rowCount == 1) {
    var id2 = id.toString().concat("temp");
    var temp = document.getElementById(id2);
    temp.style.display = "block";
  }
}
