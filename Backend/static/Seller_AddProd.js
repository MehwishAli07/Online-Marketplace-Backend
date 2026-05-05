// Seller page Add Product form Functionality

// Toggle add form visibilty
function toggleForm() {
    const form = document.querySelector(".product-form");

    form.style.display = "flex";

    // clear form
    form.reset();

    // clear product id
    document.getElementById("product_id").value = "";

    // reset button text
    document.querySelector(".submit-btn").innerText = "Add Product";
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
