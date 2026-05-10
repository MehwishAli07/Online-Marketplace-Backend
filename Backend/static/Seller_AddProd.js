// Seller Page By Mehwish ALi

// Seller page Add Product form Functionality

// Toggle add form visibilty
function toggleForm() {
    const form = document.querySelector(".product-form");
    const submitBtn = document.querySelector(".submit-btn");
    const productId = document.getElementById("product_id");

    // if form is open → close it
    if (form.style.display === "flex") {
        form.style.display = "none";
        form.reset();
        productId.value = "";
        submitBtn.innerText = "Add Product";
    } 
    // if form is closed → open it
    else {
        form.style.display = "flex";

        // only reset if NOT editing
        if (!productId.value) {
            form.reset();
        }

        submitBtn.innerText = "Add Product";
    }
}
// Functionality for edit and button
function editProduct(id, name, description, price) {

    // show form
    document.querySelector(".product-form").style.display = "flex";

    // fill fields
    document.querySelector('input[name="name"]').value = name;
    document.querySelector('textarea[name="description"]').value = description;
    document.querySelector('input[name="price"]').value = price;

    // set hidden id
    document.getElementById("product_id").value = id;

    // change button text
    document.querySelector(".submit-btn").innerText = "Update Product";

    // scroll to form
    document.querySelector(".product-form").scrollIntoView({ behavior: "smooth" });
}
