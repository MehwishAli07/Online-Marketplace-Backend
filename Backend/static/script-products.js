// open a dialog box by id
function openDialog(id) {
  document.getElementById(id).showModal();
}

// Close the dialog box by id
function closeDialog(id) {
  document.getElementById(id).close();
}

//function to choose whether to display/hide filter ListFormat
//added by Caden Fontenot. will be called in HTML
function toggleFilters(){
	const filterList = document.getElementById("filterList");
	filterList.classList.toggle("hidden");
}