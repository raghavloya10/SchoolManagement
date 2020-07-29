function view(id) {
  var elementToDisplay = document.getElementById(id)
  if (elementToDisplay.classList.contains("collapsableinitial")) {
    elementToDisplay.classList.remove("collapsableinitial");
    elementToDisplay.classList.add("collapsablefinal");
  } else {
    elementToDisplay.classList.remove("collapsablefinal");
    elementToDisplay.classList.add("collapsableinitial");
  }
}
