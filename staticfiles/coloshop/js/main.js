document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            let productId = this.getAttribute("data-product-id");

            fetch(`/cart/add/${productId}/`, {
                method: "GET",
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("✅ تم إضافة المنتج إلى السلة!");
                } else {
                    alert("❌ حدث خطأ أثناء الإضافة!");
                }
            });
        });
    });
});